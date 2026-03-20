import os
from pydoc import text

from google import genai
from pinecone import Pinecone
from dotenv import load_dotenv
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(_project_root / ".env")


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class GeminiPineconeVectorStore:
    def __init__(self , index_name = "whatsapp-analyser") -> None:
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.genai = genai.Client(api_key=GEMINI_API_KEY)
        self.pc.delete_index(index_name)
        self.pc.create_index(
            name=index_name,
            dimension=3072,
            metric="cosine",
            spec={"serverless": {"cloud": "aws", "region": "us-east-1"}}
        )
        self.index = self.pc.Index(index_name)
    
    def embed(self, texts : list):
        not_morethan_100_texts = [texts[start : start + 100] for start in range(0 , len(texts) , 100)]
        result_vectors = []
        for sized_chuncks in not_morethan_100_texts:
            res = self.genai.models.embed_content(
                model="models/gemini-embedding-001",
                contents=sized_chuncks
            )
            result_vectors.extend(res.embeddings)
        return result_vectors
    def upsert(self , texts):
        '''Takes list of Text values to insert in the index'''
        embeds = self.embed(texts)
        vectors = []
        for i , emb in enumerate(embeds):
            vectors.append({
                "id" : str(i),
                "values" : emb.values,
                "metadata" : {"text" : texts[i]}
            })

        return self.index.upsert(vectors)

    def query(self , text , top_k=10):
        '''sent a text object and it will return the top_k(5) most relavent embeddings'''
        [embed] = self.embed([text])

        return self.index.query(
            vector=embed.values,
            top_k=top_k,
            include_metadata=True
        )