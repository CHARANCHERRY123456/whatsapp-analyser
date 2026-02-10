from .chunking.time_slicer import TimeSlicer
from .embeding import embed
from .slice_text import slice_text
from .store import ChromaStore
from .llm import Gemini
class RAG:
    def __init__(self , data):
        self.data = data
        self.tf = TimeSlicer()
        self.slices = self.tf.slice(self.data)
        texts = slice_text(self.slices)
        self.llm = Gemini()
        self.metadatas = [{
            "source": f"slice_{i}",
            "start_time": str(self.slices[i][0][2]),
            "text": texts[i],
        } for i in range(len(texts))]

        self.embeddings = embed(texts)

        self.store = ChromaStore()
        self.store.add_embeddings(self.embeddings ,self.metadatas)

    def ask_query(self, query):
        """
        Embed the full query string once and send a single 1D embedding vector
        (list of floats) to ChromaDB.
        """
        # embed() expects a list[str]; it returns a 2D array: shape (1, D)
        query_embeddings = embed([query])

        # Take the first (and only) embedding: shape (D,)
        query_embedding = query_embeddings[0]

        # If it's a numpy array, convert to a plain Python list[float]
        if hasattr(query_embedding, "tolist"):
            query_embedding = query_embedding.tolist()

        # Now pass a single embedding vector to the store
        topk = self.store.query(query_embedding)
        prompt = self._build_prompt(query, topk)
        answer = self.llm.ask_gemini(prompt)
        return answer









    def _build_prompt(self, query, top_k_results):
        """
        Build prompt with retrieved context from ChromaDB.
        Extract actual text content from the retrieved chunks.
        """
        # Extract text content from retrieved chunks
        # ChromaDB returns: {'ids': [[...]], 'metadatas': [[{...}]], 'documents': [[...]], 'distances': [[...]]}
        retrieved_contexts = []
        
        # Try to get text from metadatas first (we stored it there)
        if top_k_results and 'metadatas' in top_k_results and top_k_results['metadatas']:
            for metadata_list in top_k_results['metadatas']:
                if metadata_list:  # Check if list is not empty
                    for metadata in metadata_list:
                        if isinstance(metadata, dict) and 'text' in metadata:
                            retrieved_contexts.append(metadata['text'])
        
        # If no text in metadatas, try documents field
        if not retrieved_contexts and top_k_results and 'documents' in top_k_results and top_k_results['documents']:
            for doc_list in top_k_results['documents']:
                if doc_list:
                    retrieved_contexts.extend(doc_list)
        
        # Format the retrieved contexts
        if retrieved_contexts:
            context_text = "\n\n---\n\n".join(retrieved_contexts[:5])  # Limit to top 5 chunks
        else:
            context_text = "No relevant context found in the chat history."
        
        prompt = f"""You are an AI assistant helping users understand their WhatsApp chat history.

User Question: {query}

Relevant Chat Context (retrieved from chat history):
{context_text}

Instructions:
- Answer the user's question based ONLY on the provided chat context above
- If the context doesn't contain relevant information, say "I couldn't find that information in the chat history"
- Give a clear, concise answer without mentioning that you're using RAG or embeddings
- Don't make up information that's not in the context
- Keep your answer natural and conversational

Answer:"""
        
        return prompt
