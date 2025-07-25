import json
import csv
import os

# Ścieżki do plików
input_path = "../data/sample_ifc.json"         # plik JSON z BIMVision
output_path = "../data/ifc_objects.csv"        # plik wynikowy CSV

# Lista interesujących typów IFC
component_ifc_types = {
    "IFCWALL", "IFCDOOR", "IFCWINDOW", "IFCSLAB",
    "IFCCOLUMN", "IFCBEAM", "IFCSTAIR", "IFCRAILING",
    "IFCFURNISHINGELEMENT"
}

# Wczytaj dane wejściowe
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

parsed_rows = []

# Przetwarzanie obiektów
for obj in data:
    attributes = obj.get("Attributes", [])
    property_sets = obj.get("PropertySets", [])

    # Znajdź typ IFC
    ifc_type = next((a["Value"] for a in attributes if a["Name"] == "IfcEntity"), None)
    if not ifc_type or ifc_type.upper() not in component_ifc_types:
        continue

    global_id = next((a["Value"] for a in attributes if a["Name"] == "Guid"), "N/A")
    name = next((a["Value"] for a in attributes if a["Name"] == "Name"), "N/A")
    description = next((a["Value"] for a in attributes if a["Name"] == "Description"), "")

    # Sklejanie właściwości w jeden tekst
    properties_text = []
    for pset in property_sets:
        for prop in pset.get("Properties", []):
            pname = prop.get("Name", "").strip()
            pval = prop.get("Value", "").strip()
            if pname and pval:
                properties_text.append(f"{pname}: {pval}")

    full_text = description.strip()
    if properties_text:
        full_text += ". " + "; ".join(properties_text)

    parsed_rows.append({
        "GlobalId": global_id,
        "IfcType": ifc_type,
        "Name": name,
        "Text": full_text.strip()
    })

# Tworzenie folderu jeśli nie istnieje
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Zapis do pliku CSV
with open(output_path, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["GlobalId", "IfcType", "Name", "Text"])
    writer.writeheader()
    writer.writerows(parsed_rows)

print(f"Zapisano {len(parsed_rows)} komponentów do pliku: {output_path}")
