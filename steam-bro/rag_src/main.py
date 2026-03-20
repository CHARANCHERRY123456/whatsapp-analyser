from .chunking.time_slicer import TimeSlicer
from .embeding import embed
from .slice_text import slice_text
from .pinecone_gemini import GeminiPineconeVectorStore
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

        # self.embeddings = embed(texts)
        # self.store = ChromaStore()
        # self.store.add_embeddings(self.embeddings ,self.metadatas)


        self.pinecone_store = GeminiPineconeVectorStore()
        self.pinecone_store.upsert(texts)

    def ask_query(self, query):
        """
        Takes the query as a string object and return the answer in string 
        it uses pinecone store and gemini llm to generate final answer
        """

        # Now pass a single embedding vector to the store
        topk = self.pinecone_store.query(query , 10)
        prompt = self._build_prompt(query, topk)
        answer = self.llm.ask_gemini(prompt)
        return answer









    def _build_prompt(self, query, top_k_results):
        """Build prompt from Pinecone query result (matches with metadata.text)."""
        matches = getattr(top_k_results, "matches", []) or []
        contexts = []
        for m in matches:
            meta = getattr(m, "metadata", None)
            text = meta.get("text") if isinstance(meta, dict) else getattr(meta, "text", None)
            if text:
                contexts.append(text)
        context_text = "\n\n---\n\n".join(contexts[:5]) if contexts else "No relevant context found in the chat history."

        return f"""You are an AI assistant helping users understand their WhatsApp chat history.

User Question: {query}

Relevant Chat Context (retrieved from chat history):
{context_text}

Instructions:
- Answer based ONLY on the chat context above. If not found, say "I couldn't find that in the chat history."
- Be concise and conversational. Don't make up information.

Answer:"""
