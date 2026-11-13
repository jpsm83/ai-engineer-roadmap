"""Evaluate a fine-tuned model with exact match and a benchmark harness.

This course example:

1. loads the Lamini docs test split;
2. loads the fine-tuned `lamini/lamini_docs_finetuned` model;
3. generates answers for a few test questions;
4. compares each generated answer with the target using exact match;
5. optionally runs EleutherAI's lm-evaluation-harness on ARC Easy.

The exact-match section runs locally on CPU. The benchmark section is skipped
unless the harness is installed or cloned next to this file.
"""

import shutil
import subprocess
import sys
from pathlib import Path

import datasets
import pandas as pd
import torch
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

DATA_DIR = Path(__file__).resolve().parent

## The base instruction dataset provides the held-out test split.
DATASET_NAME = "lamini/lamini_docs"

## The model trained on that dataset for longer than the 3-step demo.
MODEL_NAME = "lamini/lamini_docs_finetuned"

## A second dataset used for further evaluation and iteration in the course.
EVALUATION_DATASET_NAME = "lamini/lamini_docs_evaluation"

## How many test examples to generate answers for. Set to -1 to evaluate all.
NUM_EXAMPLES = 10


def is_exact_match(generated_answer, target_answer):
    """Exact match: true only when the two strings are identical."""
    return generated_answer.strip() == target_answer.strip()


def inference(
    text,
    model,
    tokenizer,
    max_input_tokens=1000,
    max_output_tokens=100,
):
    """Generate an answer for one prompt and strip the prompt from the output."""
    ## Tokenize the prompt into model input IDs.
    tokenizer.pad_token = tokenizer.eos_token
    input_ids = tokenizer.encode(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=max_input_tokens,
    )

    ## Generate tokens. The model continues the prompt one token at a time.
    ## The attention mask marks real tokens, and pad_token_id tells generate()
    ## which ID to use for padding.
    device = model.device
    attention_mask = torch.ones_like(input_ids)
    generated_tokens_with_prompt = model.generate(
        input_ids=input_ids.to(device),
        attention_mask=attention_mask.to(device),
        pad_token_id=tokenizer.pad_token_id,
        max_length=max_output_tokens,
    )

    ## Decode the token IDs back into text, dropping special tokens.
    generated_text_with_prompt = tokenizer.batch_decode(
        generated_tokens_with_prompt, skip_special_tokens=True
    )

    ## The decoded text starts with the prompt, so remove that prefix.
    generated_text_answer = generated_text_with_prompt[0][len(text):]

    return generated_text_answer


def load_test_data():
    """Load the Lamini docs dataset and return its test split."""
    dataset = datasets.load_dataset(DATASET_NAME)
    test_dataset = dataset["test"]

    ## Show one question/answer pair before running the model.
    print(test_dataset[0]["question"])
    print(test_dataset[0]["answer"])

    return test_dataset


def load_model():
    """Load the fine-tuned model and its matching tokenizer."""
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    ## eval() switches dropout and other training-only layers off.
    model.eval()

    return model, tokenizer


def show_one_prediction(test_dataset, model, tokenizer):
    """Generate and compare a single answer as a small sanity check."""
    test_question = test_dataset[0]["question"]
    generated_answer = inference(test_question, model, tokenizer)

    print(test_question)
    print(generated_answer)

    answer = test_dataset[0]["answer"]
    print(answer)

    exact_match = is_exact_match(generated_answer, answer)
    print(exact_match)

    return exact_match


def evaluate_exact_matches(test_dataset, model, tokenizer):
    """Generate answers for a few examples and count exact matches."""
    ## metrics collects one True/False value per example. predictions keeps the
    ## generated answer next to the target so they can be inspected.
    metrics = {"exact_matches": []}
    predictions = []

    ## tqdm draws a progress bar. stop after NUM_EXAMPLES, unless it is -1.
    for i, item in tqdm(enumerate(test_dataset)):
        print("i Evaluating: " + str(item))
        question = item["question"]
        answer = item["answer"]

        try:
            predicted_answer = inference(question, model, tokenizer)
        except Exception:
            ## Skip examples the model cannot process, as in the course.
            continue

        predictions.append([predicted_answer, answer])

        ## Exact match is strict: any wording difference counts as a miss.
        exact_match = is_exact_match(predicted_answer, answer)
        metrics["exact_matches"].append(exact_match)

        if i > NUM_EXAMPLES and NUM_EXAMPLES != -1:
            break

    print("Number of exact matches: ", sum(metrics["exact_matches"]))

    ## Tabulate predictions so they can be read side by side.
    df = pd.DataFrame(
        predictions, columns=["predicted_answer", "target_answer"]
    )
    print(df)

    return df


def show_evaluation_dataset():
    """Load the extra evaluation dataset used by the course."""
    evaluation_dataset = datasets.load_dataset(EVALUATION_DATASET_NAME)

    print(evaluation_dataset)

    ## The dataset has a train split; show its structure as a table.
    evaluation_df = pd.DataFrame(evaluation_dataset["train"])
    print(evaluation_df.head())

    return evaluation_dataset


def run_lm_evaluation_harness():
    """Run EleutherAI's lm-evaluation-harness on ARC Easy, if available.

    The course command expects a local clone:

        python lm-evaluation-harness/main.py \\
            --model hf-causal \\
            --model_args pretrained=lamini/lamini_docs_finetuned \\
            --tasks arc_easy \\
            --device cpu

    This function also supports the newer `lm_eval` command. If neither is
    installed, it prints setup instructions and returns.
    """
    harness_script = DATA_DIR / "lm-evaluation-harness" / "main.py"

    if harness_script.exists():
        command = [
            sys.executable,
            str(harness_script),
            "--model",
            "hf-causal",
            "--model_args",
            f"pretrained={MODEL_NAME}",
            "--tasks",
            "arc_easy",
            "--device",
            "cpu",
        ]
    elif shutil.which("lm_eval"):
        ## Newer harness CLI: --model hf instead of hf-causal.
        command = [
            "lm_eval",
            "--model",
            "hf",
            "--model_args",
            f"pretrained={MODEL_NAME}",
            "--tasks",
            "arc_easy",
            "--device",
            "cpu",
        ]
    else:
        print(
            "Skipping lm-evaluation-harness: install it with "
            "`pip install lm-eval` or clone "
            "https://github.com/EleutherAI/lm-evaluation-harness next to this "
            "file."
        )
        return

    print("Running:", " ".join(command))
    subprocess.run(command, check=False)


def main():
    test_dataset = load_test_data()
    model, tokenizer = load_model()

    show_one_prediction(test_dataset, model, tokenizer)
    evaluate_exact_matches(test_dataset, model, tokenizer)

    show_evaluation_dataset()

    ## Optional: run the ARC Easy benchmark when the harness is available.
    run_lm_evaluation_harness()


if __name__ == "__main__":
    main()
