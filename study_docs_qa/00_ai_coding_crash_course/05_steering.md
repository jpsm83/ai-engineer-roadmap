# AI Coding Crash Course — Steering — Q&A

Fast-reference notes for Matt Pocock's *AI Coding Crash Course* (AI Hero).
**The Steering Map → Steering With a Pointer → What Are Agent Skills? → Write a Skill → User vs. Project Skills → Navigation Pointers → Pruning → Trying Out Pruning → Claude Code's Automatic Memory.**

---

## Part 5 — Steering

### The Steering Map

**Q: What is steering?**
A: Shaping what the agent does and how it does it without rewriting the prompt every turn. Steering includes instructions, context, tools, permissions, checks, and the files the agent can read.

**Q: What is the steering map?**
A: A way to choose the right layer: always-on instructions in `AGENTS.md` or `CLAUDE.md`, on-demand instructions in **skills**, references through **context pointers**, cross-session facts in memory, and hard limits through permissions.

**Q: Why not put everything in one instruction file?**
A: Everything in the always-on layer is billed on every request and dilutes attention. A long file makes the agent worse at following any single instruction.

**Q: What is the first question to ask about an instruction?**
A: "Is this true for every task in this repo?" If yes, it belongs in `AGENTS.md`. If only for some tasks, put it in a skill or behind a pointer.

**Q: What belongs in `AGENTS.md`?**
A: Build and test commands, non-obvious conventions, hard constraints such as "never edit the generated client", and pointers to deeper docs. Short and declarative.

**Q: What does `AGENTS.md` have to do with `CLAUDE.md`?**
A: `AGENTS.md` is the cross-harness convention; `CLAUDE.md` is Claude Code's variant. Keep one source of truth and point or symlink the other to it so the instructions do not drift.

**Q: How do permissions fit the steering map?**
A: Permissions are the hard boundary. Instructions shape what the agent wants to do; permissions decide what it is allowed to do, and a sandbox limits the damage if it does.

### Steering With a Pointer

**Q: What is a context pointer?**
A: A line in one document that names another file and says when to read it. It costs one line in the window and pulls in the full content only when the task calls for it.

**Q: What are the two parts of a useful pointer?**
A: A stable path and enough description to know when following it is worth it. A bare path with no hint gets skipped by the session that needed it.

**Q: How do you write a good pointer?**
A: Match the language of the task: "release, deploy, or rollback: read `internal/deploy.md` first". Name the path and the trigger together.

**Q: Why is a pointer better than inlining?**
A: An inlined document is paid for on every request, whether or not it is relevant. A pointer is almost free until the agent follows it.

**Q: Where do pointers appear?**
A: Lines in `AGENTS.md`, skill descriptions, filenames in a directory listing, links between docs, and a **Home Repo** naming its other repositories.

**Q: What is the risk of a pointer?**
A: It can point at stale content. The pointed-to document is still a source that can drift, so keep it current and prefer the primary source when behaviour matters.

### What Are Agent Skills?

**Q: What is an agent skill?**
A: A packaged capability: a folder with a `SKILL.md` file containing metadata and instructions, plus optional scripts, templates, and reference material. It is loaded only when the task matches.

**Q: How does the harness know when to load a skill?**
A: Only the name and description sit in context by default. When the task matches the description, the agent reads the rest of the skill.

**Q: Why are skills useful?**
A: They apply **progressive disclosure**. A large runbook can live on disk and cost almost nothing until a deploy task needs it.

**Q: What is the difference between a skill and a tool?**
A: A tool is something the agent calls; a skill is instructions it reads. A skill can tell the agent which tools to use and in what order.

**Q: What is the difference between a skill and `AGENTS.md`?**
A: `AGENTS.md` is always loaded; a skill is loaded on demand. Use `AGENTS.md` for rules that apply everywhere and skills for task-specific procedures.

**Q: Are skills portable across harnesses?**
A: The skill format is an open standard, so a skill written once can work across compatible harnesses. The exact loading and invocation behaviour can still vary, so test it in your harness.

### Write a Skill

**Q: What does a skill need at minimum?**
A: A name, a description that says when to use it, and the instructions themselves. Scripts and templates are optional but useful for repeatable work.

**Q: What makes a skill description effective?**
A: It names the trigger in the user's language: "use when releasing, deploying, or rolling back". The agent chooses based on the description, so vague descriptions produce missed or spurious loads.

**Q: How should the instructions be written?**
A: As a short, ordered procedure with concrete commands, paths, and examples. One skill should do one job well rather than covering a whole department.

**Q: How do you test a skill?**
A: Invoke it on a real task, check that it loads at the right time, and verify that the output follows the steps. A skill that is never loaded is documentation, not a capability.

**Q: What should you do when a prompt or workflow repeats?**
A: Turn it into a skill. Capture the steps, the constraints, and the checks, then replace the repeated prompt with a single invocation.

**Q: What is the most common skill mistake?**
A: Writing a long essay instead of an executable procedure. The agent needs enough detail to act, not a history of the topic.

### User vs. Project Skills

**Q: What is a user-level skill?**
A: A skill installed in your personal scope, such as `~/.claude/skills`. It follows you across projects and is not part of any repository.

**Q: What is a project-level skill?**
A: A skill stored in the repository, such as `.claude/skills` or `.agents/skills`. It is shared with the team, versioned with the code, and reviewed like any other project asset.

**Q: When should a skill be project-level?**
A: When it encodes project-specific procedures: how to deploy this service, how to write a migration here, or how this codebase's tests are structured.

**Q: When should a skill be user-level?**
A: When it is a personal workflow that applies across repositories, such as a preferred review checklist or a general research routine.

