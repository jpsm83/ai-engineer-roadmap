# Building Systems with the ChatGPT API — Q&A

---

## Part 1 — Introduction

### Prompt-based systems

**Q: How does building with prompts differ from supervised learning?**
A: Supervised learning needs labeled data, training, and a deploy cycle that can take months. A **prompt-based** system writes instructions, calls an LLM API, and iterates in minutes or hours because the model is already trained.

**Q: What does this course mean by a system?**
A: Not one prompt, but a **pipeline**: Python plus several LLM calls that classify input, retrieve facts, generate a reply, and check safety and quality. Each step can consume a prior completion or a tool, then pass a structured result downstream.

---

## Part 2 — Language Models, the Chat Format and Tokens

### How LLMs work

**Q: How is a language model trained?**
A: With supervised learning that repeatedly predicts the **next token** given the tokens so far. At inference it samples that distribution to continue the sequence.

**Q: What is a base LLM vs. an instruction-tuned LLM?**
A: A **base LLM** only continues likely text. An **instruction-tuned LLM** is further trained on instruction–response pairs and **RLHF** (reinforcement learning from human feedback) so it follows tasks. Use the instruction-tuned kind in applications.

### Tokens

**Q: What is a token?**
A: A common character sequence the tokenizer uses as a unit. Short common words are often one token; rarer words split (e.g., `prompting` → `prom` + `pt` + `ing`). Count them with OpenAI's Tokenizer UI or Python's `tiktoken`.

**Q: Why do letter-level tasks fail on a whole word?**
A: The model sees tokens, not characters, so reversing a word can scramble token pieces. Hyphenate letters (`l-o-l-l-i-p-o-p`) so each letter is its own token.

**Q: Why do tokens matter for cost and limits?**
A: Billing and the **context window** (input plus output) are in tokens. For English, **1 token ≈ 4 characters ≈ ¾ of a word** (100 tokens ≈ 75 words). The API returns `prompt_tokens`, `completion_tokens`, and `total_tokens`.

### Chat format

**Q: How do you call the Chat Completions API?**
A: Create `client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))` after loading `.env`, send a list of `messages` (each with `role` and `content`) to `client.chat.completions.create`, and read `response.choices[0].message.content`. Keep `OPENAI_API_KEY` in an environment variable (e.g., `python-dotenv`); never hard-code it. The course notebooks used the removed `openai.ChatCompletion.create` API.

**Q: What do the chat roles do?**
A: **`system`** sets standing behavior (persona, language, length). **`user`** is the human turn. **`assistant`** is a prior model turn you feed back, or extra context you inject as if the assistant already knew it.

**Q: Which generation parameters does the course use?**
A: **`temperature`** is sampling randomness (`0` is deterministic — use it for classification, extraction, and eval). **`max_completion_tokens`** caps the completion (the course called this `max_tokens`; that name is deprecated and does not work on reasoning models). For a one-letter `Y`/`N` gate, set `max_completion_tokens=1`. `gpt-5-nano` only allows the default temperature (`1`).

---

## Part 3 — Evaluate Inputs: Classification

### Routing queries

**Q: Why classify the user input first?**
A: Different intents need different pipelines (billing vs. product vs. account). A cheap first call returns a label so later prompts, tools, or humans only run for that path.

**Q: How do you classify with an LLM?**
A: Put the taxonomy in the system message (primary and secondary categories), wrap the query in a **delimiter** such as `####` so it is treated as data, and require **JSON** keys the program can load. Use `temperature=0` so the schema stays stable.

---

## Part 4 — Evaluate Inputs: Moderation

### Moderation API

**Q: What does the Moderation API do?**
A: `client.moderations.create(model="omni-moderation-latest", input=text)` scores text against OpenAI's content policy. The result includes **`flagged`**, boolean **`categories`** (`hate`, `violence`, `self-harm`, `sexual`, `sexual/minors`, `hate/threatening`, `violence/graphic`), and numeric **`category_scores`**. The course notebooks used the removed `openai.Moderation.create` API.

