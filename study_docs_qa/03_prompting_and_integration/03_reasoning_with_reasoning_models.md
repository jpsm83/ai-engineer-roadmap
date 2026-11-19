# Reasoning with reasoning model — Q&A

## Part 1 — Introduction to reasoning model

### Reasoning models

**Q: What is reasoning model?**
A: OpenAI's **reasoning model**: it thinks before it replies. Unlike GPT-4o, which writes the answer immediately, reasoning model spends inference time generating a hidden **chain of thought (CoT)**, then returns a more careful response. It is strong at abstract reasoning — planning, coding, analysis, law, and other STEM work.

**Q: What is test-time compute?**
A: Extra work at **inference**, not training. reasoning model spends that budget on hidden **reasoning tokens** that try strategies, catch errors, and break the problem down. More thinking time usually raises accuracy on tasks that benefit from a slow pass, and the loop gives extra chances to catch hallucinations.

**Q: What are reasoning tokens?**
A: Hidden completion tokens used as a scratchpad. You do not see them, but they count toward **cost** and the **context limit**; if the total overflows, the output is truncated. They are **not** carried into the next turn, so each call reasons from scratch.

**Q: How was reasoning model trained to reason?**
A: Large-scale **reinforcement learning** teaches it to produce a chain of thought before answering. That internal CoT is longer and higher quality than what you get by writing "think step by step" yourself. Typical behaviors: break the problem into steps, try several strategies, and correct mistakes.

**Q: What is consensus voting?**
A: A second way to spend inference compute: sample many answers and take the **majority**. When a good check exists, agreeing samples beat a single draw.

**Q: Where does reasoning model outperform GPT-4o?**
A: On reasoning-heavy evals: ML benchmarks, exams, PhD-level science (**GPQA Diamond**), and **MMLU**. On **MATH**, accuracy rose from 60.3% (GPT-4o) to 94.8% (reasoning model).

### Generator-verifier gap

**Q: What is the generator-verifier gap?**
A: For some problems, **checking** a candidate is much easier than producing one — puzzles, math, and code. If you have a reliable verifier, extra test-time compute pays off: generate, check, keep the valid result.

**Q: When does extra thinking time not help?**
A: When verification is no easier than generation, e.g., looking up a fact or recognizing an image. Thinking longer will not recover a missing capital city.

**Q: When should you use reasoning model instead of a smaller, faster model?**
A: Use reasoning model when the task has a generator-verifier gap or needs a test-and-learn loop (planning, coding, domain reasoning); use GPT-4o or `gpt-4o-mini` for cheap, low-latency steps. **reasoning model-mini** is the faster, cheaper sibling for coding, math, and science, with less world knowledge — intelligence trades off against latency and cost.

---

## Part 2 — Prompting reasoning model

### Four principles

**Q: What are the four prompting principles for reasoning model?**
A: (1) **Simple and direct**, (2) **no explicit CoT**, (3) **structure**, (4) **show rather than tell**. reasoning model needs less prompt scaffolding than earlier chat models; over-instructing fights its built-in reasoning.

**Q: Why keep reasoning model prompts simple and direct?**
A: Straightforward instructions work best. State the task; do not wrap it in a recipe of sub-steps. Extra guidance often makes the reply more verbose without making it more correct.

**Q: Should you ask reasoning model to think step by step?**
A: No. Explicit CoT ("think step by step", "don't skip any steps", a numbered plan) interferes with the model's own reasoning and can yield bloated output, worse answers, or even refusals. A short task statement is usually enough; extra steps are the exception for a few nuanced jobs.

**Q: How should you structure a complex reasoning model prompt?**
A: Split roles and data with delimiters: Markdown, quotes, or pseudo-XML such as `<instructions>`, `<policy>`, and `<user_query>`. Structure improves compliance and makes failures easier to locate.

**Q: What does show rather than tell mean?**
A: Give **one or two** worked examples instead of a long rule list. **Few-shot** context teaches domain, tone, and citation style more reliably than describing every expected behavior.

---

## Part 3 — Planning with reasoning model

### Orchestrator pattern

**Q: Why is reasoning model a good planner?**
A: Given a hard goal, a tool catalog, and constraints, it writes a detailed policy: which tools to call, in what order, and which branches to take. That planning step is where the extra intelligence is worth the cost.

**Q: How do you combine reasoning model with a cheaper model?**
A: **Orchestrator pattern:** (1) reasoning model or reasoning model-mini writes the plan once, (2) `gpt-4o-mini` executes the plan with tools in a loop. Using reasoning model for every tool call is slow and expensive; planning once and executing cheaply balances accuracy and cost.

**Q: What do you put in the planner prompt?**
A: Role, goal, the executor it will hand off to, each available function (name, arguments, when to use it), and bounds (e.g., notify the user before finishing, ship what you can now, back-order the rest). Ask for the next steps of the plan, not a chatty essay.

**Q: How should the executor be prompted?**
A: The cheaper model still needs explicit CoT. Tell it to follow the plan **exactly**, then (1) read the policy, (2) identify the current step, (3) briefly explain the action, (4) call the matching tool. Loop on `chat.completions.create` with `tools` until a terminal call such as `instructions_complete`. Set `parallel_tool_calls=False` if steps must stay ordered.

**Q: Should reasoning model call the tools itself?**
A: It can, but that is usually overkill. Reserve reasoning model for the plan; let `gpt-4o-mini` (or GPT-4o) do the function calls.

---

## Part 4 — Coding with reasoning model

### Generate, edit, and compare

**Q: How does reasoning model compare with GPT-4o on coding?**
A: reasoning model and reasoning model-mini outperform GPT-4o on coding that needs structure, validation, and edge cases. Use that gap when the spec is non-trivial, not for a one-line snippet.

