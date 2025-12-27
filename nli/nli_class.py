from transformers import AutoModelForSequenceClassification, AutoTokenizer
from nli.subclaim import is_comparative_claim, decompose_comparative_claim
import torch


class NLIModel:
    """
    Wrapper around a Natural Language Inference (NLI) model.

    This class is used to filter retrieved passages by checking
    whether they entail a given claim or its decomposed sub-claims.
    """

    def __init__(self):
        """
        Load a pretrained NLI model and tokenizer once,
        to avoid repeated initialization during inference.
        """
        model_name = "facebook/bart-large-mnli"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

    def nli_output(self, premise: str, hypothesis: str):
        """
        Run NLI inference between a premise and a hypothesis.

        Returns:
            predicted_label (int):
                0 = contradiction, 1 = neutral, 2 = entailment
            predicted_score (float):
                Confidence score for the predicted label.
        """
        inputs = self.tokenizer(
            premise,
            hypothesis,
            return_tensors="pt",
            truncation=True,
            padding="longest"
        )

        # Disable gradient computation for inference
        with torch.no_grad():
            logits = self.model(**inputs).logits

        probs = torch.softmax(logits, dim=-1)[0]

        predicted_label = torch.argmax(probs).item()
        predicted_score = probs[predicted_label].item()

        return predicted_label, predicted_score

    def nli_passage_basic(self, claim, passages_rag, threshold=0.60):
        """
        Filter retrieved passages by keeping only those that
        strongly entail the full claim.

        If no passage passes the entailment threshold,
        the original passages are returned as a fallback.
        """
        entail_passages = []

        for premise in passages_rag:
            label, score = self.nli_output(premise, claim)
            if label == 2 and score > threshold:
                entail_passages.append(premise)

        return entail_passages if entail_passages else passages_rag

    def nli_passage_subclaim(self, claim, passages_rag, threshold=0.60):
        """
        Apply NLI-based filtering using claim decomposition.

        Comparative or conjunctive claims are split into sub-claims,
        which are verified independently against each passage.
        """
        entail_passages = []

        for premise in passages_rag:

            # Handle comparative or conjunctive claims via decomposition
            if is_comparative_claim(claim):
                sub_claims = decompose_comparative_claim(claim)

                for sub in sub_claims:
                    label, score = self.nli_output(premise, sub)
                    if label == 2 and score > threshold:
                        entail_passages.append(premise)

            # Handle standard (non-comparative) claims directly
            else:
                label, score = self.nli_output(premise, claim)
                if label == 2 and score > threshold:
                    entail_passages.append(premise)

        # Remove duplicates while preserving insertion order
        entail_passages = list(dict.fromkeys(entail_passages))

        return entail_passages if entail_passages else passages_rag