**Q: When would you ignore the default `flagged` bit?**
A: When the app needs a stricter bar. Use `category_scores` and set your own thresholds (e.g., block a lower violence score than the default flag).

### Prompt injection

**Q: What is prompt injection?**
A: User text that tries to override the system (“ignore previous instructions and…”). The model may then do a task it was not built for.

**Q: How do you reduce prompt injection?**
A: (1) Wrap user text in delimiters. (2) Strip those delimiter characters from the user string first. (3) Restate the standing rule next to the wrapped input. (4) Run a separate few-shot detector that answers only `Y` or `N` (`max_completion_tokens=1`) before the main call.

---

## Part 5 — Process Inputs: Chain of Thought Reasoning

### Step-by-step reasoning

**Q: What is chain of thought reasoning?**
A: Instructing the model to work through numbered steps before the user-facing answer, instead of jumping to a conclusion. Extra “thinking” tokens catch bad assumptions (a wrong comparison, a product you do not sell).

**Q: How do you structure a chain-of-thought system prompt?**
A: List the steps, require a fixed layout (`Step 1:{delimiter} …` through `Response to user:{delimiter} …`), and separate every step with the delimiter. Ground later steps in facts you placed in the prompt.

### Inner monologue

**Q: What is an inner monologue?**
A: The reasoning the user should not see. Because steps are delimiter-separated, take `response.split(delimiter)[-1]` as the reply and discard the scratch work. On parse failure, return a generic apology instead of raw chain-of-thought.

---

## Part 6 — Process Inputs: Chaining Prompts

### Multi-step pipelines

**Q: What is chaining prompts?**
A: Several LLM calls with **Python between them**. Call 1 extracts structure; code looks up facts or calls a tool; call 2 answers using only that retrieved context. State lives in your program, not in the model's memory.

**Q: Why chain instead of one long prompt?**
A: Each call is **more focused**; you stay under token limits by sending only relevant context; you **pay per token**, so a small extract plus a lookup is cheaper than pasting a whole catalog; and you can branch, search, or query a database between steps. A single chain-of-thought prompt is a poor fit when the task needs those tools.

**Q: How do you use the model as a reasoning engine?**
A: Do not ask it to memorize your catalog. Have it name products or categories in the query (structured list only), look those keys up in your data, then pass the records into the next call as an `assistant` message (`Relevant product information:` plus JSON). Require JSON-only output, `json.loads` after normalizing quotes, and treat decode errors as empty — do not invent products.

---

## Part 7 — Check Outputs

### Safety and quality gates

**Q: How do you check an output for harm?**
A: Completions can be harmful even when the input was clean, so send the reply to the Moderation API. If `flagged` is true, do not show it; return a refusal or escalate.

**Q: How do you check that an answer is sufficient and factual?**
A: A second LLM call sees the user question, the retrieved facts, and the draft reply, and returns **`Y`** only if the reply answers the question **and** uses those facts correctly, else **`N`**. Limit the completion to one token.

---

## Part 8 — End-to-End System

### Combining the pipeline

**Q: What is the end-to-end processing order?**
A: (1) Moderate the user input. (2) Extract relevant categories or products. (3) Look them up in your catalog. (4) Generate a grounded reply. (5) Moderate the reply. (6) Ask whether the reply sufficiently answers the question. (7) Return it, or escalate to a human.

**Q: What should happen when a check fails?**
A: Flagged **input** → refuse to process; flagged **output** → do not send the completion; quality gate **`N`** → apologize and hand off to a human. Do not retry silently with a weaker answer.

**Q: How do you keep a multi-turn assistant consistent?**
A: The API is stateless. Append each user turn and approved assistant reply to a **context** list and resend it on the next call, along with a short system message.

---

## Part 9 — Evaluation Part I

### When there is a single right answer

