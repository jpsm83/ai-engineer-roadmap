"""Inspect pretraining data and build the instruction fine-tuning dataset.

This course example shows how a raw JSONL file of question/answer pairs is
turned into two common fine-tuning formats:

- text-only: one "text" field containing question and answer together;
- question/answer: the prompt template and the answer kept separate.

It also peeks at a streaming pretraining dataset (C4) for comparison.
"""

import itertools
from pathlib import Path
from pprint import pprint

import datasets
import jsonlines
import pandas as pd
from datasets import load_dataset

DATA_DIR = Path(__file__).resolve().parent
INSTRUCTION_FILE = DATA_DIR / "lamini_docs.jsonl"
PROCESSED_FILE = DATA_DIR / "lamini_docs_processed.jsonl"

## Pretrained datasets are huge, so streaming=True downloads examples on demand
## instead of loading the whole dataset into memory.
# pretrained_dataset = load_dataset("EleutherAI/pile", split="train", streaming=True)

pretrained_dataset = load_dataset("c4", "en", split="train", streaming=True)

## islice() takes only the first n examples from the stream.
n = 5
print("Pretrained dataset:")
top_n = itertools.islice(pretrained_dataset, n)
for i in top_n:
    print(i)

## Load the course instruction data. Each line is one JSON object, which is why
## lines=True is required.
instruction_dataset_df = pd.read_json(str(INSTRUCTION_FILE), lines=True)
print("Instruction rows:", len(instruction_dataset_df))
print(instruction_dataset_df.head())

## to_dict() converts the table into column-oriented Python dictionaries:
## {"question": {0: ..., 1: ...}, "answer": {0: ..., 1: ...}, ...}
examples = instruction_dataset_df.to_dict()
text = examples["question"][0] + examples["answer"][0]
print("First question + answer:", text)

## Datasets from different sources use different column names. This block
## detects the convention and concatenates the first example accordingly.
if "question" in examples and "answer" in examples:
    text = examples["question"][0] + examples["answer"][0]
elif "instruction" in examples and "response" in examples:
    text = examples["instruction"][0] + examples["response"][0]
elif "input" in examples and "output" in examples:
    text = examples["input"][0] + examples["output"][0]
else:
    text = examples["text"][0]

## Template used when question and answer are trained together in one string.
prompt_template_qa = """### Question:
{question}

### Answer:
{answer}"""

question = examples["question"][0]
answer = examples["answer"][0]

## format() fills the placeholders in the template with the first example.
text_with_prompt_template = prompt_template_qa.format(question=question, answer=answer)
print("First formatted example:")
pprint(text_with_prompt_template)

## Template used when the model should learn to generate only the answer. The
## prompt ends after "### Answer:".
prompt_template_q = """### Question:
{question}

### Answer:"""

## Build both dataset variants in one pass so they stay aligned.
num_examples = len(examples["question"])
finetuning_dataset_text_only = []
finetuning_dataset_question_answer = []
for i in range(num_examples):
    question = examples["question"][i]
    answer = examples["answer"][i]

    ## text-only: prompt and answer in a single training string.
    text_with_prompt_template_qa = prompt_template_qa.format(question=question, answer=answer)
    finetuning_dataset_text_only.append({"text": text_with_prompt_template_qa})

    ## question/answer: the answer is stored separately as the target.
    text_with_prompt_template_q = prompt_template_q.format(question=question)
    finetuning_dataset_question_answer.append({"question": text_with_prompt_template_q, "answer": answer})

pprint(finetuning_dataset_text_only[0])

pprint(finetuning_dataset_question_answer[0])

## Save the question/answer version as JSONL, one object per line.
with jsonlines.open(str(PROCESSED_FILE), "w") as writer:
    writer.write_all(finetuning_dataset_question_answer)

## The same course data is also published on the Hugging Face Hub, which shows
## the expected DatasetDict(train/test) structure.
finetuning_dataset_name = "lamini/lamini_docs"
finetuning_dataset = load_dataset(finetuning_dataset_name)
print(finetuning_dataset)
