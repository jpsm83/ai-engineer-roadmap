"""Prepare instruction data for fine-tuning: tokenization and prompt formatting.

This is a course example. Run it from anywhere with:
    python finetuning/03_data_preparation.py
"""

from functools import partial
from pathlib import Path
from pprint import pprint

import datasets
import pandas as pd
from transformers import AutoTokenizer

MODEL_NAME = "EleutherAI/pythia-70m"
DATA_DIR = Path(__file__).resolve().parent
INSTRUCTION_FILE = DATA_DIR / "lamini_docs.jsonl"
MAX_LENGTH = 2048

PROMPT_TEMPLATE = """### Question:
{question}

### Answer:"""


def load_tokenizer():
    ## AutoTokenizer picks the tokenizer class that matches the model name.
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    ## This model has no dedicated padding token. Reusing the end-of-sequence
    ## token lets us pad batches without adding a new embedding.
    tokenizer.pad_token = tokenizer.eos_token
    return tokenizer


def show_tokenizer_basics(tokenizer):
    ## Tokenization turns text into integer IDs the model can process.
    text = "Hi, how are you?"

    encoded_text = tokenizer(text)["input_ids"]
    pprint(encoded_text)

    decoded_text = tokenizer.decode(encoded_text)
    print("Decoded tokens back into text: ", decoded_text)

    ## Tokenizing a list produces one ID list per text. The lists have
    ## different lengths because the texts contain different numbers of tokens.
    list_texts = ["Hi, how are you?", "I'm good", "Yes"]
    encoded_texts = tokenizer(list_texts)
    print("Encoded several texts: ", encoded_texts["input_ids"])

    ## padding=True adds pad tokens so all sequences in the batch are the same
    ## length, which is required for batched matrix operations.
    encoded_texts_longest = tokenizer(list_texts, padding=True)
    print("Using padding: ", encoded_texts_longest["input_ids"])

    ## truncation=True cuts anything longer than max_length. By default
    ## Hugging Face keeps the beginning and drops tokens from the right.
    encoded_texts_truncation = tokenizer(list_texts, max_length=3, truncation=True)
    print("Using truncation: ", encoded_texts_truncation["input_ids"])

    ## Switching to left-side truncation keeps the end of the text instead.
    ## This is useful for generation tasks, where the most recent tokens matter.
    tokenizer.truncation_side = "left"
    encoded_texts_truncation_left = tokenizer(list_texts, max_length=3, truncation=True)
    print("Using left-side truncation: ", encoded_texts_truncation_left["input_ids"])

    encoded_texts_both = tokenizer(
        list_texts, max_length=3, truncation=True, padding=True
    )
    print("Using both padding and truncation: ", encoded_texts_both["input_ids"])


def load_instruction_examples():
    ## Each line of the JSONL file is one training example.
    instruction_dataset_df = pd.read_json(str(INSTRUCTION_FILE), lines=True)
    examples = instruction_dataset_df.to_dict()

    ## Support the common column-name conventions used by instruction datasets.
    if "question" in examples and "answer" in examples:
        text = examples["question"][0] + examples["answer"][0]
    elif "instruction" in examples and "response" in examples:
        text = examples["instruction"][0] + examples["response"][0]
    elif "input" in examples and "output" in examples:
        text = examples["input"][0] + examples["output"][0]
    else:
        text = examples["text"][0]

    print("One raw example:")
    pprint(text)

    return examples


def build_finetuning_dataset(examples):
    if "question" not in examples or "answer" not in examples:
        raise ValueError(
            "This course example expects 'question' and 'answer' columns in "
            f"{INSTRUCTION_FILE}."
        )

    ## Wrap each question in the same prompt template the model will see at
    ## inference time. The answer stays separate so it can become the label.
    num_examples = len(examples["question"])
    finetuning_dataset = []

    for i in range(num_examples):
        question = examples["question"][i]
        answer = examples["answer"][i]
        text_with_prompt_template = PROMPT_TEMPLATE.format(question=question)
        finetuning_dataset.append(
            {"question": text_with_prompt_template, "answer": answer}
        )

    print("One datapoint in the finetuning dataset:")
    pprint(finetuning_dataset[0])

    return finetuning_dataset


