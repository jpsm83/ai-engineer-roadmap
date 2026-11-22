# Finetuning Large Language Models — Q&A

---

## Part 1 — Why Finetune

### Finetuning vs. prompting and RAG

**Q: What is finetuning?**
A: Continuing to train a pretrained LLM on your own data so its weights change. The model learns patterns from your examples instead of only receiving them in the prompt.

**Q: How does finetuning differ from prompt engineering?**
A: Prompt engineering changes the input and leaves the weights untouched; finetuning changes the weights themselves. Prompting is cheap and reversible, while finetuning is slower and produces a new model artifact.

**Q: How does finetuning differ from RAG?**
A: **RAG** retrieves external documents at inference and puts them in the prompt; finetuning bakes behavior into the weights. RAG is for knowledge that changes; finetuning is for consistent style, format, and task behavior.

**Q: When is finetuning a good fit?**
A: When you need a specific tone or style, a strict output format, better accuracy on a narrow task, or a smaller, cheaper model that behaves like a larger one. It also helps when prompts have grown long and brittle.

**Q: When should you avoid finetuning?**
A: When prompt engineering or RAG already meets the bar, when you lack enough clean examples, or when the required knowledge changes frequently. Finetuning is the expensive option, not the default.

**Q: Does finetuning add new knowledge?**
A: It can, but that is not its strength. Facts injected by finetuning can become stale or hallucinated, so retrieval is the more reliable way to supply current, verifiable knowledge. Finetuning is primarily a behavior tool — tone, structure, refusal style, and reasoning pattern.

---

## Part 2 — Where Finetuning Fits In

### The adaptation spectrum

**Q: What is the spectrum of model adaptation?**
A: Prompt engineering → RAG → finetuning → pretraining, in increasing order of data, compute, and commitment. Cheaper options should be tried first.

**Q: What is pretraining?**
A: Training a model from scratch on massive general text to learn language and world patterns. It is enormously expensive and is not what this course teaches.

**Q: How does finetuning differ from pretraining?**
A: Pretraining starts from random weights on broad data; finetuning starts from a pretrained model on a smaller, targeted dataset. Finetuning reuses the model's existing language ability instead of rebuilding it.

**Q: Why does starting from a pretrained model matter?**
A: The model already understands language, so you only teach the specific behavior or task. That cuts the required data and compute by orders of magnitude.

**Q: Are RAG and finetuning mutually exclusive?**
A: No — they are complementary. A common production pattern retrieves current facts with RAG and uses finetuning to enforce response style and format.

**Q: Should you finetune a base model or an instruction-tuned model?**
A: A base model only predicts the next token; an instruction-tuned model has already learned to follow directions. `01_finetuned_vs_non_finetuned.py` compares `meta-llama/Llama-2-7b-hf` with `meta-llama/Llama-2-7b-chat-hf` through `BasicModelRunner`. The local training run starts from the base `EleutherAI/pythia-70m`.

---

## Part 3 — Instruction Finetuning

### Instruction tuning and PEFT

**Q: What is instruction finetuning?**
A: Training on pairs of an instruction and a desired response so the model learns to follow that kind of request. It is a form of supervised finetuning (SFT).

**Q: What does an instruction example contain?**
A: `lamini_docs.jsonl` stores a `question` and an `answer`. The scripts also recognize `instruction`/`response` and `input`/`output` when those column names appear.

**Q: Why use a prompt template?**
A: The template fixes how the question and answer are framed. `prompt_template_q` ends at `### Answer:` so the model learns to generate the answer. `prompt_template_qa` includes `{answer}` in one `text` string. Use the same template at inference.

**Q: What template do the scripts use?**
A: `### Question:` and `### Answer:`, not an Alpaca `### Instruction:` / `### Response:` wrapper. The chat comparison uses Llama 2's `[INST] ... [/INST]` around the same prompt.

**Q: What is full finetuning?**
A: Updating all of the model's weights. The local script does this: `AutoModelForCausalLM.from_pretrained("EleutherAI/pythia-70m")` and a Hugging Face `Trainer` for `max_steps=3`. It saves a full checkpoint under `lamini_docs_3_steps/final`, not a LoRA adapter.

**Q: What is parameter-efficient finetuning (PEFT)?**
A: Freezing most of the base model and training a small set of added parameters. It cuts memory and storage and lets many task adapters share one base model.

**Q: What is LoRA?**
A: **Low-Rank Adaptation** — a PEFT method that trains two small matrices whose product is added to selected weight matrices. Only the adapters are trained and saved, so the base model stays frozen.