**Q: How do you evaluate an LLM application over time?**
A: (1) Tune prompts on a handful of examples. (2) Add **tricky** failures as you find them. (3) Define a metric on those examples. (4) If accuracy matters, collect a randomly sampled **development set**. (5) Keep a hold-out **test set** you do not tune on.

**Q: When is there a single right answer?**
A: When the output is structured and comparable: a category, a JSON list of IDs, a label. Score exact match (or set equality) against an **ideal answer** without judging prose.

**Q: How do you score a structured extraction against an ideal?**
A: Parse the completion to sets keyed by category: empty vs. empty is a full match, empty vs. nonempty is zero, equal product sets are correct, and a **subset** or **superset** is still wrong for exact match. Average per example, then report the fraction correct.

**Q: What belongs in the extraction instructions?**
A: Allowed categories and products only; map mentioned items to that list; if none match, output `[]`. Do not infer extra attributes (cheapest, best) from names. After a format failure, add “JSON only, no extra text” and few-shot examples that return the full allowed list as JSON.

**Q: What is regression testing for prompts?**
A: After a change that fixes a hard case, rerun the earlier examples. A tweak that helps one query must not break the ones that already worked.

---

## Part 10 — Evaluation Part II

### When there is no single right answer

**Q: How do you evaluate open-ended answers?**
A: Generated prose has many acceptable wordings, so do not require string equality. Use a **rubric**, comparison to an expert answer, or a similarity metric such as **BLEU**.

**Q: What is rubric evaluation?**
A: An evaluator LLM scores the submission against the question and the **context** the agent was given. Typical checks: based only on context (`Y`/`N`), extra facts not in context, disagreement with context, how many user questions, and how many were answered. Ignore style and punctuation.

**Q: How do you compare a submission to an expert answer?**
A: Use an eval prompt (the course uses one from OpenAI Evals) that picks a single letter: **(A)** subset of the expert and consistent, **(B)** superset and consistent, **(C)** same details, **(D)** factual disagreement, **(E)** differences that do not matter factually. A relevant shorter answer can be **A**; an unrelated sentence is **D**.

---

## Part 11 — Conclusion

### Takeaways

**Q: What is the working method for LLM systems?**
A: Split the job into evaluate-input, process, and check-output stages; keep facts and control flow in code; iterate with a growing eval set rather than hunting for one perfect prompt. Ground replies, moderate both directions, escalate when unsure, and use generation responsibly.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Prompt-based system | Pipeline of LLM calls and code, iterated in hours not months |
| Base vs. instruction-tuned | Next-token continuation vs. task-following after RLHF |
| Token | Tokenizer unit; ~4 English characters; basis of cost and context |
| `tiktoken` | Python library to count tokens locally |
| Chat format | List of `{role, content}` messages sent to `client.chat.completions.create` |
| `system` / `user` / `assistant` | Standing rules, human turn, prior or injected model turn |
| `temperature` | Sampling randomness; `0` for deterministic pipelines |
| Classification | First-pass label so later steps can route |
| Delimiter | Marker (e.g., `####`) that treats user text as data |
| Moderation API | Policy scores and `flagged` for input or output text |
| Prompt injection | User text that tries to override the system prompt |
| Chain of thought | Numbered reasoning steps before the final answer |
| Inner monologue | Hidden CoT; show only the last delimiter-separated span |
| Chaining prompts | Multiple API calls with code, tools, or lookups between them |
| Output check | Moderate the reply and `Y`/`N`-grade sufficiency and facts |
| Escalation | Hand off to a human when a safety or quality gate fails |
| Development / test set | Examples you tune on vs. a hold-out you do not |
| Exact-match eval | Structured output scored against an ideal (set equality) |
| Rubric eval | LLM grades open-ended answers against listed criteria |
| Expert comparison | A–E factual relation to a human-written ideal answer |
| BLEU | n-gram overlap score between two texts |

---
