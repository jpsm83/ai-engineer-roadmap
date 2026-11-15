# AI Prompting for Everyone — Q&A

Fast-reference notes for Andrew Ng's *AI Prompting for Everyone* (DeepLearning.AI).
**Finding information → AI as a thought partner → Working with multimedia and code.**

---

## Part 1 — Finding Information

### The AI novice and the AI power user

**Q: How is prompting in 2026 different from 2022?**
A: Models can think for minutes, ingest many documents, and use web search and other tools. Novices still prompt like a Google search ("Does Taco Bell still have the Double Decker Taco?"); power users ask hard questions, upload context, and tell the model to think hard.

**Q: What college-grad analogy explains short prompts?**
A: Treat AI as a smart, motivated new graduate who does not know you yet. "Write a good self-review" is generic; uploading a project-tracker screenshot, docs, and voice memos captures what you are proud of. Power users almost have **empathy** for the AI: would this instruction give a person enough to do a good job?

**Q: How do power users get honest feedback instead of flattery?**
A: Models were trained to please you. Calling mobile tie-dye "my great business idea" invites praise; a **neutral** prompt plus a **rubric** (problem, market, competitive advantage) does not hint at the hoped-for answer and may score the idea 8/100.

**Q: How do power users write without AI slop, and are viral mistakes typical?**
A: They do not jump to a full draft: upload notes, outline, critique, expand to bullets, critique, then draft, treating the model as a thinking partner. Models err less than in 2022–2023 if prompted well; viral cases (r's in strawberry; walk vs. drive to wash the car) are not representative, and power-user work includes deep research, analyzing personal data, and building websites.

### Pretrained knowledge

**Q: Where does a model's knowledge come from?**
A: It learned patterns from huge amounts of internet text. That stored knowledge is **pretrained knowledge**, one of several training stages. Sources include Reddit, Quora, books, Wikipedia, news, and research articles: trillions of words.

**Q: How does internet frequency predict reliability, and do typos matter?**
A: Common topics (cooking, celebrities, movies) are usually more reliable; niche topics (quasars) have less text; Cantonese is under 0.1% of internet content; company secrets not on the open web are unknown. Typos are fine because models learned from messy text, but training data also has misconceptions and outdated facts, so pretrained knowledge is not enough for real-time questions.

### Web search

**Q: Why do models search the web, and which questions stay pretrained?**
A: Training stopped on a **knowledge cutoff** date (GPT-5.4: August 2025), so the "6-7" meme needed a search. A year in the question, current events, location-specific queries, and niche facts tend to trigger search, automatically or when you click search or write "please do a web search." Common knowledge stays pretrained: a phone dropped in soup, why cats stare at walls, what is on the Voyager 1 record.

**Q: Why can web search still be unreliable?**
A: Search prefers popular pages; one report found Reddit the most cited site, then Wikipedia, YouTube, Google, and Yelp. Asking "how safe are gray market peptides" may pull forums and seller sites, while steering toward WHO, FDA, and the EMA yields more scientific answers; pages can also be stale (a Henderson, Nevada running-spot list came from a page more than two decades old).

**Q: How does AI web search work, and when should you use a search engine instead?**
A: You talk to a **user-facing** model that may ask an assistant to query a search engine, scan results, download pages, and return **summaries**; it has not read those pages in full, so citations can misrepresent the source. Use a search engine to scan sources quickly, find a forgotten site, or open original data (e.g., a 2013 Honda Civic air filter); use AI search for synthesis, weighed pros and cons, or a conclusion across pages.

### Deep research

**Q: What is deep research, and when should you use it?**
A: A mode, offered by ChatGPT, Gemini, and Claude, that plans research, searches many sources (often in parallel), evaluates them, searches again if needed, and writes a cited report after minutes of work. You give rich context (e.g., a Palo Alto Halloween haunted house), approve a **research plan**, and let the model go deeper as needed — that loop is **agentic AI** — and Gemini can turn the report into a webpage or checklist. Pretrained knowledge is seconds for common facts; web search is many seconds and a handful of pages for current or niche facts; deep research is minutes, dozens of sources, and complex synthesis, usually user-triggered.

---

## Part 2 — AI as a Thought Partner

### Brainstorming

**Q: Why is "give me a list" a weak brainstorm?**
A: OpenAI data: about half of ChatGPT chats are writing and practical guidance; creative ideation is about 3.9%. Models can list 200 uses for a brick, but "workout plan, 38, beginner, 10 lb dumbbells, 15 minutes" still yields generic squats and push-ups.

**Q: How do you get more creative options?**
A: Add unusual context ("I can't stick to these; I have a trampoline and a cat") and iterate. Models prefer common internet answers, which is good for facts (tallest building) and bad for brainstorming, so ask for 3–5 options, say what you like and dislike, add forgotten facts, and request new options until one is worth fleshing out.

### Context

**Q: How much context can a model hold, and what is already in it?**
A: People keep about seven items in working memory; leading models can take on the order of **750,000 words** (about four or five Harry Potter books), so you can upload hundreds of pages of leases and reviews. Before you type, a **system prompt** (date, model name, "be helpful") and tool descriptions are already there; your prompt, uploads, and **chat history** are added next. Unrelated follow-ups (your workout, then one for your mom) leave distracting context, so start a **new chat** and give everything a trusted advisor would need; "read everything and think really hard" is a common pattern.

### AI desktop apps

**Q: What can desktop apps do that chat cannot?**
A: Apps such as Claude Cowork, Microsoft Copilot, and Google Antigravity can, with permission, **agentically** find and read files. Chat requires uploads in advance; a desktop app started in a folder can discover the filming-procedures file and even notice a crew member's birthday.

**Q: What is the safe workflow?**
A: State the task, let the model **propose a plan** without acting, review and revise, then execute. Limit access to the relevant folder, read permission requests, and remember that deleted files often skip the recycle bin and edits often have no history.

### Reasoning with AI

**Q: What can reasoning models do, and is "think step by step" still good advice?**
A: They can think at length on complex tasks; plots of human task duration vs. AI success show a move from seconds-long work (2024–2025) to tasks that take people many hours. "Think step by step" is largely obsolete: prefer **think hard** or **ultrathink**, or turn on a thinking control, let the model search, read files, and loop (e.g., a five-landmark Rome day), and use the newest model with real job-sized problems and all the context a human expert would need.

### Sycophancy

**Q: What is sycophancy?**
A: A trained bias to tell you what you want to hear. "Don't you think remote work is better?" and "Is it true that office work is more productive?" both get agreement. A Washington Post study found ChatGPT-style models used phrases like "that's correct" about **10 times** more than "not quite right," reinforced by thumbs-up training.

**Q: How do you prompt around it?**
A: Use **neutral framing** with no hint of the desired answer: "To what extent, if at all, do carbon taxes affect small businesses?" not "Aren't carbon taxes bad for small businesses?" Compare options with pros and cons; even "find all the positive measures this quarter" steers the model.

### Writing and critique

**Q: What is AI slop?**
A: Content that looks fine sentence by sentence but lacks substance: extra **em dashes**, overused **nuanced** and **delve**, lists of three, few concrete nouns, and vague **not X but Y**. OpenAI found writing is about 24% of ChatGPT tasks, the largest group, and people have even started saying "delve" more in speech.

**Q: What is progressive outlining, and how should you edit?**
A: Outline, critique, bullets, critique, then prose; a few outline words change a whole section, which is higher leverage than editing a premature draft word by word. About two-thirds of writing chats start from existing text. Edit piece by piece (sentence or paragraph), lock one piece, then move on; a whole-document rewrite is harder to review.

**Q: How do you get an honest critique?**
A: Give a **rubric** with unambiguous yes/no criteria and have the model score each item, then sum; you can brainstorm the rubric with AI first. "Score this out of 100, then break it down" makes the model pick a high score and justify it. In the course lab, a vague rubric scored a sci-fi story 100; an objective rubric scored 75 and named fixes.

**Q: Should one model critique another?**
A: Cross-model review (Gemini grades ChatGPT) can add a small boost; self-critique is usually fine. Models have **jagged intelligence**: better than people at some tasks, worse at others, and the best model for your task changes quickly, so try the same prompt on several models.

---

## Part 3 — Working with Multimedia and Code

### Multimedia data

**Q: What are multimodal outputs, and how do cost and time compare?**
A: Images, video, voice, music, and code as well as text; outputs are slower and more costly than text. Andrew Ng used Google's **Nano Banana** to design his daughter Nova's cat birthday cake, then a baker made it real. Text is cheapest and fastest (models started as **LLMs**); speech costs more, images more still, and video much more, so iterating is harder, and voice clones can patch a podcast flub or give game characters voices but also enable emergency-fund scams, so use them only for beneficial, responsible work.

### Image understanding

**Q: What can models see well, and what do they miss?**
A: They read text in images, including messy handwriting, and can infer a blocked whiteboard label (convolutional neural network). They see **coarsely** — similar gym machines get confused, while a distinctive human-sized hamster-wheel treadmill is identified well — so receipts and multi-image dumps work if you double-check; a picture is often the fastest context.

### Image generation

**Q: How should you prompt for images?**
A: Ask a text model to write the image prompt first: setting, character details, mood or style. Visual language helps: cinematic, watercolor, cyberpunk, anime. You can restore photos (glare, texture, aspect ratio), as in Andrew Ng's childhood picture.

**Q: How does image generation differ from text?**
A: Text is produced piece by piece and can be stopped early; images are generated **all at once** by a **diffusion model** that starts from noise and subtracts it toward a caption. Older models mangled hands, text, and character consistency; newer ones (e.g., Nano Banana infographics) are much better, though one image can still take tens of seconds and cost many cents vs. seconds and under a cent for a short paragraph, with costs trending down.

### Building apps

**Q: Can non-coders build apps with a prompt?**
A: Yes, at a basic level, and it is much easier than months ago, but it is not trivial: specify **goal**, **inputs**, and **outputs** (fireworks simulator, obstacle game, Pomodoro timer, bill splitter, outfit picker) and start with one well-defined task and no extra files. Easier: a platformer or French-vocab quiz; harder: a multiplayer game or live French practice with AI feedback. Try anyway; the lab builds shareable browser apps from one prompt.

### Data analysis

**Q: How does AI analyze spreadsheets, and when should it run code?**
A: Upload the file and ask; the model can use a **code-execution** tool, like web search, to write and run programs for averages, plots, and filters. It is not a top human data scientist, but it is fast at basic insights (a bubble-tea shop may skip flat drinks and graph four seasonal standouts), and "analyze carefully" can trigger minutes of thinking. Double-check figures because it can still **hallucinate**, though run code makes numbers more likely accurate; use pretrained knowledge for common facts, web search for current specifics, deep research for multi-source plans, and code when you need calculation or a chart.

### Putting it together

**Q: What does the final project practice, and what should you keep doing?**
A: (1) Brainstorm a research question with context and feedback, (2) run research with sources, (3) build an app from the report (quiz, mini-game, or infographic): thought partner, then information finding, then making something. After the course, keep trying new models, give AI hard tasks, and provide high-quality context so your intuition stays current.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Power user | Uploads context, thinks hard, prompts neutrally, iterates before drafting |
| Pretrained knowledge | Patterns learned from internet text up to a cutoff date |
| Knowledge cutoff | Last date the model's training text covers |
| Web search | Handful of live pages; auto or user-triggered; summaries, not full reads |
| Deep research | Minutes-long, many-source, plan-then-search agentic report |
| Agentic AI | Model chooses next searches or actions instead of one frozen plan |
| Context | Prompt, files, chat history, system prompt, and tool descriptions in view |
| System prompt | Hidden instructions (date, model, be helpful, how tools work) |
| Desktop app | Chat plus permissioned file tools (Cowork, Copilot, Antigravity) |
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
