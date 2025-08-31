# BIM Element Semantic Classification using Sentence-Transformers
This project aims to develop a prototype system for automatic classification of BIM elements based on their textual descriptions in IFC files. The system assigns BIM elements to classes from multiple classification dictionaries supported by bSDD (including CCI, Uniclass, and others) by leveraging semantic embeddings.

Instead of relying on supervised fine-tuning (which requires labeled datasets), the approach uses sentence-transformers to generate semantic embeddings of element descriptions and classification classes, comparing them via cosine similarity. This enables flexible, multi-dictionary classification without binding to a fixed label set.

The project also explores enhancing embeddings quality using contrastive learning and few-shot learning techniques to improve classification accuracy. Initially, we wanted to use TSDAE but it requires for the model to have cross-attention layers and we were set on using the multilingual sentence transformer (due to the fact the IFC descriptions that come from our BIM models are often in Polish).

## Key features
- automatic extraction and parsing of textual descriptions from IFC files
- embedding generation of BIM element descriptions and class labels using multilingual sentence-transformers
- semantic similarity matching across multiple classification dictionaries (CCI, Uniclass, etc.)
- optional fine-tuning via contrastive learning and few-shot learning to boost accuracy
- evaluation using top-k accuracy, cosine similarity scores, F1-score and other metrics
- export of classification results compatible with BIMVision via JSON/CSV format for seamless integration
- modular pipeline designed for extensibility and further dictionary additions

## Technologies & Tools
- **Language:** Python 3.10+
- **NLP:** sentence-transformers (paraphrase-multilingual-MiniLM), PyTorch
- **Data processing:** pandas, numpy, matplotlib
- **APIs:** bSDD REST API or local dictionary files
- **Evaluation metrics:** cosine similarity, top-k accuracy, F1-score
- **Formats:** JSON/CSV(?) for data exchange with BIMVision (C# interface)
- **Development:** Jupyter Notebook, Git, VSCode

## Usage

If you want to see how the algorithm works using a simple GUI, you need to:

1. Clone the repository

```
git clone https://github.com/DevStranger/BIM-Classification.git
```

2. Go to the right location

```
cd BIM-Classification
```

3. Install the required libraries

```
pip install -r requirements.txt
```

4. Go into the right folder

```
cd code
```

5. Run the app :)

```
streamlit run app.py
```
_*the suggested sample data file is ```/data/ifc_objects.csv```_

-------------------------

If you would like to see how the model was trained and enhanced, you need to:

1. Clone the repository

```
git clone https://github.com/DevStranger/BIM-Classification.git
```

2. Start Jupyter Lab (or Jupyter Notebook) in your cmd (command line lol)

```
jupyter lab
```

