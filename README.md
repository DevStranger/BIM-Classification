# BIM Element Semantic Classification using Sentence-Transformers
This project aims to develop a prototype system for automatic classification of BIM elements based on their textual descriptions in IFC files. The system assigns BIM elements to classes from multiple classification dictionaries supported by bSDD (including CCI, Uniclass, and others) by leveraging semantic embeddings.

Instead of relying on supervised fine-tuning (which requires labeled datasets), the approach uses sentence-transformers to generate semantic embeddings of element descriptions and classification classes, comparing them via cosine similarity. This enables flexible, multi-dictionary classification without binding to a fixed label set.

The project also explores enhancing embeddings quality using TSDAE and few-shot learning techniques to improve classification accuracy.

## Key features
- automatic extraction and parsing of textual descriptions from IFC files
- embedding generation of BIM element descriptions and class labels using multilingual sentence-transformers
- semantic similarity matching across multiple classification dictionaries (CCI, Uniclass, etc.)
- optional fine-tuning via TSDAE and few-shot learning to boost accuracy
- evaluation using top-k accuracy, cosine similarity scores, F1-score and other metrics
- export of classification results compatible with BIMVision via JSON/CSV format for seamless integration
- modular pipeline designed for extensibility and further dictionary additions

## Technologies & Tools
- **Language:** Python 3.10+
- **NLP:** sentence-transformers (paraphrase-multilingual-MiniLM), PyTorch, TSDAE
- **Data processing:** pandas, numpy, matplotlib
- **APIs:** bSDD REST API or local dictionary files
- **Evaluation metrics:** cosine similarity, top-k accuracy, F1-score
- **Formats:** JSON/CSV(?) for data exchange with BIMVision (C# interface)
- **Development:** Jupyter Notebook, Git, VSCode

## Usage

*Instructions for setting up, running the classification pipeline, and using the model will be added here once the implementation is complete.*

## Results and Evaluation

*This section will include quantitative evaluation metrics (accuracy, F1-score, similarity scores) and qualitative analysis of classification results once available.*

## Disclaimer
This project was developed as part of an internship at Datacomp IT in Kraków, Poland. The work presented here reflects the scope and objectives of the internship and is intended for educational and prototypical purposes.
