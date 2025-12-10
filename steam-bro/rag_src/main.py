from .chunking.time_slicer import TimeSlicer
from .embeding import embed
from .slice_text import slice_text
from .store import ChromaStore
class RAG:
    def __init__(self , data):
        self.data = data
        self.tf = TimeSlicer()
        self.slices = self.tf.slice(self.data)
        texts = slice_text(self.slices)
        self.metadatas = [{
            "source": f"slice_{i}",
            "start_time": str(self.slices[i][0][2]),
            "text": texts[i],
        } for i in range(len(texts))]

        self.embeddings = embed(texts)

        self.store = ChromaStore()
        self.store.add_embeddings(self.embeddings ,self.metadatas)

