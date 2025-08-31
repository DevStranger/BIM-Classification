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

If you would like to see how the model was trained and enhanced, you need to:

1. Clone the repository

```
git clone https://github.com/DevStranger/BIM-Classification.git
```

2. Start Jupyter Lab (or Jupyter Notebook) in your cmd (command line lol)

```
jupyter lab
```

The notebooks you may find interesting (with coresponding result files):
-
-
-

## Results and Evaluation

*This section will include quantitative evaluation metrics (accuracy, F1-score, similarity scores) and qualitative analysis of classification results once available.*

## Simple GUI Demo

*will apear here in a second*

## Disclaimer
This project was developed as part of an internship at Datacomp IT in Kraków, Poland. The work presented here reflects the scope and objectives of the internship and is intended for educational and prototypical purposes.
