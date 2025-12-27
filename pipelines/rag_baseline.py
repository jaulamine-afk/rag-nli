from rag.retriever import BasicRetriever
from rag.generator import Generator
from rag.prompt import create_prompt
from pipelines.base import BasicBaseline


class RAGBaseline(BasicBaseline):
    """
    Baseline RAG pipeline.

    This pipeline retrieves relevant passages for a question
    and directly generates an answer without any entailment
    or reasoning-based filtering.
    """

    def __init__(self, retriever: BasicRetriever, generator: Generator, top_k=2):
        self.retriever = retriever
        self.top_k = top_k
        self.generator = generator

    def answer(self, question, claim=""):
        """
        Generate an answer using standard RAG without NLI.
        The claim parameter is ignored but kept for API consistency.
        """
        passages = self.retriever.retriever_chunk(question, self.top_k)
        prompt = create_prompt(question, passages)
        return self.generator.generate_answer(prompt)

    def answer_for_agent(self, question, claim=""):
        """
        Return intermediate retrieval results for analysis and comparison.
        """
        passages = self.retriever.retriever_chunk(question, self.top_k)
        prompt = create_prompt(question, passages)
        answer = self.generator.generate_answer(prompt)

        return passages, answer
