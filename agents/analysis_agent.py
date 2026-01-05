from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv


class AgentAnalysis:
    """
    Single analysis agent that compares:
    - RAG baseline
    - RAG + NLI with subclaim decomposition

    The goal is to explain clearly WHY one answer is more reliable than the other.
    """
    def __init__(self):
        # Load API key
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dotenv_path = os.path.join(BASE_DIR, ".env")
        
        load_dotenv(dotenv_path)
        print("ok ça marche")
        self.model = init_chat_model(
            "gemini-2.5-flash",
            model_provider="google_genai"
    )

    def analyze(
        self,
        question: str,
        claim: str,
        rag_passages: list[str],
        rag_answer: str,
        subclaims: list[str],
        nli_passages: list[str],
        nli_answer: str,
        good_answer : str
    ) -> str:
        """
        Compare RAG vs RAG + NLI Subclaim results and explain differences.
        """

        prompt = (
            f"Answer in english. Keep your response SHORT and CONCISE (max 200 words). NO markdown formatting (no **, ##).\n"
            f"You are analyzing two question-answering systems.\n\n"

            f"The original question is:\n"
            f"{question}\n\n"

            f"The factual claim used for NLI is:\n"
            f"{claim}\n\n"

            f"First system: RAG without NLI.\n"
            f"It retrieved the following passages:\n"
            f"{rag_passages}\n\n"
            f"It produced this answer:\n"
            f"{rag_answer}\n\n"

            f"Second system: RAG with NLI and subclaim decomposition.\n"
            f"The claim was decomposed into these subclaims:\n"
            f"{subclaims}\n\n"
            f"After NLI filtering, it kept these passages:\n"
            f"{nli_passages}\n\n"
            f"It produced this answer:\n"
            f"{nli_answer}\n\n"

            f"The correct answer is: {good_answer}\n\n"

            f"Now explain in clear and simple terms:\n"
            f"1. Which answer is more reliable and why\n"
            f"2. How subclaims and NLI filtering affected the result\n"
            f"3. Whether irrelevant information was reduced\n\n"
            f"Be concise and direct."
        )

        response = self.model.invoke(
            [{"role": "user", "content": prompt}]
        )

        return response.content.strip()
