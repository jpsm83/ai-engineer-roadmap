# AI Coding Crash Course — Fundamentals — Q&A

Fast-reference notes for Matt Pocock's *AI Coding Crash Course* (AI Hero).
**Your Starting Context → Killing Bloat → Showing Context in the Status Line → Codebase Exploration → The /teach Skill → Build a Feature → Why Plan Mode Sucks → The Grill-Execute-Clear Loop → Compaction → Handing Off → Clear, Compact, Handoff, or Subagent → Auto-Compaction.**

---

## Part 4 — Fundamentals

### Your Starting Context

**Q: What is your starting context?**
A: Everything the agent sees before your first message: the **system prompt**, project instructions such as `CLAUDE.md` or `AGENTS.md`, tool definitions, and often the repository's file tree.

**Q: Why is the starting context often already large?**
A: The system prompt can be tens of thousands of tokens, every tool adds a schema, MCP servers add more, and a long instruction file is loaded in full. You pay for all of it on every request.

**Q: How do you measure the starting context?**
A: Use the request logger or the harness's context display to see the token count. If the first turn is already large, the problem is configuration, not the task.

**Q: What belongs in the always-loaded layer?**
A: Only instructions that apply to every session: build and test commands, hard constraints, and conventions the code cannot make obvious. Everything else should be behind a skill or a pointer.

### Killing Bloat

**Q: What counts as context bloat?**
A: Unused MCP servers, verbose instruction files, irrelevant skills, large tool schemas, pasted documentation, and stale tool results. Anything loaded without serving the current task is bloat.

**Q: How do you kill bloat?**
A: Disable unused MCP servers, shorten `AGENTS.md` to the lines that apply everywhere, move detail into skills, and replace long explanations with **context pointers**.

**Q: Why is a large tool set harmful?**
A: Every tool definition occupies context, and many similarly described tools make the model worse at choosing the right one. A narrow, well-described tool set is easier to use than a broad, fuzzy one.

**Q: Does removing context lose information?**
A: Only if the information is gone entirely. A pointer keeps it reachable; a skill keeps it loadable. Progressive disclosure moves detail out of the always-on layer without deleting it.

**Q: What is the first thing to check when the agent seems forgetful?**
A: The size and relevance of the context. If the window is full of stale tool output, the fix is clearing or compacting, not adding more instructions.

### Showing Context in the Status Line

**Q: What is the context status line?**
A: A harness display, often customisable, that shows model, token usage, context percentage, or other session state. It makes the invisible budget visible while you work.

**Q: Why is a status line useful?**
A: It gives you an early warning before the dumb zone. You can compact or hand off at a phase boundary instead of discovering the degradation after a bad change.

**Q: What should you watch?**
A: The context percentage and the growth rate. A fast-growing session is a sign that tool results are dominating or that the task is too broad for one context.

### Codebase Exploration

**Q: Why explore the codebase before changing it?**
A: The agent needs to find the existing patterns, types, routes, and tests. Without exploration it reinvents helpers, duplicates logic, and ignores the conventions the project already enforces.

**Q: How should you direct exploration?**
A: Start with the structure: `package.json`, routes, database schema, and test layout. Then point at the files closest to the feature and ask the agent to explain how they connect.

**Q: Why use a subagent for exploration?**
A: A broad search produces pages of tool results that matter only long enough to find the answer. A subagent burns its own context and reports back the few paths and facts you need.

**Q: What should an exploration report contain?**
A: The relevant files, the existing pattern to follow, the tests that cover the area, and any constraints or gotchas. Ask for paths, not a long narrative.

**Q: How do you verify the agent's understanding?**
A: Ask it to describe the data flow or the proposed change in its own words, then check that description against the code. A plausible summary is not evidence; the files are.

### The /teach Skill

**Q: What is `/teach`?**
A: A skill that turns a directory into a teaching workspace and teaches one topic across many sessions. It writes a mission, vetted resources, short lessons, and a record of what you have learned.

**Q: When should you use `/teach`?**
A: When learning is the project: an unfamiliar codebase, a framework, a language, or a new stack. It is not for a single explanation inside a working session.

