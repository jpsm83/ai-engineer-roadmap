# AI Prompting for Everyone — Q&A

Fast-reference notes for Andrew Ng's *AI Prompting for Everyone* (DeepLearning.AI).
**Finding information → AI as a thought partner → Working with multimedia and code.**

---

## Part 1 — Finding Information

### Power users vs. novices

**Q: How has prompting changed since 2022?**
A: Models can think for minutes, ingest many documents, and call tools such as web search. A novice still types a short search-style query; a **power user** asks a hard question, attaches context, and tells the model to think hard.

**Q: Why do short prompts underperform?**
A: Treat the model as a capable new hire who does not know you yet. A one-line request is generic; notes, files, and constraints give it enough to do a good job. Power users almost have **empathy** for the AI: would this instruction be enough for a person?

**Q: How do you get honest evaluation instead of flattery?**
A: Models are trained to please. Hinting that an idea is "great" invites praise. Use **neutral framing** (no hoped-for answer in the wording) plus a **rubric** of scored criteria.

**Q: How do you avoid AI slop, and are viral model mistakes typical?**
A: Do not jump to a full draft: outline, critique, expand, critique, then write, using the model as a thinking partner. Viral failures (counting letters, toy riddles) are not representative of well-prompted work such as research, data analysis, or building a site.

### Pretrained knowledge

**Q: Where does a model's knowledge come from?**
A: Patterns learned from huge amounts of internet text: forums, books, Wikipedia, news, and papers. That stored knowledge is **pretrained knowledge**, one of several training stages.

**Q: When is pretrained knowledge reliable?**
A: Common topics with lots of training text are usually stronger; niche topics, low-resource languages, and anything never published are weaker or unknown. Typos in your prompt are fine because training text was messy, but the data also contains errors and outdated facts, so pretrained knowledge is not enough for live questions.

### Web search

**Q: When does a model need web search?**
A: Training stops at a **knowledge cutoff**. Current events, a year in the question, location-specific facts, and obscure details tend to trigger search (automatically or when you ask). Everyday common-sense questions usually stay pretrained.

**Q: Why can AI web search still be wrong?**
A: Search ranks popular pages, so forums and stale lists can outrank primary sources. Steer toward the authorities you trust, and treat citations as pointers to check, not as proof.

**Q: How does AI web search work, and when is a search engine better?**
A: A **user-facing** model may ask an assistant to query a search engine, scan hits, and return **summaries**; it has not fully read those pages, so citations can misstate the source. Use a search engine to scan original pages or find a forgotten URL; use AI search to synthesize and weigh sources.

### Deep research

**Q: What is deep research, and when should you use it?**
A: A mode (ChatGPT, Gemini, Claude) that plans research, searches many sources, evaluates them, searches again if needed, and writes a cited report after minutes. You supply rich context, approve a **research plan**, and let the model loop — that loop is **agentic AI**. Pretrained knowledge is seconds; web search is many seconds and a handful of pages; deep research is minutes, dozens of sources, and complex synthesis, usually user-triggered.

---

## Part 2 — AI as a Thought Partner

### Brainstorming

**Q: Why is "give me a list" a weak brainstorm?**
A: Models default to the most common internet answers. That is useful for facts and weak for ideation: you get a generic list instead of options fitted to your constraints.

**Q: How do you get more original options?**
A: Add unusual constraints, ask for a few options, say what you like and dislike, then request another round. Iterate until one option is worth developing.

### Context

**Q: What is in the model's context, and how large is it?**
A: **Context** is everything in view: a hidden **system prompt** (date, model, "be helpful", tool docs), your message, uploads, and **chat history**. Leading models can hold on the order of hundreds of thousands of words, far more than human working memory.

**Q: When should you start a new chat?**
A: When the next question is unrelated. Leftover history distracts the model. Give a new chat everything a trusted advisor would need; "read this and think hard" is a common pattern.

### Desktop apps

**Q: What can a desktop AI app do that chat cannot?**
A: With permission, apps such as Claude Cowork, Microsoft Copilot, and Google Antigravity can **agentically** find and read files in a folder. Chat only sees what you uploaded in advance.

**Q: What is the safe desktop workflow?**
A: State the task, let the model **propose a plan** without acting, review it, then execute. Limit access to the relevant folder, read permission prompts, and remember that deletes may skip the recycle bin and edits may have no history.

### Reasoning

**Q: What can reasoning models do, and is "think step by step" still useful?**
A: They can think at length on tasks that take a person hours. Prefer **think hard** / **ultrathink**, or a thinking control, and let the model search and loop. Give it a real job-sized problem and the context an expert would need; "think step by step" is largely obsolete.

### Sycophancy

