def create_prompt(question,retrieved_chunks):
    
    context = "\n".join(retrieved_chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    return prompt 