**Q: How do you prompt reasoning model to write new code?**
A: State the behavior, constraints, and export names; ask for **code only** if you need a drop-in file. A capable reasoning model will invent structure and validation instead of a thin scaffold.

**Q: How do you use reasoning model to edit code?**
A: Paste the snippet and say what is wrong at a high level (nested loops, missing error handling, unreadability). Ask it to return only the cleaned version. It tends to flatten loops, add guards, and rename for clarity.

**Q: Can reasoning model judge two implementations?**
A: Yes. Ask which option is better and why. That **LLM-as-judge** pass is useful after you generate candidates from different models.

---

## Part 5 — Reasoning with images

### Hierarchy of reasoning

**Q: How do you send an image to reasoning model?**
A: Encode the file as **base64** and pass a multimodal user message: text plus `image_url` with `data:image/png;base64,...`. Optionally set `response_format` to `json_object` when you need a parseable extract.

**Q: Why is reasoning model stronger than GPT-4o at image reasoning?**
A: Vision plus test-and-learn: it can try a reading, check it against the picture, and drop hallucinated boxes or edges. GPT-4o often misreads dense diagrams (org charts, ER diagrams) that reasoning model gets right.

**Q: What is a hierarchy of reasoning for images?**
A: Pay latency and cost **once** up front: have reasoning model preprocess the image into a rich structured index (JSON with ids, names, roles, and reporting links). Later questions use that text, not the pixels. You avoid re-encoding the image, and Q&A becomes cheaper, faster, and more consistent.

**Q: Why extract structure before asking questions?**
A: Tuning the extraction prompt against the image is the expensive, error-prone step. Once the index is right, counting reports or tracing a manager is ordinary text reasoning — and you can even run that on a smaller model.

---

## Part 6 — Meta-prompting

### Routine generation

**Q: What is meta-prompting?**
A: Using reasoning model to **write and revise prompts** for a cheaper model. You hill-climb an evaluation set instead of guessing which RAG, fine-tune, or wording change you need.

**Q: How do you turn a human policy into an LLM routine?**
A: Give reasoning model the help-center article and a closed tool list. Ask for a program-like procedure: numbered actions, lettered sub-actions, `if...then...else`, function names in backticks, polite questions when data is missing, an "anything else?" step, and a final `case_resolution` call. Use only the supplied functions.

**Q: What should you check after generating a routine?**
A: A **data-quality** pass: the model must not invent tools. If it did, implement those functions or regenerate before you eval.

### Eval loop

**Q: How do you evaluate a customer-support routine?**
A: Run each case with a policy-following **agent** (`temperature=0`, tools on) and a simulated **customer** that answers from case details. Score the terminal tool name and arguments against `expected_function` and `expected_inputs`. Accuracy is the fraction of matching rows.

**Q: How does the meta-prompting loop improve the routine?**
A: (1) Send reasoning model the original policy, tool list, current routine, and eval table (request, expected vs. actual call, transcript, `is_correct`). (2) Ask it to fix failure modes without violating the source policy. (3) Re-run the eval. Repeat for a fixed number of iterations and plot accuracy.

**Q: How do you get a parseable revised policy from reasoning model?**
A: At the time of the course, reasoning model did not support structured outputs. Chain a GPT-4o call with a JSON schema such as `{ "final_answer": string }` and take that field.

**Q: What edits tend to raise eval score?**
A: Few-shot examples of two often-confused tools, named attributes the agent mislabels, tighter step wording, or a format change (Markdown vs. `<step>` / `<if>` XML). Keep every change compliant with the original policy and the allowed tools.

**Q: How do you stay inside the context window across iterations?**
A: Cap messages (e.g., `MAX_TOKENS = 120000`). Drop transcripts from older tables, add the newest eval first, then older runs until the budget is full, and reset the reasoning model thread each round so the instruction block stays clean.

---

## Part 7 — Conclusion

### Takeaways

**Q: What is the working method for reasoning models?**
A: Prompt reasoning model simply, spend it where thinking pays (plans, hard code, visual indexes, prompt rewrites), and delegate execution to faster models. Measure with evals; let reasoning model climb those evals.

**Q: When is reasoning model the wrong default?**
A: High-volume, low-reasoning steps, tight latency budgets, and lookups with no verifier. Those belong on GPT-4o or `gpt-4o-mini`.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| reasoning model | Reasoning model that thinks (hidden CoT) before it answers (gpt-5-nano) |
| non reasoning model | Faster, cheaper reasoning model variant for coding, math, and science (gpt-6-luna with reasoning_effort equals to none) |
| Test-time compute | Extra inference work that improves reasoning accuracy |
| Reasoning tokens | Hidden billed tokens; count toward context; not kept across turns |
| Chain of thought | Stepwise internal reasoning; reasoning model does this without being asked |
| Consensus voting | Sample many answers and keep the majority |
| MATH | Math-reasoning benchmark; reasoning model 94.8% vs. GPT-4o 60.3% |
| Generator-verifier gap | Checking a solution is easier than producing one |
| Simple and direct | Short, literal task; no extra recipe |
| No explicit CoT | Do not add "think step by step"; it can hurt reasoning model |
| Structure | Markdown, quotes, or XML tags that separate roles and data |
| Show rather than tell | One or two examples instead of a long rule list |
| Orchestrator | reasoning model plans; a cheaper model executes with tools |
| Hierarchy of reasoning | Index the image once; answer later from that structure |
| Meta-prompting | reasoning model rewrites a cheaper model's prompt using eval failures |
| Routine | Policy rewritten as numbered, tool-calling steps for an LLM |
| LLM-as-judge | Ask a model which of two outputs is better and why |

---