**Q: How does it avoid relying on the model's memory?**
A: It treats **parametric knowledge** as untrusted. It finds high-trust resources, records them in `RESOURCES.md`, cites them in every lesson, and recommends a primary source to read yourself.

**Q: Why is it stateful?**
A: The mission, resources, lessons, and learning records live as files. A fresh session continues from those files instead of depending on what is left of the previous conversation.

**Q: How does `/teach` connect to grilling?**
A: If a grilling session hits something you do not understand, hand off to a teaching workspace, learn the topic, then return to the original thread. Do not stop the grilling to learn mid-decision.

### Build a Feature

**Q: What is the feature-building loop?**
A: Explore the relevant code, agree on the approach, implement in small steps, run the checks, and review the diff. The loop repeats until the feature is done and verified.

**Q: Why small steps?**
A: Each step is easier to review and easier to revert. A large change hides mistakes, fills the context with tool results, and makes it hard to tell which decision caused a failure.

**Q: What should the agent do before editing?**
A: Read the files it will change and the tests that cover them. It should state the plan and the acceptance criteria, then make the smallest change that satisfies them.

**Q: How do you verify a feature?**
A: Run the automated checks, exercise the behaviour, and read the diff. Passing tests mean the asserted properties hold; they do not mean the feature is the right one.

**Q: What is the most common feature-building mistake?**
A: Letting the agent build the whole feature in one turn without a checkpoint. The context fills, the review becomes impossible, and the first real inspection happens after the mess is complete.

### Why Plan Mode Sucks

**Q: What is plan mode?**
A: An **agent mode** that blocks edits and steers the agent toward research and planning. It is useful for reading and proposing, but it is not a substitute for a real design conversation.

**Q: Why does plan mode often disappoint?**
A: It makes the agent hurry to produce a plan and treat that plan as settled. The plan looks complete, but the decisions you never made are filled with defaults.

**Q: What should you do instead of relying on plan mode?**
A: **Grill** the idea first. Make the agent ask questions until the requirements and trade-offs are explicit, then write the plan from that shared understanding.

**Q: When is plan mode still useful?**
A: For safe exploration and for producing a first draft when the problem is already well specified. Use it as a read-only workspace, not as a substitute for thinking.

### The Grill-Execute-Clear Loop

**Q: What is grilling?**
A: A Socratic interview in which the agent asks you one decision at a time, often with a recommended answer, until the design concept is stable. No handoff artifact is written until the concept is shared.

**Q: Why grill before building?**
A: Agents fill gaps silently. Asked to build from a vague prompt, the model picks defaults and writes them in, so you discover the guesses late, at review or in production.

**Q: What is the grill-execute-clear loop?**
A: Grill until the requirements are shared, execute the work in a focused session, then clear the context before the next piece. Each phase gets a fresh, sharp window.

**Q: How do you know grilling is finished?**
A: The agent stops asking questions because the frontier is empty, and you can defend each decision to someone who was not there. Then you confirm the shared understanding before work starts.

**Q: What if a question cannot be answered in conversation?**
A: **Prototype** it. Build a rough version, react to the artifact, and return to the conversation with an answer. Some questions need something to look at, not more words.

**Q: What is the main risk in grilling?**
A: Passivity. If you answer "agreed" to every question, you end up with a plan the agent wrote and you nodded at. Push back, change scope, and say "I don't know" when true.

### Compaction

**Q: What is compaction?**
A: A **handoff** done in memory: the session history is summarised, and the summary seeds a fresh session. It trades detail for headroom.

**Q: Why is compaction lossy?**
A: The summary is a **secondary source**. Whatever the summariser leaves out is gone from the new context, including decisions that seemed unimportant at the time.

**Q: When should you compact?**
A: At a phase boundary, after the plan is settled and before the next big step. Tell the summariser what must survive: schema decisions, constraints, and the next task.

**Q: Why not compact mid-task?**
A: The summary decides for itself what mattered, often while the work is half-finished. Mid-task compaction is how an agent confidently forgets a constraint you established an hour ago.

**Q: What is the difference between compact and clear?**
A: **Compact** tries to carry the essentials across; **clear** drops everything and starts cold. Clear is better when the accumulated context is mostly noise.

