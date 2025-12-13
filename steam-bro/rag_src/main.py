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

    def ask_query(self,query):
        embedq = embed(list(query))
        topk = self.store.query(embedq)
        prompt = self._build_prompt(query , topk)
        answer = self.llm.ask_gemini(prompt)
        print(answer)
        return answer









    def _build_prompt(self,query , top_k_embeds):
        
        prompt = "I am performing a rag based applicaiton and you are my llm agent i will provide what is the user query or question " \
         "and i will also provide you the related content which performed with embedding and getting top k related data" \
         "the user basically upload his whatsapp chat it may be group or personal chat and he/she will ask the question" \
         "so that we have to reply the answer so that user should highly satisfied and even if you don' get you say entertain the user " \
         "without giving the wrong information" \
         "you have to give a small simple answer i will directly provide the user and your answer should not include any thinking jsut a reply to user should here" \
         "don't even say i see history , i have did this , did that don't never expose the internal llm things just give the answer for quesiton and abstract the process" \
         f"here i am attaching the query =  {query} emeddings = {top_k_embeds}"
        
        return prompt
