from rag.retriever import BasicRetriever
from rag.generator import Generator
from rag.prompt import create_prompt
from pipelines.base import BasicBaseline
from nli.nli_class import NLIModel


class RAG_NLI(BasicBaseline):
    """
    RAG pipeline enhanced with NLI-based passage filtering.

    Retrieved passages are filtered based on whether they
    entail the full claim before answer generation.
    """

    def __init__(self, retriever: BasicRetriever, generator: Generator, nli_model: NLIModel, top_k=2):
        self.retriever = retriever
        self.top_k = top_k
        self.nli_model = nli_model
        self.generator = generator

    def answer(self, question, claim=""):
        """
        Generate an answer after filtering retrieved passages
        using NLI entailment against the full claim.
        """
        passages = self.retriever.retriever_chunk(question, self.top_k)
        filtered_passages = self.nli_model.nli_passage_basic(claim, passages)
        prompt = create_prompt(question, filtered_passages)

        return self.generator.generate_answer(prompt)
