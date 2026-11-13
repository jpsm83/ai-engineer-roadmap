# Finetuning Large Language Models — Q&A

Fast-reference notes for Sharon Zhou's *Finetuning Large Language Models* (DeepLearning.AI / Lamini).
**Why Finetune → Where Finetuning Fits In → Instruction Finetuning → Data Preparation → Training → Evaluation and Iteration → Getting Started.**

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

**Q: Finetuning vs. pretraining?**
A: Pretraining starts from random weights on broad data; finetuning starts from a pretrained model on a smaller, targeted dataset. Finetuning reuses the model's existing language ability instead of rebuilding it.

**Q: Why does starting from a pretrained model matter?**
A: The model already understands language, so you only teach the specific behavior or task. That cuts the required data and compute by orders of magnitude.

**Q: Are RAG and finetuning mutually exclusive?**
A: No — they are complementary. A common production pattern retrieves current facts with RAG and uses finetuning to enforce response style and format.

**Q: Base model vs. instruction-tuned model?**
A: A base model only predicts the next token; an instruction-tuned model has already learned to follow directions. Finetuning usually starts from an instruction-tuned model so it builds on that behavior.

---

## Part 3 — Instruction Finetuning

### Instruction tuning and PEFT

**Q: What is instruction finetuning?**
A: Training on pairs of an instruction and a desired response so the model learns to follow that kind of request. It is a form of supervised finetuning (SFT).

**Q: What does an instruction example contain?**
A: An `instruction`, an optional `input` that provides context, and the `output` the model should produce. The input can be empty when the instruction is self-contained.

**Q: Why use a prompt template?**
A: The template fixes how instruction, input, and output are framed. Using the same template at training and inference keeps the model's expected format consistent.

**Q: What is an Alpaca-style template?**
A: A common format with sections such as `### Instruction:`, `### Input:`, and `### Response:` that wraps each example. The model learns to emit the answer after the response marker.

**Q: What is full finetuning?**
A: Updating all of the model's weights. It is the most flexible option but needs the most memory and compute and produces a full model copy.

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
A: Into training, validation, and test sets. Train on one portion, tune and detect overfitting on validation, and report final results on the untouched test set.

**Q: Why must the format match at inference?**
A: The model learns the exact prompt structure it saw during training. A different template at inference shifts the input distribution and degrades output.

**Q: What happens during tokenization?**
A: Text is split into tokens and truncated or padded to a fixed maximum length. Long examples are cut, so important content must fit within the context limit.

**Q: What is a common data pitfall?**
A: **Leakage** — validation or test examples appearing in training. It inflates scores and hides real generalization problems.

---

## Part 5 — Training Process

### Training the model

**Q: What are the steps to train?**
A: (1) Load the pretrained model and tokenizer, (2) format and tokenize the data, (3) set training arguments, (4) run training while monitoring loss, and (5) save the model or adapters.

**Q: What loss does instruction finetuning use?**
A: Causal language modeling loss — the negative log-likelihood of each next token given the preceding tokens. The model learns to predict the response token by token.

**Q: Should loss be computed on the instruction tokens?**
A: No — the useful signal is the response. Masking the instruction tokens so only response tokens contribute stops the model from being trained to reproduce prompts.

**Q: What are the key training hyperparameters?**
A: Learning rate, number of epochs, batch size, and sequence length, plus warmup and weight decay. Start conservative and change one at a time.

**Q: What learning rate is appropriate?**
A: A small learning rate relative to pretraining, so the model adapts without forgetting. Too high destabilizes training; too low barely changes behavior.

**Q: How many epochs?**
A: Start with a small number, often one to three. More epochs raise the risk of overfitting, especially with a small dataset.

**Q: What is overfitting and how do you spot it?**
A: The model memorizes training examples instead of generalizing. Training loss keeps falling while validation loss flattens or rises.

**Q: What should you monitor during training?**
A: Training and validation loss curves, plus sample generations. Falling training loss with worsening samples signals a problem even when the number looks good.

**Q: What is a checkpoint?**
A: A saved snapshot of the model or adapters at a training step. Checkpoints let you compare versions, resume training, and roll back a bad run.

**Q: What does LoRA change during training?**
A: Only the adapter matrices receive gradients; the base weights stay frozen. The saved artifact is the small adapter, not a full model copy.

---

## Part 6 — Evaluation and Iteration

### Evaluating finetuned models

**Q: Why is evaluation essential?**
A: Lower training loss does not prove better behavior on real inputs. Evaluation shows whether the model actually improved and whether it regressed elsewhere.

**Q: How should a finetuned model be evaluated?**
A: On a held-out test set, against a clear baseline such as the base model or a prompted model. Use task metrics plus human review of real examples.

**Q: What metrics are used?**
A: Task-specific scores (e.g., accuracy, exact match, or overlap metrics), validation loss, and human ratings. For open-ended outputs, human or model-assisted judging matters more than a single number.

**Q: Why is human evaluation important?**
A: It catches tone, usefulness, and failure modes that automatic metrics miss. A model can score well and still be unhelpful or unsafe in practice.

**Q: What is the right baseline?**
A: The best cheaper alternative — usually the same model with prompt engineering or RAG. If finetuning does not beat it, the added cost is not justified.

**Q: How do you detect catastrophic forgetting?**
A: Test the finetuned model on general tasks and held-out inputs, not just the target task. A drop in unrelated abilities means the update was too aggressive.

**Q: How do you iterate?**
A: Improve the data first, then adjust hyperparameters, then consider a different model or LoRA settings. Data fixes usually beat hyperparameter tuning.

**Q: When should you stop iterating?**
A: When the model reliably clears the evaluation bar on the test set and further work costs more than it gains. Ship, monitor, and retrain when data or requirements change.

---

## Part 7 — Getting Started

### Practical considerations

**Q: How should a beginner start?**
A: Pick one narrow, high-value task, gather a small clean dataset, and establish a baseline with prompting or RAG first. Then finetune and compare against that baseline.

**Q: Managed service or self-hosted training?**
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
| Instruction / input / output | The three fields of a training example |
| Prompt template | Fixed wrapper applied to every training example |
| Alpaca-style | Template using `### Instruction:`, `### Input:`, `### Response:` |
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

*Study aid; for authoritative content, refer to the official DeepLearning.AI course.*