Contents of the notebooks (in order of creation or recent updates):
- **_test.ipynb_** - designed to precompute embeddings for CCI data to save on computational time and complexity in future tasks. It ensures that embeddings are either loaded if already computed or generated and saved if not.
- **_parsed_test.ipynb_** - performs semantic classification of IFC elements by matching them to bSDD classes using sentence embeddings and cosine similarity. It demonstrates an automated way to assign standardized building system classes to IFC elements based on textual descriptions (_nota bene:_ this is the initial test done on imaginary, sample data not real-life files).
- **_full_bsdd_tests.ipynb_** - performs semantic classification of IFC elements against bSDD classes, similar to parsed_test.ipynb, but it incorporates more detailed IFC information, including numeric properties and P-Set attributes, to enhance classification accuracy and full bSDD information pulled from the official bSDD site. It demonstrates a more comprehensive semantic mapping pipeline.
- **_tsdae_test.ipynb_** - fine-tunes a sentence embedding model using TSDAE (Text-to-Text Denoising AutoEncoder) on IFC data, then uses the fine-tuned model to classify IFC elements against CCI classes. The aim is to improve semantic embeddings for domain-specific text and provide more accurate similarity-based classification. It was later on proved, that this method will be inefficient in our case due to the use of a multilingual sentence-transformer which does not have the required cross-attention layers.
- **_tsdae_model_train.ipynb_** - prepares a domain-specific TSDAE model for IFC and bSDD textual data. It consolidates multiple IFC CSV files, applies soft filtering on bSDD classes, and fine-tunes a sentence embedding model using a Denoising AutoEncoder.
- **_mapped_ifc_test.ipynb_** - performs keyword-assisted semantic classification of IFC elements against bSDD classes using a fine-tuned TSDAE embedding model. It combines type-specific keyword filtering with embeddings to improve classification relevance.
- **_ifc_bsdd_mapping.ipynb_** - demonstrates a semantic mapping and clustering pipeline for IFC elements against bSDD classes using sentence embeddings. It combines similarity-based matching with unsupervised clustering and visualization, providing both individual matches and global structure insights.
- **_extra_layer_test.ipynb_** - demonstrates a hybrid classification pipeline that combines sentence embeddings from a fine-tuned TSDAE/few-shot model with a logistic regression classifier. It shows how to add an extra classification layer on top of embeddings to predict labels for IFC elements.
- **_contrastive_test.ipynb_** - prepares a contrastive learning dataset from IFC and bSDD textual data and fine-tunes a sentence embedding model using the Multiple Negatives Ranking Loss (contrastive learning). The goal is to create embeddings that better capture semantic similarity between IFC elements and bSDD classes.
- **_initial_tsdae_fewshot_test.ipynb_** - demonstrates few-shot fine-tuning of a contrastive sentence embedding model on a small domain-specific dataset and the addition of a logistic regression classification layer on top of embeddings. It creates a hybrid embedding + classifier model for IFC/bSDD text classification. Throughout the project, this notebook was used for various tasks and experiments along with the `tester.ipynb` notebook.
- **_tester.ipynb_**- used throughout the project as a multipurpose tool, integrating several key workflows: it handles final evaluation of IFC object classification, performs post-processing and reranking of predictions, supports clustering of bSDD classes, and combines hybrid approaches including cosine similarity, few-shot embeddings, and a trained classifier. It also includes augmentation steps for IFC descriptions and generates final labels in CSV and JSON formats, alongside visualizations and summary statistics for analysis.
  
## Results and Evaluation

*This section will include quantitative evaluation metrics (accuracy, F1-score, similarity scores) and qualitative analysis of classification results once available.*

## Simple GUI Demo 
_*using the sample data file ```/data/ifc_objects.csv```_

### After running the app, you will see a simple GUI asking you to upload a file in either ```.csv``` or ```.json``` format
<img width="1800" height="432" alt="Zrzut ekranu 2025-08-31 153209" src="https://github.com/user-attachments/assets/12afa8a3-d984-47d9-b763-6bafd5105a63" />

### When you upload the file, the app will let you know how many IFC objects have been found inside of it
<img width="1723" height="723" alt="Zrzut ekranu 2025-08-31 153420" src="https://github.com/user-attachments/assets/1274a7b3-ecab-4cdd-984b-1887a4a2ceca" />

### Now we need to press the button to start the classification process (it might take a while depending on the file size and its contents)
<img width="1731" height="189" alt="Zrzut ekranu 2025-08-31 153426" src="https://github.com/user-attachments/assets/64f1aff6-5ff6-437a-b7d5-4400c4619dce" />

### After the algorithm is done, you will see the classification results in a table containing the best 3 calculated matches along with their score and the result of the classification layer
<img width="1736" height="377" alt="Zrzut ekranu 2025-08-31 153433" src="https://github.com/user-attachments/assets/118d8e34-7ea5-4592-8d71-f743b68f2673" />
<img width="1772" height="412" alt="Zrzut ekranu 2025-08-31 153448" src="https://github.com/user-attachments/assets/34a63f6f-f97d-4359-b1cd-6af134d2a310" />

### You can choose to download the classification results in a ```.csv``` file
<img width="424" height="89" alt="Zrzut ekranu 2025-08-31 153453" src="https://github.com/user-attachments/assets/061cb301-066f-4cb8-b656-fcfe7e864320" />

### Done!
<img width="445" height="121" alt="Zrzut ekranu 2025-08-31 153503" src="https://github.com/user-attachments/assets/5f4060f7-84d6-4bad-b29f-d80ac9c04d37" />

## Disclaimer
This project was developed as part of an internship at Datacomp IT in Kraków, Poland. The work presented here reflects the scope and objectives of the internship and is intended for educational and prototypical purposes.
