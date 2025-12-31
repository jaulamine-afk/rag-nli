# RAG + NLI + Sub-Claims Pipeline Method

## Overview

The **RAG + NLI + Sub-Claims** pipeline extends the RAG + NLI approach to handle complex questions that involve **comparisons**, **disjunctions** (OR), or **conjunctions** (AND). By decomposing complex claims into simpler sub-claims, this method enables finer-grained NLI filtering and improves answer quality for multi-faceted questions.

## Motivation

The standard **RAG + NLI** pipeline struggles with questions like:
- *"Who is taller, Eiffel Tower or Big Ben?"* (Comparative)
- *"Is Paris the capital of France or Germany?"* (Disjunctive - OR)
- *"Did Einstein win a Nobel Prize and teach at Princeton?"* (Conjunctive - AND)

These questions cannot be easily verified as a single claim because they involve **multiple entities or conditions**. The NLI model may struggle to find passages that entail the entire complex claim at once.

**Solution:** Decompose the complex claim into **independent sub-claims**, validate each sub-claim separately, and aggregate the results.

## How It Works

### 1. Dense Retrieval (FAISS)
Same as RAG + NLI: the question is sent to FAISS, which retrieves top-k semantically similar passages.

### 2. Claim Analysis & Decomposition
The system analyzes the derived claim to detect if it contains:
- **Comparative structures** (e.g., "taller than", "bigger than")
- **Disjunctive operators** (OR)
- **Conjunctive operators** (AND)

If detected, the claim is **decomposed into sub-claims**.

