# ChatGPT Prompt Engineering for Developers — Q&A

Fast-reference notes for Isa Fulford and Andrew Ng's *ChatGPT Prompt Engineering for Developers* (DeepLearning.AI).
**Introduction → Guidelines → Iterative development → Summarizing → Inferring → Transforming → Expanding → Chatbot.**

---

## Part 1 — Introduction

### Types of LLMs

**Q: What is prompt engineering?**
A: Writing instructions that steer an LLM toward a useful output. For developers it is the main way to build features on an LLM API — summarize, classify, rewrite, generate, or chat — without training a new model.

**Q: What is a base LLM?**
A: A model trained only to predict the next word. It continues text in a likely way, so a question may be completed with more questions instead of an answer.

**Q: What is an instruction-tuned LLM?**
A: A base model further trained on instruction–response pairs, then refined with **RLHF** (reinforcement learning from human feedback) to be helpful, honest, and harmless. It tries to do the task you asked for. Use this kind of model for applications.

**Q: What two principles make prompts work?**
A: (1) Write **clear, specific instructions**. (2) Give the model **time to think** (steps or an intermediate solution) instead of demanding a snap judgment.

---

## Part 2 — Guidelines

### Clear and specific instructions

**Q: Should a prompt be short?**
A: No. Clear is not the same as short. Extra context, constraints, and examples usually improve the result.

**Q: What is a delimiter?**
A: A marker that separates your instructions from the text the model should process — triple backticks, triple quotes, dashes, angle brackets, or XML tags. The model then knows which span is data.

**Q: What is prompt injection, and how do delimiters help?**
A: **Prompt injection** is user-supplied text that tries to override the task ("ignore previous instructions and…"). Wrapping that text in delimiters, and telling the model to treat only the delimited span as data, makes hijacking harder.

**Q: How do you get output a program can parse?**
A: Ask for a **structured format** and name the fields: JSON, HTML, Markdown, a table. The model then returns something code can load instead of free prose.

**Q: How do you handle input that may not fit the task?**
A: State the success path and the fallback. If the text contains steps, rewrite them as a numbered list; if it does not, output a fixed phrase such as `No steps provided` instead of inventing some.

**Q: What is few-shot prompting?**
A: Putting one or more input/output examples in the prompt before the real request. The model copies the shown format, tone, or style.

### Time to think

**Q: How do you give the model time to think?**
A: Break the job into ordered steps and ask it to complete them in sequence. Optionally name the output sections so each step lands in a fixed slot.

**Q: Why make the model solve a problem before judging someone else's answer?**
A: If you only ask "is this correct?", it often agrees with a plausible wrong solution. Have it produce its own solution first, then compare; do not let it grade until that work is done.

### Hallucinations

**Q: What is a hallucination?**
A: A fluent statement that is not true. Models will invent details about obscure or mixed-up entities rather than say they do not know.

**Q: How do you reduce hallucinations?**
A: Ground the answer in text you provide: first extract relevant quotes, then answer using only those quotes. Do not ask the model to recall niche facts from memory.

---

## Part 3 — Iterative Prompt Development

### Process

**Q: How do you develop a prompt?**
A: The same loop as machine learning: write a first prompt, run it, look at failures, then clarify instructions, add constraints, or give more thinking time. Repeat. There is no perfect prompt, only a **process** that converges.

**Q: What should you change when the output is wrong?**
A: Diagnose the failure, then adjust one of: clearer task wording, extra context, a length or format limit, a named audience, step-by-step reasoning, or examples. Change little, retest.

**Q: When do you test on many examples?**
A: After the prompt works on a few cases. A mature app needs a batch of inputs so a tweak that helps one sample does not break the rest.

### Common refinements

**Q: How do you control length?**
A: State a hard cap: at most N words, sentences, or characters. Models often overrun a vague "keep it short."

**Q: How do you aim the output at the right reader?**
A: Name the audience and what they care about. A specialist wants technical details; a shopper wants benefits. Without that, the model guesses and often guesses wrong.

**Q: How do you force required fields into the output?**
A: List them explicitly: IDs, a table of dimensions, HTML wrapping, and so on. If a field must appear, say so; the model will not reliably infer it.

---

## Part 4 — Summarizing

### Length, focus, and extract

**Q: What is summarizing with an LLM?**
A: Compressing a longer text into a shorter one while keeping the meaning. It is a core way to scan many documents or reviews quickly.

**Q: How do you keep a summary short?**
A: Put the budget in the prompt (`in at most 30 words`, or a sentence/character limit). Check the result; raise or lower the cap as needed.

**Q: How do you summarize for one purpose?**
A: Say who will read it and which aspect to emphasize (shipping, price, risk, plot). Otherwise the summary mixes every theme and the reader still has to hunt.

**Q: When should you extract instead of summarize?**
A: When you need selected facts, not a condensation of the whole text. **Extract** pulls only the requested slice; **summarize** retells everything, so off-topic points leak in.

**Q: How do you summarize many documents?**
A: Use the same prompt in a loop, one input at a time, and collect the outputs. That is enough for a human to scan a large queue.

---

## Part 5 — Inferring

### Labels and fields

**Q: What is inferring?**
A: Reading a text and returning labels or hidden attributes: sentiment, emotions, topics, entities. You describe the task in English instead of training a classifier.