def show_tokenizing_one_example(tokenizer, finetuning_dataset):
    ## Concatenate prompt and answer, then tokenize them as one sequence.
    text = finetuning_dataset[0]["question"] + finetuning_dataset[0]["answer"]
    tokenized_inputs = tokenizer(text, return_tensors="np", padding=True)
    pprint(tokenized_inputs["input_ids"])

    ## Never exceed the model/course limit, but also do not pad to a length
    ## longer than this example actually needs.
    max_length = min(tokenized_inputs["input_ids"].shape[1], MAX_LENGTH)

    tokenized_inputs = tokenizer(
        text,
        return_tensors="np",
        truncation=True,
        max_length=max_length,
    )
    pprint(tokenized_inputs["input_ids"])


def tokenize_function(examples, tokenizer):
    ## datasets.map() passes each row as a list when batched=True, but a plain
    ## string when batched=False. first() makes this helper work in both cases.
    def first(value):
        return value[0] if isinstance(value, list) else value

    ## Join the prompt and answer using whichever column names this dataset has.
    if "question" in examples and "answer" in examples:
        text = first(examples["question"]) + first(examples["answer"])
    elif "instruction" in examples and "response" in examples:
        text = first(examples["instruction"]) + first(examples["response"])
    elif "input" in examples and "output" in examples:
        text = first(examples["input"]) + first(examples["output"])
    else:
        text = first(examples["text"])

    ## Make sure padding is available, then tokenize. A left truncation side is
    ## used below so the end of long examples (usually the answer) is kept.
    tokenizer.pad_token = tokenizer.eos_token
    tokenized_inputs = tokenizer(
        text,
        return_tensors="np",
        padding=True,
    )

    max_length = min(tokenized_inputs["input_ids"].shape[1], MAX_LENGTH)
    tokenizer.truncation_side = "left"
    tokenized_inputs = tokenizer(
        text,
        return_tensors="np",
        truncation=True,
        max_length=max_length,
    )

    return tokenized_inputs


def build_tokenized_dataset(tokenizer):
    ## Load the local JSONL into a Hugging Face Dataset so map() can process it.
    finetuning_dataset_loaded = datasets.load_dataset(
        "json", data_files=str(INSTRUCTION_FILE), split="train"
    )

    ## map() runs tokenize_function once per batch and adds the tokenizer
    ## outputs (input_ids, attention_mask) as new dataset columns.
    tokenized_dataset = finetuning_dataset_loaded.map(
        partial(tokenize_function, tokenizer=tokenizer),
        batched=True,
        batch_size=1,
        drop_last_batch=True,
    )

    print(tokenized_dataset)

    ## Causal language models predict the next token, so the labels are the
    ## same token IDs as the input. The model internally shifts them by one.
    tokenized_dataset = tokenized_dataset.add_column(
        "labels", tokenized_dataset["input_ids"]
    )

    ## Hold out 10% of the examples for evaluation. The fixed seed makes the
    ## split reproducible.
    split_dataset = tokenized_dataset.train_test_split(
        test_size=0.1, shuffle=True, seed=123
    )
    print(split_dataset)

    return split_dataset


def show_hub_datasets():
    ## These examples come from the Hugging Face Hub and show how published
    ## datasets are organized into train/test splits.
    finetuning_dataset_path = "lamini/lamini_docs"
    finetuning_dataset = datasets.load_dataset(finetuning_dataset_path)
    print(finetuning_dataset)

    taylor_swift_dataset = "lamini/taylor_swift"
    bts_dataset = "lamini/bts"
    open_llms = "lamini/open_llms"

    ## Indexing returns a single example; [1] is the second training row.
    dataset_swiftie = datasets.load_dataset(taylor_swift_dataset)
    pprint(dataset_swiftie["train"][1])

    print("Other course datasets:", bts_dataset, open_llms)


def main():
    tokenizer = load_tokenizer()
    show_tokenizer_basics(tokenizer)

    examples = load_instruction_examples()
    finetuning_dataset = build_finetuning_dataset(examples)
    show_tokenizing_one_example(tokenizer, finetuning_dataset)

    split_dataset = build_tokenized_dataset(tokenizer)
    print("Finished with", len(split_dataset["train"]), "train examples")

    show_hub_datasets()

    # To publish a processed dataset:
    # split_dataset.push_to_hub("your-huggingface-username/dataset-name")


if __name__ == "__main__":
    main()