If the claim is **not decomposable** (i.e., it's a simple factual question), the pipeline falls back to the standard **RAG + NLI** logic with a single claim.

**Example:**
- **Question:** "Who is older, Barack Obama or Donald Trump?"
- **Complex Claim:** "There exists information to compare the ages of Barack Obama and Donald Trump."
- **Sub-Claims:**
  1. "There exists information about Barack Obama's birth date."
  2. "There exists information about Donald Trump's birth date."

### 3. NLI Filtering per Sub-Claim
For each sub-claim:
- Use it as the **hypothesis**
- Use retrieved passages as **premises**
- Keep passages labeled as **Entailment**

A passage is retained if it supports **at least one sub-claim**.

### 4. Answer Generation
The filtered passages are aggregated and used as context for generating the final answer.

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
└────────┬────────┘          └──────────┬───────┘
         │                              │
         ▼                              │
┌──────────────────────┐                │
│ Claim Analysis       │                │
│ Is it comparative/   │                │
│ disjunctive/         │                │
│ conjunctive?         │                │
└────────┬─────────────┘                │
         │                              │
         ▼                              │
┌──────────────────────┐                │
│ Sub-Claim            │                │
│ Decomposition        │                │
│ [SC1, SC2, ..., SCn] │                │
└────────┬─────────────┘                │
         │                              │
         │         ┌────────────────────┘
         │         │
         ▼         ▼
    ┌──────────────────────────┐
    │ NLI Model (Per Sub-Claim)│
    │ For each SCi:            │
    │   Hypothesis: SCi        │
    │   Premises: Passages     │
    │   Keep if Entailment     │
    └─────────┬────────────────┘
              │
              ▼
    ┌──────────────────────────┐
    │ Aggregate Filtered       │
    │ Passages                 │
    │ (Union of all passages   │
    │ supporting any sub-claim)│
    └─────────┬────────────────┘
              │
              ▼
    ┌──────────────────────────┐
    │ Answer Generation        │
    │ (LLM with filtered       │
    │  context)                │
    └─────────┬────────────────┘
              │
              ▼
    ┌──────────────────────────┐
    │   Final Answer           │
    └──────────────────────────┘
```

## Fallback Mechanism

Just like RAG + NLI, if **no passages** are found with entailment for any sub-claim, the system falls back to using the **original FAISS-retrieved passages** to ensure context availability.

## Example Walkthrough

### Question
*"Which is larger, Tokyo or Paris?"*

### Step 1: Retrieval
FAISS retrieves:
1. "Tokyo has a population of approximately 14 million people."
2. "Paris is the capital of France with around 2.1 million inhabitants."
3. "Tokyo is the capital of Japan."
4. "The Eiffel Tower is located in Paris."

### Step 2: Claim Decomposition
**Original Claim:** "One of Tokyo or Paris is larger than the other."

**Detected:** Comparative structure → Decompose

**Sub-Claims:**
- SC1: "There exists information about Tokyo's size."
- SC2: "There exists information about Paris's size."

### Step 3: NLI Filtering

**For SC1: "There exists information about Tokyo's size"**

| Passage | NLI Label | Kept? |
|---------|-----------|-------|
| Passage 1 | **Entailment** | ✅ Yes |
| Passage 2 | Neutral | ❌ No |
| Passage 3 | Neutral | ❌ No |
| Passage 4 | Neutral | ❌ No |

**For SC2: "There exists information about Paris's size"**

| Passage | NLI Label | Kept? |
|---------|-----------|-------|
| Passage 1 | Neutral | ❌ No |
| Passage 2 | **Entailment** | ✅ Yes |
| Passage 3 | Neutral | ❌ No |
| Passage 4 | Neutral | ❌ No |

### Step 4: Aggregation
**Filtered Passages:** Passage 1 + Passage 2 (union of passages supporting any sub-claim)

### Step 5: Generation
**Final Answer:** "Tokyo is larger than Paris. Tokyo has a population of approximately 14 million, while Paris has around 2.1 million inhabitants."

## Key Insight: Existence-Based Sub-Claims

The sub-claim decomposition strategy focuses on verifying the **independent existence of information** rather than asserting specific facts. This approach:

 **Avoids presupposing answers:** We don't assume "Tokyo has 14 million people" — we only check if information about Tokyo's population exists  
 **Increases recall:** Passages that contain relevant information are more likely to entail existence claims  
 **Handles uncertainty better:** Works even when exact values vary across sources  
 **Validates information availability:** Ensures each component needed to answer the question has supporting evidence

For example:
- ❌ Assertive claim: "Barack Obama was born in 1961" (too specific, may fail if year is slightly wrong in passage)
- ✅ Existence claim: "There exists information about Barack Obama's birth date" (more robust, captures any birth date mention)

This technique is particularly effective for comparative and conjunctive questions where independent verification of each component is essential.

## Key Benefits

 **Handles complex questions:** Comparative, disjunctive, and conjunctive queries  
 **Finer-grained filtering:** Each sub-claim is validated independently  
 **Improved precision:** Eliminates passages irrelevant to all sub-claims  
 **Maintains coverage:** Union aggregation ensures relevant context for each aspect  
 **Better answer grounding:** Generated answers are supported by specific evidence per sub-claim

## When to Use This Method

Use **RAG + NLI + Sub-Claims** when questions involve:
- **Comparisons:** "Which is X, A or B?"
- **Disjunctions:** "Is X true or Y true?"
- **Conjunctions:** "Did X happen and Y happen?"
- **Multi-entity questions:** Questions requiring information about multiple entities

For simple, single-entity factual questions, the standard **RAG + NLI** method is sufficient and more efficient.

## Limitations

- **Decomposition quality:** Rule-based decomposition may fail for highly complex or ambiguous claims
- **Increased computational cost:** NLI must run multiple times (once per sub-claim)
- **Not all claims are decomposable:** Some complex questions cannot be easily split
- **Dependency handling:** Sub-claims are treated independently, which may miss interdependencies

## Comparison with RAG + NLI

| Aspect | RAG + NLI | RAG + NLI + Sub-Claims |
|--------|-----------|------------------------|
| **Best for** | Simple factual questions | Complex/comparative questions |
| **NLI calls** | 1 per passage | N per passage (N = # sub-claims) |
| **Claim handling** | Single claim | Multiple sub-claims |
| **Computational cost** | Lower | Higher |
| **Precision on complex questions** | Lower | Higher |
