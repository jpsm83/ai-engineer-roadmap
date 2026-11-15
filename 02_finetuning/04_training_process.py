"""Fine-tuning training process, step by step.

The course first shows the short Lamini version (choose a base model, load data,
train), then opens up the same process with Hugging Face Transformers so the
individual pieces are visible:

1. choose a base model and tokenizer;
2. tokenize and split the instruction data;
3. run the base model to see its answer before training;
4. configure training arguments;
5. train for a few steps, save, and reload the model;
6. compare the slightly trained model with a longer-trained model.

The local Hugging Face part runs on CPU. The Lamini sections at the bottom need
real Lamini credentials in the repository-root .env file; they are skipped when
those credentials are missing.
"""

import logging
import os
import time
from pathlib import Path

import datasets
import lamini
import pandas as pd
import torch
from dotenv import load_dotenv
from lamini import BasicModelRunner
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer as HFTrainer,
    TrainingArguments,
)

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = DATA_DIR

## Lamini models are referenced by IDs. The course uses this hash for the
## larger 2.8B model shown at the end of the lesson.
model_name_to_id = {
    "bigger_model_name": "06ad41e68cd839fb475a0c1a4ee7a3ad398228df01c9396a97788295d5a0f8bb"
}

## Load the shared credentials from the repository root. The local training
## below does not need them; only the BasicModelRunner calls do.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
lamini.api_url = os.getenv("POWERML__PRODUCTION__URL")
lamini.api_key = os.getenv("POWERML__PRODUCTION__KEY")


def lamini_is_configured():
    ## Treat missing, empty, or the literal placeholder "none" as not set.
    return bool(
        lamini.api_url
        and lamini.api_key
        and lamini.api_url.strip().lower() != "none"
        and lamini.api_key.strip().lower() != "none"
    )


def get_tokenize_function(tokenizer, max_length):
    """Return the tokenizer callback used by datasets.map()."""

    def tokenize_function(examples):
        ## datasets.map() sends lists when batched=True, so read the first
        ## element of the current one-example batch.
        if "question" in examples and "answer" in examples:
            text = examples["question"][0] + examples["answer"][0]
        elif "input" in examples and "output" in examples:
            text = examples["input"][0] + examples["output"][0]
        else:
            text = examples["text"][0]

        ## Pad within this example. The data collator later pads a whole batch.
        tokenizer.pad_token = tokenizer.eos_token
        tokenized_inputs = tokenizer(
            text,
            return_tensors="np",
            padding=True,
        )

        ## Do not exceed the configured model length.
        current_length = tokenized_inputs["input_ids"].shape[1]
        max_length_for_example = min(current_length, max_length)

        if current_length > max_length_for_example:
            logger.warning(
                "Truncating input from %s to %s",
                current_length,
                max_length_for_example,
            )

        ## Keep the end of long examples, which usually contains the answer.
        tokenizer.truncation_side = "left"
        tokenized_inputs = tokenizer(
            text,
            return_tensors="np",
            truncation=True,
            max_length=max_length_for_example,
        )

        ## Causal language models use the input token IDs as their labels.
        tokenized_inputs["labels"] = tokenized_inputs["input_ids"].copy()

        return tokenized_inputs

    return tokenize_function


def load_local_dataset(dataset_path, tokenizer, max_length):
    """Load, tokenize, and split the local JSONL instruction dataset."""
    ## Each line of the file is one question/answer example.
    finetuning_dataset_loaded = datasets.load_dataset(
        "json", data_files=dataset_path, split="train"
    )

    ## map() applies the tokenizer once per example and adds input_ids,
    ## attention_mask, and labels as columns.
    tokenized_dataset = finetuning_dataset_loaded.map(
        get_tokenize_function(tokenizer, max_length),
        batched=True,
        batch_size=1,
        drop_last_batch=True,
    )

    ## Hold out 10% for evaluation. A fixed seed keeps the split reproducible.
    split_dataset = tokenized_dataset.train_test_split(
        test_size=0.1, shuffle=True, seed=123
    )
    return split_dataset["train"], split_dataset["test"]