**Q: How do you classify sentiment?**
A: Ask for the sentiment and, if code will consume it, restrict the answer to a small set (`positive` or `negative`). Open-ended wording yields a paragraph you then have to parse.

**Q: How do you detect emotions or a specific feeling?**
A: Ask for a short list (cap the count and the format) or a yes/no for one emotion such as anger. Tight output specs keep results consistent.

**Q: How do you pull several fields in one call?**
A: List every field, require JSON (or another schema), and say what to use when a value is missing (`unknown`). One LLM call can replace several traditional NLP models.

### Topics

**Q: How do you find topics in a text?**
A: Ask for a fixed number of short topic phrases. You can also check a predefined list and return `0` or `1` per item (**zero-shot** labeling) and trigger an alert when a watched topic is present.

---

## Part 6 — Transforming

### Language and tone

**Q: What is transforming?**
A: Taking text in one form and returning it in another: language, register, file format, or corrected prose. The prompt must name both the input form and the desired output form.

**Q: What translation can you ask for?**
A: Identify a language, translate into one or several targets, or request formal vs. informal variants. Quality varies by language; always specify source and target.

**Q: How do you change tone?**
A: Name the current tone and the target (slang → business letter, casual → legal). "Make it nicer" is too vague to control.

### Format and proofreading

**Q: How do you convert formats?**
A: Describe both sides: JSON to an HTML table, Markdown to a dict, and so on. Include headers, keys, or titles you need in the result.

**Q: How do you proofread with an LLM?**
A: Instruct it to `proofread and correct`, and say what to output if nothing is wrong. It can fix grammar, homonyms, and spelling; you can also ask it to restyle the text (tone, house style, Markdown) in the same pass.

---

## Part 7 — Expanding

### Generation and temperature

**Q: What is expanding?**
A: Growing a short input (notes, a review, a bullet list) into a longer piece (email, essay, reply). It is the inverse of summarizing.

**Q: How do you generate a useful long reply?**
A: Give the facts to use, the action (thank vs. apologize), the tone, and any required signature or disclaimer, and tell the model to reuse specific details from the source. Use this capability responsibly: do not spam, and disclose when a message is from an AI.

**Q: What is temperature?**
A: The sampling randomness of the completion. **`temperature=0`** always picks the most likely next token (stable, repeatable — use this for production tasks). Higher values (e.g., `0.7`) pick less likely tokens: more variety, more drift from the brief.

---

## Part 8 — Chatbot

### Chat format

**Q: How does a chat API differ from a single prompt?**
A: You send a list of **messages** instead of one string. Each message has a role and content. The model replies to the whole list.

**Q: What does each role do?**
A: **`system`** sets persona and standing rules (how to behave for the whole conversation). **`user`** is the human turn. **`assistant`** is a previous model turn you are feeding back.

**Q: Does the model remember the conversation?**
A: No: each API call is stateless. To continue a chat you must resend the **context** (system message plus earlier user and assistant turns); omit a turn and the model no longer knows it.

### Building a specialized bot

**Q: How do you specialize a chatbot?**
A: Put the job, style, workflow, and any catalog or constraints in the system message. The bot then greets, collects what it needs, confirms, and stays in character without restating those rules every turn.

**Q: How do you keep a multi-turn bot consistent?**
A: Append every new user line and assistant reply to the message list and send the full list on the next call. Use a low temperature so it does not invent options outside the rules.

**Q: How do you get a structured result from a chat?**
A: After (or during) the conversation, send another completion that asks for a JSON (or other schema) summary of the collected fields. That object is what your backend should store or execute.

---

## Part 9 — Conclusion

### Takeaways

**Q: What is the working method?**
A: Clear instructions, time to think, then iterate until the prompt is good enough. Prompt engineering is that loop, not a single magic sentence.

**Q: What can you build with these techniques?**
A: Summaries, inferences, transformations, expansions, and chatbots — often in minutes or hours, because calling an instruction-tuned LLM is cheap compared with training a custom model. Experiment, and use generation responsibly.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Prompt engineering | Steering an LLM with instructions instead of training a new model |
| Base LLM | Next-word model; continues text rather than following a task |
| Instruction-tuned LLM | Base model fine-tuned on instructions, then RLHF |
| RLHF | Human preference training toward helpful, honest, harmless |
| Delimiter | Marker that separates instructions from data |
| Prompt injection | User text that tries to override the intended task |
| Few-shot prompting | Examples in the prompt that show the desired behavior |
| Time to think | Steps or a private solution before the final answer |
| Hallucination | Fluent but false content |
| Iterative development | Write, run, diagnose, refine; repeat |
| Summarize vs. extract | Condense the whole text vs. pull only requested facts |
| Inferring | Labels or fields (sentiment, topics, entities) from text |
| Zero-shot | Classify from instructions only, no extra training |
| Transforming | Convert language, tone, format, or correctness |
| Expanding | Grow a short input into a longer text |
| Temperature | Sampling randomness; `0` = deterministic, higher = more varied |
| System / user / assistant | Chat roles: standing rules, human turn, prior model turn |
| Context | Message history you must resend; the API is stateless |

---

*Study aid; for authoritative content, refer to the official DeepLearning.AI course.*