**Q: What is sycophancy?**
A: A trained bias to agree with what you seem to want. Leading questions get agreement either way. Preference training (thumbs-up) reinforces phrases that sound confirmatory.

**Q: How do you prompt around sycophancy?**
A: Use **neutral framing** with no hint of the desired answer. Ask for pros and cons of options; even "list only the positives" steers the model.

### Writing and critique

**Q: What is AI slop?**
A: Prose that looks fine sentence by sentence but lacks substance: extra **em dashes**, overused **nuanced** and **delve**, lists of three, few concrete nouns, and vague **not X but Y**.

**Q: What is progressive outlining, and how should you edit?**
A: Outline → critique → bullets → critique → prose. Changing a few outline words rewrites a whole section, which is higher leverage than editing a premature draft. Edit piece by piece, lock one piece, then move on; a whole-document rewrite is harder to review.

**Q: How do you get an honest critique?**
A: Give a **rubric** of unambiguous yes/no criteria, score each item, then sum. "Score this out of 100" makes the model pick a high number and justify it. You can draft the rubric with AI first.

**Q: Should one model critique another?**
A: Cross-model review can add a small boost; self-critique is usually enough. Models have **jagged intelligence**: superhuman on some tasks, worse than people on others, and the best model for a task changes quickly, so try the same prompt on several.

---

## Part 3 — Working with Multimedia and Code

### Multimedia

**Q: What are multimodal outputs, and how do cost and time compare?**
A: Images, video, voice, music, and code as well as text. Text is cheapest and fastest (models started as **LLMs**); speech costs more, images more, video much more, so iterating is harder. Use voice clones only for beneficial, responsible work.

**Q: What can models see in images, and what do they miss?**
A: They read text, including messy handwriting, and can infer occluded labels. They see **coarsely**: distinctive objects are easier than similar-looking ones. Pictures are fast context; still double-check.

**Q: How should you prompt for image generation?**
A: Ask a text model to write the image prompt first: setting, character, mood or style (cinematic, watercolor, cyberpunk, anime). You can also restore photos (glare, texture, aspect ratio).

**Q: How does image generation differ from text?**
A: Text is produced token by token and can be stopped early. Images are generated **all at once** by a **diffusion model** that starts from noise and denoises toward a caption. Newer models are much better at hands, text, and character consistency, but an image still costs more time and money than a short paragraph.

### Apps and data

**Q: Can a non-coder build an app from a prompt?**
A: At a basic level, yes, if you specify **goal**, **inputs**, and **outputs** and start with one well-defined task. Simple single-player tools are easier than multiplayer or live AI-feedback apps; it is not trivial, but it is far easier than a year ago.

**Q: How does AI analyze a spreadsheet, and when should it run code?**
A: Upload the file and ask. A **code-execution** tool lets the model write and run programs for averages, plots, and filters, which makes numbers more trustworthy than mental arithmetic — still **hallucinate**-check the figures. Use pretrained knowledge for common facts, web search for current specifics, deep research for multi-source plans, and code when you need calculation or a chart.

**Q: How do you combine these skills on a real task?**
A: (1) Brainstorm the question with context and critique, (2) research with sources, (3) make something from the result (quiz, mini-app, infographic). Keep trying new models, give hard tasks, and supply high-quality context so your intuition stays current.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Power user | Uploads context, thinks hard, prompts neutrally, iterates before drafting |
| Pretrained knowledge | Patterns learned from internet text up to a cutoff date |
| Knowledge cutoff | Last date the model's training text covers |
| Web search | Handful of live pages; summaries, not full reads |
| Deep research | Minutes-long, many-source, plan-then-search agentic report |
| Agentic AI | Model chooses next searches or actions instead of one frozen plan |
| Context | Prompt, files, chat history, system prompt, and tool descriptions in view |
| System prompt | Hidden instructions (date, model, be helpful, how tools work) |
| Desktop app | Chat plus permissioned file tools |
| Think hard / ultrathink | Cue to reason at length; replaces "think step by step" |
| Sycophancy | Trained bias to agree with what you seem to want |
| Neutral framing / rubric | No hint of the desired answer / yes-no criteria scored then summed |
| AI slop | Generic AI prose (em dashes, delve, not-X-but-Y) |
| Progressive outlining | Outline → bullets → prose, with critique at each step |
| Jagged intelligence | Superhuman on some tasks, worse than people on others |
| Multimodal | Images, audio, video, or code as input or output |
| Diffusion model | Image generator that denoises from random pixels all at once |
| Goal / input / output | Three building blocks of an app-building prompt |
| Code-execution tool | Lets the model write and run code for analysis and plots |

---

*Study aid; for authoritative content, refer to the official DeepLearning.AI course.*