**Q: How do you make compaction safer?**
A: Write decisions into a plan or handoff artifact on disk first, then compact. The file survives even if the summary loses the detail.

### Handing Off

**Q: What is a handoff?**
A: Transferring context from one session to another through a carry mechanism, usually a **handoff artifact** written to the environment. The receiving session starts with zero context.

**Q: When is a handoff the right tool?**
A: When the work has to travel: to a new harness, a different directory, a colleague, or a parallel side task. If nothing is travelling, compact or clear is usually enough.

**Q: What makes a good handoff artifact?**
A: It is written for a reader with zero context: concrete file paths, decisions and why they were made, what is done, what is left, and the next step. It references specs and diffs instead of copying them.

**Q: Why must a handoff record the "why"?**
A: Otherwise the new session relitigates settled decisions. It sees what was decided but not the reasoning, so it reopens the question instead of continuing the work.

**Q: What should a handoff never contain?**
A: Secrets, tokens, passwords, or unverified claims presented as facts. The next agent trusts the document, so a belief written as a fact becomes a false premise.

**Q: How do you use a handoff artifact?**
A: Start the fresh session by pointing at the file: read it, then continue. Point at the path rather than pasting the summary into a shell command, which can mangle backticks and substitutions.

### Clear, Compact, Handoff, or Subagent

**Q: What does clearing preserve?**
A: Nothing from the session. It ends the conversation and starts with an empty context; only files in the environment survive.

**Q: What does compacting preserve?**
A: Your intent, compressed into a summary. It is the right default at a phase boundary when the work stays in the same place.

**Q: What does a handoff preserve?**
A: The work's ability to move. It writes a portable artifact that a different session, directory, harness, or person can read.

**Q: What does a subagent preserve?**
A: The parent's context. The subagent absorbs noisy work in its own window and returns only a report, with a return path to the parent.

**Q: How do you choose among them?**
A: Continuing is the default. For the boundary cases: clear when the task is done and the context is noisy; compact when the task continues and you need the intent; hand off when the work must travel; delegate to a subagent when the work is noisy but bounded.

**Q: What do all four have in common?**
A: They are ways of managing the context budget. The mistake is pushing through a bloated session because none of them feels necessary yet.

### Auto-Compaction

**Q: What is autocompaction?**
A: Compaction triggered automatically when the context approaches full, often around 80%. The harness asks the model to summarise the session and continues in a fresh window.

**Q: Why is autocompaction risky?**
A: It fires at a moment you did not choose, possibly mid-refactor, and the summary decides what to keep. The agent can continue confidently while missing a constraint you established earlier.

**Q: What is the classic symptom?**
A: The agent keeps working but starts contradicting an old decision, and you only notice when the work has already drifted. It looks like disobedience; it is lost context.

**Q: How do you prevent autocompaction?**
A: Watch the context indicator, compact manually at a natural boundary, and write important decisions to disk before the window fills. You can also adjust or disable the threshold in the harness.

**Q: What should you do after autocompaction fires?**
A: Reload the plan or handoff document, restate the constraints that matter, and verify the next step against the primary source. Do not assume the summary kept what you needed.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Starting context | System prompt, instructions, tools, and repo tree loaded before you speak |
| Context bloat | Loaded content that does not serve the current task |
| Status line | Harness display of model, tokens, and context usage |
| Codebase exploration | Reading structure, patterns, and tests before changing code |
| `/teach` | Skill that builds a persistent teaching workspace |
| Plan mode | Read-only mode that blocks edits and encourages planning |
| Grilling | Socratic interview until the design concept is shared |
| Prototyping | Building a rough artifact to settle an ungrillable question |
| Compaction | Summarising a session into a fresh context |
| Handoff | Transferring context to another session via an artifact |
| Handoff artifact | File with paths, decisions, status, and next steps |
| Clearing | Ending a session with no carry-over |
| Subagent | Child agent with isolated context and a report back |
| Autocompaction | Automatic compaction when the window nears full |
| Primary source | The code, transcript, or raw result itself |
| Secondary source | A summary or account of a primary source |

---

*Study aid; for authoritative content, refer to the official AI Hero course.*