def tokenize_and_split_data(training_config, tokenizer):
    """Course helper: return tokenized (train, test) datasets."""
    dataset_path = training_config["datasets"]["path"]
    use_hf = training_config["datasets"]["use_hf"]
    max_length = training_config["model"]["max_length"]

    print("tokenize", use_hf, dataset_path)

    if use_hf:
        ## Published datasets already provide train/test splits.
        dataset = datasets.load_dataset(dataset_path)
        return dataset["train"], dataset["test"]

    return load_local_dataset(dataset_path, tokenizer, max_length)


def inference(text, model, tokenizer, max_input_tokens=1000, max_output_tokens=100):
    """Generate an answer with a model and strip the prompt from the output."""
    ## Tokenize: turn the prompt text into model input IDs.
    input_ids = tokenizer.encode(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=max_input_tokens,
    )

    ## Generate: let the model continue the prompt.
    device = model.device
    generated_tokens_with_prompt = model.generate(
        input_ids=input_ids.to(device),
        max_length=max_output_tokens,
    )

    ## Decode: convert token IDs back into text.
    generated_text_with_prompt = tokenizer.batch_decode(
        generated_tokens_with_prompt, skip_special_tokens=True
    )

    ## The generated text still starts with the prompt, so remove it.
    generated_text_answer = generated_text_with_prompt[0][len(text):]

    return generated_text_answer


class Trainer(HFTrainer):
    """Transformers Trainer extended with FLOPs/timing logs from the course."""

    def __init__(
        self,
        model,
        model_flops,
        total_steps,
        args=None,
        data_collator=None,
        train_dataset=None,
        eval_dataset=None,
        tokenizer=None,
        model_init=None,
        compute_metrics=None,
        callbacks=None,
        optimizers=(None, None),
    ):
        ## Use a language-modeling collator so variable-length examples are
        ## padded correctly and padding labels become -100 (ignored by loss).
        if data_collator is None and tokenizer is not None:
            data_collator = DataCollatorForLanguageModeling(
                tokenizer=tokenizer, mlm=False
            )

        super().__init__(
            model=model,
            args=args,
            data_collator=data_collator,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            processing_class=tokenizer,
            model_init=model_init,
            compute_metrics=compute_metrics,
            callbacks=callbacks,
            optimizers=optimizers,
        )

        ## Extra values used by the custom logging below.
        self.total_steps = total_steps
        self.model_flops = model_flops
        self.start_step = 0
        self.do_grad_scaling = False

    def training_step(self, model, inputs, num_items_in_batch=None):
        """Run one forward/backward pass, skipping empty batches."""
        ## A tokenized example can be empty after truncation; skip it.
        if inputs["input_ids"].numel() == 0:
            print("Inputs: ", inputs)
            print("Inputs - input_ids", inputs["input_ids"])
            print("numel", inputs["input_ids"].numel())
            return torch.tensor(0)

        model.train()
        inputs = self._prepare_inputs(inputs)

        with self.compute_loss_context_manager():
            loss = self.compute_loss(
                model, inputs, num_items_in_batch=num_items_in_batch
            )

        if self.args.n_gpu > 1:
            loss = loss.mean()

        ## Backpropagate through the loss.
        if self.do_grad_scaling:
            self.scaler.scale(loss).backward()
        else:
            self.accelerator.backward(loss)

        return loss.detach() / self.args.gradient_accumulation_steps

    def log(self, logs):
        """Add epoch, timing, and FLOPs information to each log entry."""
        if self.state.epoch is not None:
            logs["epoch"] = round(self.state.epoch, 2)

        self.update_log_timing(logs)

        output = {**logs, **{"step": self.state.global_step}}
        self.update_history(output)

        logger.debug("Step (%s) Logs: %s", self.state.global_step, logs)
        self.control = self.callback_handler.on_log(
            self.args, self.state, self.control, logs
        )

    def update_log_timing(self, logs):
        """Estimate iteration time, FLOPs, and remaining training time."""
        if len(self.state.log_history) == 0:
            self.start_time = time.time()
            logs["iter_time"] = 0.0
            logs["flops"] = 0.0
            logs["remaining_time"] = 0.0
            self.start_step = self.state.global_step
        elif self.state.global_step > self.start_step:
            logs["iter_time"] = (time.time() - self.start_time) / (
                self.state.global_step - self.start_step
            )
            logs["flops"] = self.model_flops / logs["iter_time"]
            logs["remaining_time"] = (
                self.total_steps - self.state.global_step
            ) * logs["iter_time"]

    def update_history(self, output):
        """Smooth loss values so the training curve is easier to read."""
        if "eval_loss" in output:
            return
        if len(self.state.log_history) > 0:
            smoothing_window = 100
            p = 1.0 / smoothing_window
            if "loss" in output:
                output["loss"] = (
                    output["loss"] * p
                    + self.state.log_history[-1]["loss"] * (1.0 - p)
                )
        self.state.log_history.append(output)


