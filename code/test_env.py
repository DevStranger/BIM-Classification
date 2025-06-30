from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
embedding = model.encode("Testing testing <3")
print(embedding.shape)

