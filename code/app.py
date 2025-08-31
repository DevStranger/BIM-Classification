import streamlit as st
import pandas as pd
import json, io, joblib, re
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import torch

# Upiększacze
st.set_page_config(page_title="Klasyfikator IFC", page_icon="🏗️", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #F0F8FF; }
    .stButton>button { background-color: #1E90FF; color:white; font-size:16px; border-radius:8px; padding:10px 20px;}
    .css-1d391kg { color:#1E90FF; font-weight:bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🏗️ Klasyfikator IFC")
st.write("Wgraj plik IFC (JSON lub CSV), a aplikacja sformatuje dane i przeprowadzi klasyfikację.")

# Funkcje pomocnicze
def extract_keywords(text):
    if pd.isna(text):
        return []
    return re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())

def augment_text(ifc_text, ifc_type):
    variants = [ifc_text.strip()]
    if ifc_type:
        variants.append(f"{ifc_type} element: {ifc_text}")
        variants.append(f"{ifc_text} (IfcType: {ifc_type})")
    synonyms = {
        "wall": ["partition", "barrier", "external wall", "internal wall"],
        "slab": ["floor plate", "concrete slab", "prefabricated slab"],
        "roof": ["roofing", "roof structure", "covering"],
        "column": ["pillar", "support column"],
        "beam": ["support beam", "girder"],
        "duct": ["air channel", "ventilation duct"],
        "pipe": ["installation pipe", "tube", "pipeline"]
    }
    for word, syns in synonyms.items():
        if word in ifc_text.lower():
            for s in syns:
                variants.append(ifc_text.replace(word, s))
    return list({v.strip() for v in variants if v.strip()})

def embed_with_augmentation(model, ifc_text, ifc_type):
    aug_texts = augment_text(ifc_text, ifc_type)
    embeddings = model.encode(aug_texts, convert_to_tensor=True)
    return embeddings.mean(dim=0, keepdim=True)

def rerank_with_postprocessing(ifc_text, ifc_type, candidates, bsdd_df):
    ifc_keywords = extract_keywords(ifc_text) + [ifc_type.lower()]
    ifc_text_lower = ifc_text.lower()
    reranked = []
    general_terms = {"wall", "slab", "roof", "floor", "column"}
    technical_terms = {"duct", "corner", "cover", "pipe", "beam"}
    installation_terms = {"plumbing", "installation", "pipe", "duct", "column"}
    for idx, sim in candidates:
        bsdd_row = bsdd_df.iloc[idx]
        bsdd_text = str(bsdd_row["full_text"]).lower()
        score = sim
        for kw in ifc_keywords:
            if kw in general_terms and kw in bsdd_text:
                score += 0.02
            if kw in technical_terms and kw in bsdd_text:
                score += 0.03
        if not any(term in ifc_text_lower for term in installation_terms):
            for t in technical_terms:
                if t in bsdd_text and t not in ifc_text_lower:
                    score -= 0.03
        reranked.append((idx, score))
    return sorted(reranked, key=lambda x: x[1], reverse=True)

def add_classifier_predictions(ifc_embedding, result_entry, clf):
    ifc_embedding_np = ifc_embedding.cpu().numpy()
    probas = clf.predict_proba(ifc_embedding_np)[0]
    top3_idx = probas.argsort()[-3:][::-1]
    top3_codes = [clf.classes_[i] for i in top3_idx]
    top3_scores = [probas[i] for i in top3_idx]
    for i in range(3):
        result_entry[f"Classifier_Top{i+1}_Code"] = top3_codes[i]
        result_entry[f"Classifier_Top{i+1}_Score"] = round(top3_scores[i],4)
    if "Top1_Kod_bSDD" in result_entry:
        result_entry["Hybryda_Zgodnosc"] = (top3_codes[0] == result_entry["Top1_Kod_bSDD"])
    return result_entry

def parse_ifc_json(file) -> pd.DataFrame:
    data = json.load(file)
    parsed_rows = []
    for obj in data:
        attributes = obj.get("Attributes", [])
        property_sets = obj.get("PropertySets", [])
        global_id = next((a["Value"] for a in attributes if a["Name"] == "Guid"), "N/A")
        name = next((a["Value"] for a in attributes if a["Name"] == "Name"), "N/A")
        description = next((a["Value"] for a in attributes if a["Name"] == "Description"), "")
        properties_text = []
        for pset in property_sets:
            for prop in pset.get("Properties", []):
                pname = prop.get("Name","").strip()
                pval = str(prop.get("Value","")).strip()
                if pname and pval:
                    properties_text.append(f"{pname}: {pval}")
        full_text = description.strip()
        if properties_text:
            full_text += ". " + "; ".join(properties_text)
        parsed_rows.append({"GlobalId": global_id,"Name": name,"Text": full_text.strip()})
    return pd.DataFrame(parsed_rows)

# Ładowanie pliku
uploaded_file = st.file_uploader("Wgraj plik IFC (JSON lub CSV)", type=["json","csv"])

if uploaded_file:
    if uploaded_file.name.endswith(".json"):
        st.write("Parsuję JSON IFC...")
        ifc_df = parse_ifc_json(uploaded_file)
    else:
        ifc_df = pd.read_csv(uploaded_file)
    st.success(f"Wczytano {len(ifc_df)} obiektów IFC")
    
    st.dataframe(ifc_df, use_container_width=True, height=300)  # przewijalna tabela

    # Klasyfikacja
    if st.button("Rozpocznij klasyfikację"):
        st.info("Trwa klasyfikacja... to może chwilę potrwać.")
        
        # Wczytaj model i klasyfikator
        model = SentenceTransformer("../models/fewshot_finetuned_contrastive_updated")
        clf = joblib.load("../models/fewshot_with_classifier/classifier.pkl")
        bsdd_df = pd.read_csv("../data/contrastive_dataset/file02.csv")
        bsdd_df["full_text"] = bsdd_df["Code"].astype(str) + " — " + bsdd_df["Name"].fillna("") + " — " + bsdd_df["Text"].fillna("")
        bsdd_embeddings = model.encode(bsdd_df["full_text"].tolist(), convert_to_tensor=True)
        
        results_post = []
        for _, row in ifc_df.iterrows():
            ifc_type = str(row.get("IfcType","")).upper()
            ifc_name = str(row.get("Name",""))
            ifc_text = str(row.get("Text",""))
            full_ifc_text = ifc_name + " " + ifc_text
            ifc_embedding = embed_with_augmentation(model, full_ifc_text, ifc_type)
            similarities = util.cos_sim(ifc_embedding, bsdd_embeddings)[0]
            top_results = torch.topk(similarities, k=3)
            candidates = list(zip(top_results.indices.tolist(), top_results.values.tolist()))
            reranked = rerank_with_postprocessing(full_ifc_text, ifc_type, candidates, bsdd_df)
            
            entry = {"GlobalId": row.get("GlobalId",""), "IfcType": ifc_type, "Name": ifc_name, "Opis_IFC": ifc_text[:300]}
            for rank,(idx,score) in enumerate(reranked[:3]):
                if score >= 0.5:
                    entry[f"Top{rank+1}_Kod_bSDD"] = bsdd_df.iloc[idx]["Code"]
                    entry[f"Top{rank+1}_Nazwa_bSDD"] = bsdd_df.iloc[idx]["Name"]
                    entry[f"Top{rank+1}_Podobieństwo"] = round(score,4)
            entry = add_classifier_predictions(ifc_embedding, entry, clf)
            results_post.append(entry)
        
        df_post = pd.DataFrame(results_post)
        st.success("✅ Klasyfikacja zakończona!")
        st.dataframe(df_post, use_container_width=True, height=500)  # przewijalna tabela
        
        # Pobieranie CSV
        csv_buffer = io.StringIO()
        df_post.to_csv(csv_buffer, index=False)
        st.download_button(
            label="💾 Pobierz wyniki klasyfikacji jako CSV",
            data=csv_buffer.getvalue(),
            file_name="wyniki_ifc_klasyfikacja.csv",
            mime="text/csv"
        )
