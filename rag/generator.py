from transformers import T5Tokenizer, T5ForConditionalGeneration, AutoTokenizer, AutoModelForSeq2SeqLM
from .prompt import create_prompt


class Generator():
    """
    
    Initialize the model 

    and Generate an answer

    """

    def __init__(self, model_name = "google/flan-t5-small"):
        """
        Load the appropriate tokenizer and model depending on architecture.
        """
        if model_name == "allenai/unifiedqa-t5-small": 
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.gen_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        else : 
            self.tokenizer = T5Tokenizer.from_pretrained(model_name)
            self.gen_model = T5ForConditionalGeneration.from_pretrained(model_name)

    def generate_answer(self, prompt):
        prompt = prompt
        inputs = self.tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = self.gen_model.generate(**inputs, max_new_tokens=100)
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return answer