**Q: What is the risk of copying skills into every repo?**
A: The copies drift. A **Home Repo** keeps one copy of shared skills and instructions, and points at the other repositories instead.

**Q: What is a Home Repo?**
A: A repository that holds shared skills, `AGENTS.md`, and cross-repo docs, with pointers to the other repos. You start sessions there so the agent has one consistent setup.

### Navigation Pointers

**Q: What is a navigation pointer?**
A: A pointer that tells the agent where something lives: "billing logic is in `app/services/billing.ts`; invoice rendering is in `app/routes/invoices.tsx`". It reduces search and prevents edits in the wrong place.

**Q: Why are navigation pointers useful in a large codebase?**
A: The agent sees filenames, not the whole codebase. A good pointer turns a broad search into a direct read and keeps the context smaller.

**Q: Where should navigation pointers live?**
A: In `AGENTS.md` for the few areas every task touches, and in skills or docs for area-specific maps. Keep the always-on list short.

**Q: How do you keep navigation pointers accurate?**
A: Update them when files move, and prefer pointing at directories or stable entry points rather than line numbers. A stale pointer is worse than no pointer because it sends the agent confidently to the wrong place.

**Q: What is the difference between a navigation pointer and a context pointer?**
A: A navigation pointer locates code or docs; a context pointer is the general mechanism of naming something to load later. Every navigation pointer is a context pointer with a location as its target.

**Q: How do pointers help with context bloat?**
A: They replace pasted content with a one-line reference. The agent reads only what the current task needs, which keeps the window free for the work.

### Pruning

**Q: What is pruning?**
A: Removing stale, redundant, or rarely relevant content from the always-loaded layer. It is context maintenance, not deleting the underlying documentation.

**Q: Why prune `AGENTS.md`?**
A: Every line is loaded on every request in every session. A long file costs tokens, dilutes attention, and makes the important rules harder to follow.

**Q: What should you prune first?**
A: Instructions the code already makes obvious, rules that apply to only one task, duplicated guidance, and facts that have changed. Move task-specific detail into skills.

**Q: What should you never prune?**
A: Hard constraints, unusual build or test commands, and safety rules that the agent cannot infer. Prune noise, not the information that prevents expensive mistakes.

**Q: How do you know pruning worked?**
A: The starting context is smaller, the agent follows the remaining rules more reliably, and the same tasks still pass their checks. Measure both context size and behaviour.

**Q: What is the connection between pruning and memory?**
A: Memory systems accumulate facts, and stale memories are loaded with the same confidence as current ones. A memory system needs pruning for the same reasons `AGENTS.md` does.

### Trying Out Pruning

**Q: What is a practical pruning exercise?**
A: Take `AGENTS.md` or `CLAUDE.md`, mark each line as always true, task-specific, or derivable, then move the task-specific lines into skills and delete the derivable ones.

**Q: How do you measure the before and after?**
A: Check the context display or request logger before and after, and run a representative task. The goal is a smaller starting context with no loss in correctness.

**Q: What should you do with the removed content?**
A: Move it to a skill, a referenced doc, or a pointer. Pruning is relocation when the knowledge is still useful; it is deletion only when the knowledge is stale or obvious.

**Q: Why is pruning hard to do once?**
A: Instructions accumulate again as you correct the agent. Make pruning a periodic habit, especially after a project change or a new recurring correction.

**Q: What is the safest way to prune a critical instruction?**
A: Move it behind a pointer first, verify the agent still follows it when the task triggers the pointer, then remove the inline copy. Do not delete a safety rule until the replacement works.

### Claude Code's Automatic Memory

**Q: What is Claude Code's automatic memory?**
A: A memory feature that records facts and preferences across sessions and reloads them at session start. `/memory` opens the memory and instruction files for review and editing.

**Q: What does automatic memory help with?**
A: It reduces repetition of stable facts: your preferred package manager, a project convention, or a correction you keep making. It is continuity layered on a stateless model.

**Q: What is the risk of automatic memory?**
A: It accumulates. Old facts are loaded with the same confidence as new ones, and an outdated preference can quietly steer every session. Review and prune it regularly.

**Q: How does automatic memory differ from `AGENTS.md`?**
A: Memory is personal and learned over time; `AGENTS.md` is deliberate project instruction shared with the team. Use `AGENTS.md` for rules that every contributor needs.

**Q: How does automatic memory differ from a skill?**
A: Memory is always-loaded context about you and the project; a skill is task-specific instructions loaded on demand. Do not put a procedure in memory when it belongs in a skill.

**Q: What is the right way to use memory?**
A: Treat it as a secondary source: read it, correct it, and remove stale entries. If a fact matters to everyone, promote it to `AGENTS.md` or a project doc instead of leaving it in personal memory.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Steering | Shaping agent behaviour through instructions, context, tools, and permissions |
| Steering map | The layers: always-on instructions, skills, pointers, memory, permissions |
| `AGENTS.md` | Cross-harness always-loaded project brief |
| `CLAUDE.md` | Claude Code's variant of the project brief |
| Progressive disclosure | Loading only what the current task needs |
| Context pointer | A named reference the agent follows when relevant |
| Skill | A folder of on-demand instructions and optional resources |
| `SKILL.md` | The metadata and instruction file inside a skill |
| User skill | Personal skill available across projects |
| Project skill | Repository skill shared and versioned with the code |
| Navigation pointer | A pointer that locates code or documentation |
| Pruning | Removing stale or irrelevant content from always-loaded context |
| Memory system | Files that persist facts across sessions and reload them |
| `/memory` | Claude Code's interface for reviewing memory and instruction files |
| Home Repo | Shared repo holding skills and pointers to other repos |

---

*Study aid; for authoritative content, refer to the official AI Hero course.*