**Q: Why does freezing the base model help?**
A: It reduces trainable parameters, GPU memory, and training time, and lowers the risk of damaging the model's general abilities. The adapters are small files that can be swapped per task.

---

## Part 4 — Data Preparation

### Building the dataset

**Q: Why is data preparation so important?**
A: The model learns exactly what the examples teach, so quality dominates. Bad, inconsistent, or duplicated data produces a worse model no matter how long you train.

**Q: How much data is needed?**
A: Often hundreds to a few thousand high-quality examples for a narrow task. Quality and coverage matter more than raw volume; more data helps only when it is clean and relevant.

**Q: What makes an example high quality?**
A: It is accurate, relevant to the target task, consistent in format, and representative of real inputs. Remove duplicates, contradictions, and low-effort responses.

**Q: How should the data be split?**
A: `train_test_split(test_size=0.1, shuffle=True, seed=123)` holds out 10% after tokenization. Train on the rest. The published Hub set `lamini/lamini_docs` already has `train` and `test` splits. Report final results on data that was not used to fit the weights.

**Q: Why must the format match at inference?**
A: The model learns the exact prompt structure it saw during training. A different template at inference shifts the input distribution and degrades output.

**Q: What happens during tokenization?**
A: `AutoTokenizer.from_pretrained("EleutherAI/pythia-70m")` turns text into `input_ids`. The script sets `pad_token` to `eos_token`, `truncation_side = "left"`, and `max_length` 2048. Long examples are cut, so important content must fit.

**Q: What is a common data pitfall?**
A: **Leakage** — validation or test examples appearing in training. It inflates scores and hides real generalization problems.

---

## Part 5 — Training Process

### Training the model

**Q: What are the steps to train?**
A: (1) `AutoTokenizer.from_pretrained` and `AutoModelForCausalLM.from_pretrained` on `EleutherAI/pythia-70m`, with `tokenizer.pad_token = tokenizer.eos_token`. (2) `tokenize_and_split_data` on `lamini_docs.jsonl`. (3) `TrainingArguments`. (4) `trainer.train()`. (5) `trainer.save_model`. Hosted calls use `BasicModelRunner` when Lamini credentials are set.

**Q: What loss does instruction finetuning use?**
A: Causal language modeling loss — the negative log-likelihood of each next token given the preceding tokens. The model learns to predict the response token by token.

**Q: Should loss be computed on the instruction tokens?**
A: The useful signal is the response, so many recipes mask the prompt tokens. These scripts do not: `add_column("labels", tokenized_dataset["input_ids"])` copies every token, and the causal model shifts them internally.

**Q: What are the key training hyperparameters?**
A: `TrainingArguments` in the script sets `learning_rate=1.0e-5`, `num_train_epochs=1`, `max_steps=3`, `per_device_train_batch_size=1`, `warmup_steps=1`, `optim="adafactor"`, `gradient_accumulation_steps=4`, and `max_length=2048`. `max_steps` overrides the epoch count.

**Q: What learning rate is appropriate?**
A: The script uses `1.0e-5`, small relative to pretraining, so the model adapts without forgetting. Too high destabilizes training; too low barely changes behavior.

**Q: How many epochs should you train?**
A: The script sets `num_train_epochs=1` and stops after `max_steps=3` so the lesson stays short. More epochs raise the risk of overfitting on a small dataset.

**Q: What is overfitting and how do you spot it?**
A: The model memorizes training examples instead of generalizing. Training loss keeps falling while validation loss flattens or rises.

**Q: What should you monitor during training?**
A: Training and validation loss curves, plus sample generations. Falling training loss with worsening samples signals a problem even when the number looks good.

**Q: What is a checkpoint?**
A: A saved snapshot of the weights. `trainer.save_model` writes `lamini_docs_3_steps/final`. `save_steps=120` and `save_total_limit=1` control intermediate saves. The longer comparison model is `lamini/lamini_docs_finetuned` on the Hub.

**Q: What does LoRA change during training?**
A: Only the adapter matrices receive gradients; the base weights stay frozen. The saved artifact is the small adapter, not a full model copy. The scripts in this folder do not use LoRA; their `Trainer` updates every weight of `pythia-70m`.

---

## Part 6 — Evaluation and Iteration

### Evaluating finetuned models

**Q: Why is evaluation essential?**
A: Lower training loss does not prove better behavior on real inputs. Evaluation shows whether the model actually improved and whether it regressed elsewhere.

