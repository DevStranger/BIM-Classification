## Goals
The goal of the project is to compare the effectiveness of IFC element classification using:

- Baseline: sentence-transformers (paraphrase-multilingual-MiniLM) + cosine similarity
- TSDAE: pretraining a denoising autoencoder on IFC descriptions + embeddings
- Few-shot fine-tuning: slight model adaptation using manually labeled data

The project is exploratory in nature and aims to deliver:
- a functional classifier prototype (top-1 prediction of CCI/Uniclass code based on IFC description)
- quality analysis of results
- documentation of the methodology

## Evaluation Metrics

| Metric                | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| top-1 accuracy        | % of cases where the model assigned the correct CCI code                    |
| average cosine similarity | average similarity score of predictions                                   |
| coverage (above threshold) | % of predictions above a similarity threshold (e.g., 0.65)              |
| top-3 accuracy (optional) | whether the correct class is among the 3 nearest candidates               |

## Evaluation After Fine-tuning

- test data: 10–20 IFC descriptions with assigned CCI codes (ground truth)
- accuracy analysis:
  - comparison of baseline vs TSDAE/few-shot results
  - analysis of correct / incorrect predictions (false positives)
- similarity analysis: similarity distribution, TSNE visualization

## TSDAE Training Plan

1) prepare input data (IFC texts)
2) generate "noisy" data (e.g., word masking, reordering, deletion)
3) train TSDAE (sentence-transformers: DenoisingAutoEncoder)
4) save model + evaluate embeddings

## Few-shot Fine-tuning

1) prepare 20–50 IFC descriptions with CCI codes (manual annotation)
2) fine-tune model (e.g., transformers.Trainer, sentence-transformers.fit())
3) evaluate on test set

## Result Documentation
- save baseline vs fine-tuned predictions (JSON, CSV)
- compare metrics
- visualize similarities
- integrate with IFC file (optional, in the final week)
