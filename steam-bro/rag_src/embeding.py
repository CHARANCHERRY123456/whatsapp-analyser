from sentence_transformers import SentenceTransformer
def embed(texts):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(texts)
    return embeddings