**Q: How should a finetuned model be evaluated?**
A: `05_evaluation.py` loads `lamini/lamini_docs_finetuned` with `AutoModelForCausalLM` and scores `model.generate` against the held-out answers. Compare that with the base `EleutherAI/pythia-70m` and with a prompted baseline.

**Q: What metrics are used?**
A: `is_exact_match` is true only when `generated_answer.strip()` equals `target_answer.strip()`. The same file can run the lm-evaluation-harness ARC Easy benchmark. Human review still catches failures a string match misses.

**Q: Why is human evaluation important?**
A: It catches tone, usefulness, and failure modes that automatic metrics miss. A model can score well and still be unhelpful or unsafe in practice.

**Q: What is the right baseline?**
A: The best cheaper alternative — usually the same model with prompt engineering or RAG. If finetuning does not beat it, the added cost is not justified.

**Q: How do you detect catastrophic forgetting?**
A: Test the finetuned model on general tasks and held-out inputs, not just the target task. A drop in unrelated abilities means the update was too aggressive.

**Q: How should you iterate after a finetuning run?**
A: Improve the data first, then adjust hyperparameters, then consider a different model or LoRA settings. Data fixes usually beat hyperparameter tuning.

**Q: When should you stop iterating?**
A: When the model reliably clears the evaluation bar on the test set and further work costs more than it gains. Ship, monitor, and retrain when data or requirements change.

---

## Part 7 — Getting Started

### Practical considerations

**Q: How should a beginner start?**
A: Pick one narrow, high-value task, gather a small clean dataset, and establish a baseline with prompting or RAG first. Then finetune and compare against that baseline.

**Q: When should you use a managed service vs. self-hosted training?**
A: Managed platforms handle infrastructure and are faster to start; self-hosting gives control and can be cheaper at scale. Choose based on data sensitivity, budget, and team skills.

**Q: What costs should you expect?**
A: GPU compute for training, storage for datasets and checkpoints, and ongoing inference cost. Evaluation and data cleaning usually take more effort than the training run itself.

**Q: What privacy issues arise?**
A: Training data may contain sensitive information that the model can memorize or leak. Anonymize or redact data and confirm the provider's handling before uploading it.

**Q: What maintenance does a finetuned model need?**
A: Retraining when data, requirements, or the base model change, plus monitoring for drift and regressions. A finetuned model is a maintained artifact, not a one-off file.

**Q: What ethical risks should be checked?**
A: Bias inherited from training data, unsafe outputs, and overconfident wrong answers. Evaluate for fairness and safety and keep human oversight for high-stakes use.

**Q: What is the most common mistake?**
A: Finetuning before trying prompting or RAG, or training on too little or too noisy data. Both waste compute and produce a model that is hard to justify.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Finetuning | Further training a pretrained model on your own data |
| Prompt engineering | Shaping the input without changing weights |
| RAG | Retrieving external knowledge into the prompt at inference |
| Pretraining | Training a model from scratch on massive general data |
| Instruction finetuning | Training on instruction → response pairs |
| SFT | Supervised finetuning on labeled input/output examples |
| `question` / `answer` | Fields in `lamini_docs.jsonl` |
| Prompt template | `### Question:` and `### Answer:` (`prompt_template_q` or `prompt_template_qa`) |
| `[INST] ... [/INST]` | Llama 2 chat wrapper used with `BasicModelRunner` |
| `EleutherAI/pythia-70m` | Small base model the local `Trainer` fine-tunes |
| `AutoModelForCausalLM` | Hugging Face class that loads the causal model |
| `TrainingArguments` | Learning rate, `max_steps`, batch size, and checkpoint settings |
| Exact match | `is_exact_match`: stripped strings must be identical |
| Full finetuning | Updating all model weights |
| PEFT | Training only a small set of added parameters |
| LoRA | Low-rank adapters added to frozen weights |
| Adapter | Small trained file that modifies a frozen base model |
| Causal LM loss | Next-token negative log-likelihood |
| Tokenization | Splitting text into tokens, with truncation and padding |
| Train/validation/test split | Data portions for fitting, tuning, and final scoring |
| Leakage | Test or validation data accidentally used in training |
| Overfitting | Memorizing training data instead of generalizing |
| Catastrophic forgetting | Losing general skills after aggressive finetuning |
| Checkpoint | Saved snapshot of a model or adapter |
| Baseline | The cheaper model/prompt/RAG system to beat |
| Human evaluation | Human review of output quality and safety |

---

## Formulas

- **Causal LM loss:** `L = -Σ log P(token_t | token_<t)`
- **LoRA update:** `W' = W + (α/r) · B · A`

---
