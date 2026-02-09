# RAG with NLI and Sub-Claim Decomposition

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)](https://www.docker.com/)
[![AWS](https://img.shields.io/badge/AWS-Deployed-FF9900)](https://aws.amazon.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)



Retrieval-Augmented Generation system that filters out irrelevant information before answer generation, delivering more accurate and trustworthy AI responses.

**Use cases:** Customer support, legal document analysis, technical documentation search, compliance verification

---

## Why This Matters

Standard chatbots and Q&A systems often suffer from critical issues:

- ❌ **Hallucinations** - Give confident but incorrect answers
- ❌ **Information noise** - Mix relevant and irrelevant content
- ❌ **Complex question failures** - Struggle with multi-part questions

**This system solves these problems by:**

- ✅ Filtering out noise before generating answers (demonstrated improvements in accuracy)
- ✅ Validating each piece of information independently
- ✅ Handling complex questions requiring multiple sources

**Real-world impact:**
- Reduced customer support errors and response time
- Faster document review for legal and compliance teams
- More reliable knowledge base search
- Lower operational costs from fewer incorrect answers

---

## Key Applications

| Domain | Main Impact |
|--------|-------------|
| 📞 Customer Support | Faster ticket resolution, more reliable answers |
| ⚖️ Legal & Compliance | Quicker document analysis, reduced legal risk |
| 📚 Technical Documentation | Better developer experience, lower support load |
| 🏥 Healthcare Information | Safer and more trustworthy information |


## Approach Overview

Three pipelines are implemented and compared:

**RAG Baseline:** Dense retrieval (FAISS) + prompt-based generation

**RAG + NLI:** Filters retrieved passages using NLI to keep only those that entail the claim ([details](docs/rag_nli.md))

**RAG + NLI + Sub-Claims:** Decomposes complex claims into sub-claims, validates each independently ([details](docs/rag_nli_subclaim.md))

## System Architecture

The diagram below illustrates the main pipeline (**RAG + NLI + Sub-Claims**). It details how complex queries are decomposed and how the NLI model acts as a semantic gatekeeper to filter out noise before generation.

<p align="center">
  <img src="docs/images/Graph_rag_nli_sub.png" alt="RAG with NLI Architecture" width="600">
  <br>
  <em>(Figure: Workflow of Sub-Claim Decomposition and NLI Entailment Filtering)</em>
</p>

## Evaluation

Experiments were conducted on HotpotQA (distractor setting).

**Metrics used:**

- Exact Match
- F1
- BERTScore (Precision / Recall / F1)

| Metric | Improvement vs Baseline |
|--------|-------------------------|
| **Answer Accuracy (Exact Match)** | **+16%** |
| **Answer Quality (F1 Score)** | **+10%** |

**Key results:**  
With our most advanced pipeline (**RAG + NLI + Sub-Claims**) we observed up to **+16% improvement in Exact Match** and **+10% in F1** compared to a standard RAG baseline, depending on the model and Top-K configuration.


📈 [View detailed evaluation results](docs/evaluations.md)

---

## Analysis Agent

Built-in debugging agent powered by Gemini that explains pipeline decisions in plain language.

**Example Analysis:**

**1. Comparing Results:**

<p align="center">
  <img src="docs/images/Agent_compare.png" alt="Comparison RAG vs NLI" width="600">
</p>

The agent shows how the baseline fails (hallucination) while the filtered system succeeds.

**2. Understanding Why:**

<p align="center">
  <img src="docs/images/Agent_analysis.png" alt="Agent Logic Analysis" width="600">
</p>

The agent explains the NLI module successfully filtered out the "distractor" passage about Rihanna because it didn't entail the claim about Usher's album "Confessions".

*This agent helps during development to analyze pipeline decisions, compare baseline vs filtered outputs, and provides actionable insights for system tuning.*

---

## Project Structure

```
rag-nli/
│
├── rag/                 # Retrieval & generation
├── nli/                 # NLI model and filtering logic
├── pipelines/           # RAG / RAG+NLI / RAG+NLI+Subclaim
├── evaluation/          # Metrics and experiments
├── agents/              # Analysis agent
├── api/                 # FastAPI service
├── scripts/             # Experiment runners
├── data/
├── docs/
└── Dockerfile
└── README.md

```

## Running the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run experiments

```bash
python -m scripts.run_experiments
```

This will run all pipelines on a subset of HotpotQA and output evaluation metrics.

### 3. Run the API

The project exposes a FastAPI service for question answering.

```bash
python -m uvicorn api.main:app --host 127.0.0.1 --port 8001
```

## API Key Configuration (Gemini)

Some components (analysis agent) use Gemini 2.5 Flash-lite.

1. Generate an API key here:
   [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

2. Create a file named `.env` at the root of the project.

3. Add your key inside the `.env` file:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   


## Optional: Docker Deployment

The project can also be containerized using Docker for easier deployment and reproducibility.

A Dockerfile is provided to:

- install dependencies,
- expose the FastAPI service,
- run the application in a reproducible environment.

**Example commands:**

```bash
docker build -t rag-nli-app .
docker run -p 8001:8001 rag-nli-app
```

This setup was tested locally and deployed on an AWS EC2 (Ubuntu) instance.

## Limitations

- Sub-claim decomposition is rule-based and heuristic
- Not all claims in HotpotQA are decomposable
- No statistical significance testing (CPU-only setup)
- Focus is on retrieval noise reduction, not full hallucination prevention

These limitations are discussed transparently to emphasize realism and reproducibility.

## Technologies

- Python
- Hugging Face
- FAISS
- FastAPI
- LangChain / LangGraph
- Docker
- AWS
- Gemini (Google GenAI)

## References

[1] Lu Dai, Hao Liu, Hui Xiong. "Improve Dense Passage Retrieval with Entailment Tuning." The Hong Kong University of Science and Technology, 2024.

[2] Ori Yoran, et al. "Making Retrieval-Augmented Language Models Robust to Irrelevant Context." ICLR, 2024. (Foundational work on noise filtration in RAG).

[3] Akari Asai, et al. "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection." ICLR, 2024. (Context regarding self-correction and claim support).

[4] Shahul Es, et al. "RAGAS: Automated Evaluation of Retrieval Augmented Generation." EACL, 2024. (Framework used for defining Faithfulness metrics via NLI).

[5] Nelson F. Liu, et al. "Lost in the Middle: How Language Models Use Long Contexts." TACL, 2024. (Highlights the necessity of filtering to avoid performance degradation in long contexts).
