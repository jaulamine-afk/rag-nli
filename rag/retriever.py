import faiss
from sentence_transformers import SentenceTransformer
import numpy as np 
from datasets import load_dataset



class BasicRetriever : 
    """
    FAISS-based dense retriever for RAG.
    """

    def __init__(self, dataset):
        self.chunks = self.to_chunks(dataset)
        self.model_for_rag = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = self.encode_chunk()

    def to_chunks(self, dataset, ls = []):
        """
        Function for transforming hotpot_qa context to chunks.
        """
        for i in range(0,300):
            for j in range(len(dataset[i]['context']['sentences'])):
                sentences = " ".join(dataset[i]['context']['sentences'][j])
                ls.append(sentences)
        return ls
    
    def encode_chunk(self):
        
        embeddings = self.model_for_rag.encode(self.chunks, convert_to_numpy=True)
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)

        return index
    
    def retriever_chunk(self, query, top_k = 2):
        
        query_e = self.model_for_rag.encode([query], convert_to_numpy=True)
        query_e = query_e / np.linalg.norm(query_e, axis=1, keepdims=True)

        dis,ind = self.index.search(query_e,top_k)
        retrieve_chunks = [self.chunks[ind_passage] for ind_passage in ind[0]]

        return retrieve_chunks
        
    


