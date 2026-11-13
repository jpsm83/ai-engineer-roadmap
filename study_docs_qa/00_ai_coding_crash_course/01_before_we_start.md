# AI Coding Crash Course — Before We Start — Q&A

Fast-reference notes for Matt Pocock's *AI Coding Crash Course* (AI Hero).
**Where We're Going → Choosing Your Plan and Model → Setting Up the Project → Installing Claude Code → How to Run the Exercises → Database Migrations → Resetting to a Clean Slate → Installing the Request Logger → Navigating the Discord.**

---

## Part 1 — Before We Start

### Where We're Going

**Q: What is the core idea of the course?**
A: Learn how the **model** works, how the **harness** works, and how to combine both into a repeatable software engineering loop. The goal is control and predictable quality, not faster prompting.

**Q: What does "this isn't a vibe coding course" mean?**
A: You are expected to read diffs, understand the code, and enforce standards. **Vibe coding** accepts agent output without human review; this course teaches the opposite habit.

**Q: What will you build during the course?**
A: A full-stack exercise repo that works like a mini Udemy: React Router, TypeScript, SQLite, and Drizzle ORM. You explore, extend, and refactor it with Claude Code.

**Q: How is the course organized?**
A: Six sections and nearly 60 lessons. Each lesson has a video, a written guide, prompts to adapt, and quizzes; code lessons have checkpoint commits you can reset to.

**Q: How should you pace the course?**
A: Either marathon it over about three days or spread it across a week at a few hours a day. One lesson per sitting works better than bingeing, because each lesson builds on the last.

**Q: What is the main failure mode the course prevents?**
A: Producing code faster than you can review it. The agent never gets tired, but your attention is the bottleneck; steady, reviewed progress beats a large unreviewed branch.

### Choosing Your Plan and Model

**Q: What do you need before starting?**
A: Node.js 22 or newer, Git, the Claude Code CLI, and a Claude Pro or Max subscription. A paid plan gives you enough usage to work through the exercises.

**Q: How should you choose a model tier?**
A: Use a **frontier** model for planning, ambiguous design work, and hard debugging, and a smaller, cheaper model for mechanical edits. The best model is the cheapest one that reliably does the task.

**Q: What is the model's "effort" setting?**
A: **Effort** controls how much reasoning the model does before answering. Higher effort costs more and runs slower; use it for reasoning-heavy work and lower it for rote changes.

**Q: Why not always use the biggest model at maximum effort?**
A: Cost and latency scale with both. A one-line rename does not need maximum reasoning, and using it there wastes time without improving the result.

**Q: When should you switch models mid-session?**
A: Switch when the task changes character: a heavy model for the plan, a lighter one for repetitive edits, then back for review. The harness keeps the conversation, so the switch is cheap.

### Setting Up the Project

**Q: What are the setup commands?**
A: Clone the exercise repo, then run `npm install`, `npm run db:migrate`, `npm run db:seed`, and `npm run dev`. The app runs at `http://localhost:5173`.

**Q: What does each setup command do?**
A: `npm install` installs dependencies, `db:migrate` creates the SQLite schema, `db:seed` inserts demo data, and `dev` starts the Vite development server.

**Q: Where should you run Claude Code?**
A: From the project root. The agent then sees the repository tree, `AGENTS.md` or `CLAUDE.md`, and the scripts it needs, and its reads and edits land in the right files.

**Q: Why keep the exercise repo separate from real work?**
A: The course asks you to reset, cherry-pick, and experiment. Keeping it separate makes destructive checkpoints safe and keeps your own projects clean.

### Installing Claude Code

**Q: What is Claude Code?**
A: A coding **harness** that wraps a Claude model with filesystem tools, a Bash tool, search, permissions, and context management. It is the agent you talk to in the terminal.

**Q: How do you install and start it?**
A: Install the CLI with the official installer, authenticate with your Claude account, then run `claude` inside the project. The first run walks you through login and trust prompts.

**Q: How do you verify the setup?**
A: Ask the agent to read the project's `package.json` and list the available scripts, or run `claude --version`. If it can see the repo and run `npm run test`, the harness is wired correctly.

**Q: Why does the harness matter more than the model name?**
A: The same model in Claude Code, Cursor, or Claude.ai behaves differently because the **system prompt**, tools, permissions, and context handling differ. Most "model" surprises are harness differences.

### How to Run the Exercises

**Q: What is a lesson checkpoint?**
A: A commit on the `live-run-through` branch addressed by the lesson **slug**. It marks the exact repo state where that lesson starts or ends.

**Q: What does `npm run reset <slug>` do?**
A: It resets the repository to that lesson's checkpoint. The reset is destructive, so commit or stash your own work first with `git status` and `git stash`.

**Q: What does `npm run cherry-pick <slug>` do?**
A: It applies a lesson's solution commit, letting you skip ahead or compare your work with the intended result. Use it after trying the exercise, not instead of trying it.