def run_local_training():
    """Run the full Hugging Face training walkthrough on the local dataset."""
    ## The course shows two dataset options. This repository uses the local
    ## JSONL file so the example works without depending on a Hub dataset.
    dataset_name = "lamini_docs.jsonl"
    dataset_path = str(DATA_DIR / dataset_name)
    use_hf = False

    ## Alternative from the course: use the published dataset instead.
    # dataset_path = "lamini/lamini_docs"
    # use_hf = True

    model_name = "EleutherAI/pythia-70m"

    ## A small config keeps the model, data, and tokenizer settings together.
    training_config = {
        "model": {
            "pretrained_name": model_name,
            "max_length": 2048,
        },
        "datasets": {
            "use_hf": use_hf,
            "path": dataset_path,
        },
        "verbose": True,
    }

    ## The tokenizer converts text to token IDs. This model has no separate pad
    ## token, so reuse the end-of-sequence token for padding.
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    train_dataset, test_dataset = tokenize_and_split_data(
        training_config, tokenizer
    )

    print(train_dataset)
    print(test_dataset)

    ## Load the base model. The 70m model is small enough to train on a CPU.
    base_model = AutoModelForCausalLM.from_pretrained(model_name)

    ## Use a GPU when available; otherwise fall back to CPU.
    device_count = torch.cuda.device_count()
    if device_count > 0:
        logger.debug("Select GPU device")
        device = torch.device("cuda")
    else:
        logger.debug("Select CPU device")
        device = torch.device("cpu")

    base_model.to(device)

    ## Show the base model's answer before any fine-tuning.
    test_text = test_dataset[0]["question"]
    print("Question input (test):", test_text)
    print(f"Correct answer from Lamini docs: {test_dataset[0]['answer']}")
    print("Model's answer: ")
    print(inference(test_text, base_model, tokenizer))

    ## Train only a few steps so the lesson finishes quickly. Each optimizer
    ## step accumulates gradients over several mini-batches.
    max_steps = 3

    trained_model_name = f"lamini_docs_{max_steps}_steps"
    output_dir = str(OUTPUT_DIR / trained_model_name)

    training_args = TrainingArguments(
        ## Learning rate: how far each optimizer step moves the weights.
        learning_rate=1.0e-5,
        ## Number of training epochs.
        num_train_epochs=1,
        ## Max steps to train for (each step is a batch of data).
        ## This overrides num_train_epochs when it is not -1.
        max_steps=max_steps,
        ## Batch size for training.
        per_device_train_batch_size=1,
        ## Directory to save model checkpoints.
        output_dir=output_dir,
        ## Other arguments.
        overwrite_output_dir=False,
        disable_tqdm=False,
        eval_steps=120,
        save_steps=120,
        warmup_steps=1,
        per_device_eval_batch_size=1,
        eval_strategy="steps",
        logging_strategy="steps",
        logging_steps=1,
        optim="adafactor",
        gradient_accumulation_steps=4,
        gradient_checkpointing=False,
        ## Parameters for early stopping.
        load_best_model_at_end=True,
        save_total_limit=1,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
    )

    ## Estimate the compute cost of one training step and scale it by the
    ## number of gradient accumulation steps.
    model_flops = (
        base_model.floating_point_ops(
            {
                "input_ids": torch.zeros(
                    (1, training_config["model"]["max_length"])
                )
            }
        )
        * training_args.gradient_accumulation_steps
    )

    print(base_model)
    print("Memory footprint", base_model.get_memory_footprint() / 1e9, "GB")
    print("Flops", model_flops / 1e9, "GFLOPs")

    ## The custom Trainer adds timing and FLOPs logging to the normal Trainer.
    trainer = Trainer(
        model=base_model,
        model_flops=model_flops,
        total_steps=max_steps,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        tokenizer=tokenizer,
    )
    trainer.do_grad_scaling = False

    ## Run the training loop.
    training_output = trainer.train()
    print(training_output)

    ## Save the trained weights locally, then reload them from disk.
    save_dir = f"{output_dir}/final"

    trainer.save_model(save_dir)
    print("Saved model to:", save_dir)

    finetuned_slightly_model = AutoModelForCausalLM.from_pretrained(
        save_dir, local_files_only=True
    )

    finetuned_slightly_model.to(device)

    ## Ask the slightly trained model the same test question.
    test_question = test_dataset[0]["question"]
    print("Question input (test):", test_question)

    print("Finetuned slightly model's answer: ")
    print(inference(test_question, finetuned_slightly_model, tokenizer))

    test_answer = test_dataset[0]["answer"]
    print("Target answer output (test):", test_answer)

    ## Compare with a model that was trained for longer on the same data.
    finetuned_longer_model = AutoModelForCausalLM.from_pretrained(
        "lamini/lamini_docs_finetuned"
    )
    tokenizer = AutoTokenizer.from_pretrained("lamini/lamini_docs_finetuned")

    finetuned_longer_model.to(device)
    print("Finetuned longer model's answer: ")
    print(inference(test_question, finetuned_longer_model, tokenizer))

    ## Look for examples that contain a specific moderation instruction.
    count = 0
    for i in range(len(train_dataset)):
        if "keep the discussion relevant to Lamini" in train_dataset[i]["answer"]:
            print(
                i,
                train_dataset[i]["question"],
                train_dataset[i]["answer"],
            )
            count += 1
    print(count)

    ## Compare the base model and the longer-trained model on a new prompt.
    base_tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-70m")
    base_model = AutoModelForCausalLM.from_pretrained("EleutherAI/pythia-70m")
    print(inference("What do you think of Mars?", base_model, base_tokenizer))

    print(
        inference(
            "What do you think of Mars?", finetuned_longer_model, tokenizer
        )
    )

    return test_question


