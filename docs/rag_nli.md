# RAG + NLI Pipeline Method

## Overview

The **RAG + NLI** pipeline enhances traditional Retrieval-Augmented Generation by introducing a Natural Language Inference (NLI) filtering layer. This method reduces retrieval noise by keeping only passages that logically support the answer claim, leading to more accurate and grounded responses.

## How It Works

The pipeline operates in three main stages:

### 1. Dense Retrieval (FAISS)
A user question is sent to a dense retriever (FAISS-based), which returns the top-k most semantically similar passages from the knowledge base.

### 2. Claim Generation
From the question, a **claim** (hypothesis) is derived. Rather than formulating a direct answer, the claim expresses the **existence of information** needed to answer the question.

**Example:**
- **Question:** "Who is the president of France?"
- **Derived Claim:** "There exists information about who is the president of France."

### 3. NLI Filtering
The NLI model evaluates each retrieved passage against the claim:
- **Premises:** Retrieved passages from FAISS
- **Hypothesis:** The derived claim
- **Output:** Entailment, Contradiction, or Neutral

Only passages labeled as **Entailment** (i.e., passages that logically support the claim) are kept for generation.

### 4. Answer Generation
The filtered passages are used as context for the language model to generate a final answer.

## Pipeline Flow Diagram

```
┌─────────────────┐
│  User Question  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Dense Retriever (FAISS)│
│  Retrieve top-k passages│
└────────┬────────────────┘
         │
         ├──────────────────────────────┐
         │                              │
         ▼                              ▼
┌─────────────────┐          ┌──────────────────┐
│ Claim Generation│          │Retrieved Passages│
│ (from question) │          │ [P1, P2, ..., Pk]│
└────────┬────────┘          └─────────┬────────┘
         │                              │
         │         ┌────────────────────┘
         │         │
         ▼         ▼
    ┌─────────────────────┐
    │   NLI Model         │
    │ Hypothesis: Claim   │
    │ Premises: Passages  │
    └─────────┬───────────┘
              │
              ▼
    ┌──────────────────────┐
    │  Filter by Entailment│
    │  Keep only passages  │
    │  that support claim  │
    └─────────┬────────────┘
              │
              ▼
    ┌──────────────────────┐
    │ Filtered Passages    │
    │ [Entailment only]    │
    └─────────┬────────────┘
              │
              ▼
    ┌──────────────────────┐
    │ Answer Generation    │
    │ (LLM with context)   │
    └─────────┬────────────┘
              │
              ▼
    ┌──────────────────────┐
    │   Final Answer       │
    └──────────────────────┘
```

## Fallback Mechanism

If the NLI model returns **no passages with entailment** (all passages are labeled as Contradiction or Neutral), the system falls back to using the **original retrieved passages** from FAISS to avoid returning an empty context.

This ensures robustness while still benefiting from NLI filtering when relevant passages are available.

## Example Walkthrough

### Question
*"What is the capital of Japan?"*

### Step 1: Retrieval
FAISS retrieves the following passages:
1. "Tokyo is the capital and largest city of Japan."
2. "Japan is an island nation in East Asia."
3. "Osaka is a major city in Japan known for its cuisine."
4. "The capital of South Korea is Seoul."

### Step 2: Claim Generation
**Claim:** "Tokyo is the capital of Japan."

### Step 3: NLI Filtering
| Passage | NLI Label | Kept? |
|---------|-----------|-------|
| Passage 1: "Tokyo is the capital and largest city of Japan." | **Entailment** | ✅ Yes |
| Passage 2: "Japan is an island nation in East Asia." | Neutral | ❌ No |
| Passage 3: "Osaka is a major city in Japan known for its cuisine." | Neutral | ❌ No |
| Passage 4: "The capital of South Korea is Seoul." | Contradiction | ❌ No |

### Step 4: Generation
**Filtered Passages:** Only Passage 1 is used as context.

**Final Answer:** "Tokyo is the capital of Japan."

## Key Benefits

✅ **Reduces retrieval noise:** Irrelevant or contradictory passages are filtered out  
✅ **Improves answer grounding:** Only logically supporting evidence is used  
✅ **Maintains efficiency:** NLI filtering is fast and adds minimal overhead  
✅ **Preserves robustness:** Fallback mechanism ensures context is always available

## Limitations

- Works best for **factual, single-entity questions**
- Struggles with **comparative** or **disjunctive** questions (e.g., "Who is taller, X or Y?")
- Claim generation quality depends on the question formulation
- NLI models may misclassify nuanced or ambiguous passages

**Solution:** For complex questions, see the [RAG + NLI + Sub-Claims](./rag_nli_subclaim.md) method.