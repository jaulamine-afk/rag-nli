from bert_score import score
import re
from collections import Counter



def exact_match(prediction, gold_answer):
    if prediction.strip().lower() == gold_answer.strip().lower():
        return 1
    else: 
        return 0

def f1_score(prediction, gold_answer):
    pred_tokens = re.findall(r'\w+', prediction.lower())
    gold_tokens = re.findall(r'\w+', gold_answer.lower())

    common_token = (Counter(pred_tokens) & Counter(gold_tokens)).total()

    if common_token == 0 :
        return 0
    
    recall = common_token/len(gold_tokens)
    precision = common_token/len(pred_tokens)

    return  2* ((recall * precision) / (precision + recall))


def compute_bertscore_batch(preds, golds):
    model_type = "distilbert-base-uncased"
    rescale_with_baseline = True
    P, R, F1 = score(preds, golds, model_type=model_type,
                     rescale_with_baseline=rescale_with_baseline, lang="en")
    return P.mean().item(), R.mean().item(), F1.mean().item()