def run_lamini_examples(test_question):
    """Run the hosted Lamini sections, when credentials are available."""
    if not lamini_is_configured():
        print(
            "Skipping Lamini-hosted examples: set POWERML__PRODUCTION__URL and "
            "POWERML__PRODUCTION__KEY in the repository-root .env to run them."
        )
        return

    ## Run the much larger fine-tuned model and explore moderation.
    bigger_finetuned_model = BasicModelRunner(
        model_name_to_id["bigger_model_name"]
    )
    bigger_finetuned_output = bigger_finetuned_model(test_question)
    print("Bigger (2.8B) finetuned model (test): ", bigger_finetuned_output)

    ## Fine-tune a model in three lines of code using Lamini's hosted service.
    ## Choose base model, load data, train. Training returns a model ID,
    ## dashboard, and playground interface.
    model = BasicModelRunner("EleutherAI/pythia-410m")
    model.load_data_from_jsonlines(
        str(DATA_DIR / "lamini_docs.jsonl"),
        input_key="question",
        output_key="answer",
    )
    model.train(is_public=True)

    ## Evaluate the trained model against the base model.
    out = model.evaluate()

    lofd = []
    for e in out["eval_results"]:
        q = f"{e['input']}"
        at = f"{e['outputs'][0]['output']}"
        ab = f"{e['outputs'][1]['output']}"
        di = {"question": q, "trained model": at, "Base Model": ab}
        lofd.append(di)

    df = pd.DataFrame.from_dict(lofd)
    style_df = df.style.set_properties(**{"text-align": "left"})
    style_df = style_df.set_properties(**{"vertical-align": "text-top"})
    print(style_df.to_string())


def main():
    logging.basicConfig(level=logging.INFO)
    test_question = run_local_training()
    run_lamini_examples(test_question)


if __name__ == "__main__":
    main()
