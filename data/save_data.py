from datasets import load_dataset
import pickle

ds_stream = load_dataset('hotpotqa/hotpot_qa', 'distractor', split='validation', streaming=True)
ds_100 = []
for i, example in enumerate(ds_stream):
    if i >= 300:
        break
    ds_100.append(example)


with open('hotpotqa_300.pkl', 'wb') as f:
    pickle.dump(ds_100, f)

