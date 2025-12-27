from evaluation.metrics import exact_match, f1_score, compute_bertscore_batch


def evaluate_pipeline(pipeline, dataset, claims=[]):
    """
    Evaluate a QA pipeline on a fixed-size subset of the dataset using
    Exact Match, F1, and BERTScore.

    If claims are provided, the pipeline is assumed to require a claim
    as additional input (e.g. NLI-based pipelines).
    """
    em = 0
    f1 = 0
    size = 100  # Fixed evaluation size for fair comparison across pipelines

    all_answers = []
    all_gold_answers = []

    # Case where the pipeline expects both question and claim
    if len(claims) != 0:
        for n in range(size):
            answer = pipeline.answer(
                dataset[n]["question"],
                claims[n]
            )
            gold_answer = dataset[n]["answer"]

            em += exact_match(answer, gold_answer)
            f1 += f1_score(answer, gold_answer)

            all_answers.append(answer)
            all_gold_answers.append(gold_answer)

    # Case where the pipeline only needs the question
    else:
        for n in range(size):
            answer = pipeline.answer(dataset[n]["question"])
            gold_answer = dataset[n]["answer"]

            em += exact_match(answer, gold_answer)
            f1 += f1_score(answer, gold_answer)

            all_answers.append(answer)
            all_gold_answers.append(gold_answer)

    # Compute semantic similarity metrics over all predictions
    bert_p, bert_r, bert_f1 = compute_bertscore_batch(
        all_answers,
        all_gold_answers
    )

    # Normalize scores by dataset size
    em /= size
    f1 /= size

    return {
        "exact_match": em,
        "f1": f1,
        "bert_score_precision": bert_p,
        "bert_score_recall": bert_r,
        "bert_score_f1": bert_f1,
    }


def run_experiment(dataset, claims, rag, rag_nli, rag_subclaim):
    """
    Run a comparative evaluation of multiple QA pipelines on the same dataset.
    """
    results = {}

    # Baseline RAG does not require claims
    results["RAG"] = evaluate_pipeline(rag, dataset)

    # NLI-based pipelines require claims as additional input
    results["RAG_NLI"] = evaluate_pipeline(rag_nli, dataset, claims)
    results["RAG_NLI_SUBCLAIM"] = evaluate_pipeline(rag_subclaim, dataset, claims)

    return results
