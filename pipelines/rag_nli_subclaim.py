from rag.retriever import BasicRetriever
from rag.generator import Generator
from rag.prompt import create_prompt
from pipelines.base import BasicBaseline
from nli.nli_class import NLIModel
from nli.subclaim import decompose_comparative_claim, is_comparative_claim


class RAG_NLI_Subclaim(BasicBaseline):
    """
    RAG pipeline with NLI-based filtering and claim decomposition.

    Complex claims (comparative or disjunctive) are decomposed
    into sub-claims, which are verified independently using NLI.
    """

    def __init__(
        self,
        retriever: BasicRetriever,
        generator: Generator,
        nli_model: NLIModel,
        top_k=2
    ):
        self.retriever = retriever
        self.top_k = top_k
        self.nli_model = nli_model
        self.generator = generator

    def answer(self, question, claim=""):
        """
        Generate an answer after filtering retrieved passages
        using sub-claim-level NLI entailment.
        """
        passages = self.retriever.retriever_chunk(question, self.top_k)
        filtered_passages = self.nli_model.nli_passage_subclaim(claim, passages)
        prompt = create_prompt(question, filtered_passages)

        return self.generator.generate_answer(prompt)

    def answer_for_agent(self, question, claim=""):
        """
        Extended version used for analysis and visualization.

        Returns:
        - decomposed sub-claims
        - original retrieved passages
        - NLI-filtered passages
        - final generated answer
        """
        if is_comparative_claim(claim):
            subclaims = decompose_comparative_claim(claim)
        else:
            subclaims = [claim]

        passages_rag = self.retriever.retriever_chunk(question, self.top_k)
        filtered_passages = self.nli_model.nli_passage_subclaim(claim, passages_rag)
        prompt = create_prompt(question, filtered_passages)
        answer = self.generator.generate_answer(prompt)

        return subclaims, passages_rag, filtered_passages, answer
