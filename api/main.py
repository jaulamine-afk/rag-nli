import pickle

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag.retriever import BasicRetriever
from rag.generator import Generator
from nli.nli_class import NLIModel
from pipelines.rag_baseline import RAGBaseline
from pipelines.rag_nli_subclaim import RAG_NLI_Subclaim
from agents.analysis_agent import AgentAnalysis



app = FastAPI()

# Allow cross-origin requests from the frontend (development setup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

QA_DATA = [
    {
        "id": 0,
        "question": "Are the Laleli Mosque and Esma Sultan Mansion located in the same neighborhood?",
        "claim": "The Laleli Mosque and Esma Sultan Mansion are located in the same neighborhood.",
        "good_answer": "no"
    },
    {
        "id": 1,
        "question": "Who is older, Annie Morton or Terry Richardson?",
        "claim": "One of Annie Morton or Terry Richardson is older than the other.",
        "good_answer": "Terry Richardson"
    },
    {
        "id": 2,
        "question": "What is the name of the singer who's song was released as the lead single from the album \"Confessions\", and that had popular song stuck behind for eight consecutive weeks?",
        "claim": "There exists a singer whose song was the lead single from Confessions.",
        "good_answer": "Usher"
    },
    {
        "id": 3,
        "question": "What race track in the midwest hosts a 500 mile race eavery May?",
        "claim": "There exists a midwest race track hosting a 500 mile race every May.",
        "good_answer": "Indianapolis Motor Speedway"
    },
]

# Global initialization to avoid reloading heavy models on each request
print("Initializing models and pipelines...")

with open("data/hotpotqa_300.pkl", "rb") as f:
    dataset = pickle.load(f)

retriever = BasicRetriever(dataset)
nli_model = NLIModel()
generator = Generator(model_name="google/flan-t5-small")

rag_pipeline = RAGBaseline(retriever, generator, top_k=2)
rag_nli_pipeline = RAG_NLI_Subclaim(retriever, generator, nli_model, top_k=2)

analyzer = AgentAnalysis()

print("Initialization completed")

class QuestionRequest(BaseModel):
    question_id: int

@app.get("/")
async def root():
    return FileResponse("static/index.html", media_type="text/html")

@app.get("/api/questions")
async def get_questions():
    return {
        "questions": [
            {
                "id": qa["id"],
                "question": qa["question"],
                "claim": qa["claim"]
            }
            for qa in QA_DATA
        ]
    }

@app.post("/api/analyze")
async def analyze_question(request: QuestionRequest):
    """
    Runs both RAG and RAG+NLI pipelines and returns a comparative analysis.
    """
    try:
        qa = next(
            (q for q in QA_DATA if q["id"] == request.question_id),
            None
        )

        if qa is None:
            return {
                "success": False,
                "error": f"Question ID {request.question_id} not found"
            }

        question = qa["question"]
        claim = qa["claim"]
        good_answer = qa["good_answer"]

        rag_passages, rag_answer = rag_pipeline.answer_for_agent(question)
        print(rag_answer)

        (
            subclaims,
            passages_before_nli,
            nli_passages,
            nli_answer
        ) = rag_nli_pipeline.answer_for_agent(question, claim)

        analysis_text = analyzer.analyze(
            question=question,
            claim=claim,
            rag_passages=rag_passages,
            rag_answer=rag_answer,
            subclaims=subclaims,
            nli_passages=nli_passages,
            nli_answer=nli_answer,
            good_answer=good_answer
        )

        return {
            "success": True,
            "question": question,
            "claim": claim,
            "good_answer": good_answer,
            "rag": {
                "passages_count": len(rag_passages) if isinstance(rag_passages, list) else 0,
                "passages": rag_passages if isinstance(rag_passages, list) else [rag_passages],
                "answer": rag_answer
            },
            "rag_nli": {
                "subclaims": subclaims,
                "passages_before": len(passages_before_nli) if isinstance(passages_before_nli, list) else 1,
                "passages_after": len(nli_passages) if isinstance(nli_passages, list) else 0,
                "passages": nli_passages if isinstance(nli_passages, list) else [nli_passages],
                "answer": nli_answer
            },
            "analysis": analysis_text
        }

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
