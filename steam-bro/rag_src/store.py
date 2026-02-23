import chromadb
class ChromaStore:
    def __init__(self) -> None:
        self.client = chromadb.Client()
        # Use get_or_create_collection to avoid errors if collection already exists
        try:
            self.col = self.client.get_collection(name="documents")
            # Clear existing collection if it exists (optional - remove if you want to keep old data)
            self.client.delete_collection(name="documents")
            self.col = self.client.create_collection(name="documents")
        except:
            # Collection doesn't exist, create it
            self.col = self.client.create_collection(name="documents")
    def add_embeddings(self, embeddings, metadatas=None):
        # Extract documents from metadatas for better retrieval
        documents = None
        if metadatas:
            documents = [meta.get('text', '') for meta in metadatas]
        
        self.col.add(
            ids=list(map(str, range(len(embeddings)))),
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents  # Store documents for easier retrieval
        )
    def query(self, embedding, n_results=5):
        results = self.col.query(
            query_embeddings=[embedding],
            n_results=n_results
        )
        return results