**Q: What should you do before a reset?**
A: Check `git status`, commit anything you want to keep, and make sure you are on the expected branch. A clean working tree makes a failed exercise easy to retry.

**Q: How should you use the written guide and quizzes?**
A: Read the guide before watching the video, attempt the quiz without notes, and revisit the video only for the parts that did not stick. Active recall beats passive rewatching.

### Database Migrations

**Q: What is a database migration?**
A: A versioned, ordered change to the database schema. `npm run db:migrate` applies any migrations that have not run yet, so every environment reaches the same schema.

**Q: Why never edit an applied migration?**
A: Other environments have already recorded that migration as run, so changing it makes their schema diverge from yours. Add a new migration instead.

**Q: What does seeding do?**
A: `npm run db:seed` inserts demo users, courses, lessons, and related records so the app has realistic data. Re-seeding usually rebuilds that demo data from scratch.

**Q: Where does the data live?**
A: In a local SQLite database file using Drizzle ORM. Because it is a file, resets and seeds are fast and do not require a separate database server.

**Q: Why does the course teach migrations early?**
A: Schema changes are a common agent task and a common way to break a codebase. Seeing how migrations are versioned teaches you to ask for a new migration instead of a direct table edit.

### Resetting to a Clean Slate

**Q: When should you reset to a checkpoint?**
A: When your branch has drifted, an experiment failed, or you want to replay a lesson from its exact starting point. A clean slate makes the lesson reproducible.

**Q: What is the difference between reset and cherry-pick?**
A: **Reset** moves the repo back to a lesson checkpoint and discards later work; **cherry-pick** brings a specific solution commit onto your current branch.

**Q: What should you do if you want to keep your attempt?**
A: Commit it to a branch or stash it before resetting. Git is the safety net; the checkpoint command is not a backup.

**Q: Why is a clean repo important for learning?**
A: It separates your mistakes from pre-existing state. When a test fails after a reset, you know the failure came from the lesson, not from leftover edits.

### Installing the Request Logger

**Q: What is the request logger?**
A: A local proxy that sits between your agent and the model provider and writes a readable Markdown file for every real request. It shows the actual system prompt, tool definitions, and messages sent to the model.

**Q: How do you run it?**
A: Run `npm run request-logger` in the exercise repo. The wizard asks which agent and provider you use, then prints the exact command to start your agent through the proxy.

**Q: Where do the logs go?**
A: Into `request-logger/logs/`, with a readable `.md` render plus the raw request and response files. The folder is gitignored and safe to delete.

**Q: What does the logger not record?**
A: Housekeeping calls such as token counting are forwarded but not logged. Only real turns that produce model output get a capture, so the log reflects what actually mattered.

**Q: Why use the request logger?**
A: It turns guesses about context into evidence. You can see how large the system prompt is, which tools are loaded, what the agent actually sent, and where tokens and cache discounts went.

**Q: What is the observer effect in the logger?**
A: Pointing Claude Code away from its normal host can disable tool search, which makes the captured request larger than a real one. The printed command sets `ENABLE_TOOL_SEARCH=true` to counteract this.

**Q: What if the logs folder stays empty?**
A: Check that the agent was started with the printed command, that the agent and provider choices are correct, and that the agent was not already running before the environment variables were set.

### Navigating the Discord

**Q: How should you ask for help?**
A: Search the channel first, then post the smallest reproducible example: the command, the error, and the relevant file or lesson slug. Avoid pasting entire transcripts.

**Q: What should you never share?**
A: API keys, tokens, passwords, customer data, or private repository contents. Redact secrets before posting logs or screenshots.

**Q: Where should questions go?**
A: In the channel for the relevant section or lesson, not in a general chat. Course-specific channels keep answers searchable for other students.

**Q: What is the fastest way to get unstuck?**
A: Reset to the lesson checkpoint, reproduce the failure, and ask a specific question with the exact step where it diverged. "It doesn't work" cannot be diagnosed; a checkpoint and an error can.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Model | The frozen parameters that perform next-token prediction |
| Harness | Everything around the model: tools, system prompt, context, permissions |
| Agent | A model plus a harness, taking turns with you |
| Environment | The workspace the agent acts on, usually the filesystem |
| Context window | The token sequence the model sees on each request |
| Session | One bounded run of interaction that fills the context window |
| Turn | One user message plus everything the agent does in response |
| Checkpoint | A commit on `live-run-through` addressed by a lesson slug |
| Slug | The stable identifier used by `reset` and `cherry-pick` |
| Migration | A versioned schema change applied by `db:migrate` |
| Seed | Demo data inserted by `db:seed` |
| Exercise repo | The full-stack app used for the course's code lessons |
| Request logger | Local proxy that records real model requests as Markdown |
| Claude Code | Terminal harness that turns Claude into a coding agent |

---

*Study aid; for authoritative content, refer to the official AI Hero course.*
