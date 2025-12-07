from .chunking.time_slicer import TimeSlicer
from .embeding import embed
from .slice_text import slice_text
class RAG:
    def __init__(self , data):
        self.data = data
        self.tf = TimeSlicer()
        self.slices = self.tf.slice(self.data)
        print("number of slices : " , len(self.slices))
        texts = slice_text(self.slices)


        self.embeddings = embed(texts)
        print("Embeddings generated")


