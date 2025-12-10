import chromadb
class ChromaStore:
    def __init__(self) -> None:
        self.client = chromadb.Client()
        self.col = self.client.create_collection(name="documents")
    def add_embeddings(self, embeddings, metadatas=None):
        self.col.add(
            ids = list(map(str, range(len(embeddings)))),
            embeddings=embeddings,
            metadatas=metadatas
        )
    def query(self, embedding, n_results=5):
        results = self.col.query(
            query_embeddings=[embedding],
            n_results=n_results
        )
        return results