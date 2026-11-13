# AI Coding Crash Course — Shipping — Q&A

Fast-reference notes for Matt Pocock's *AI Coding Crash Course* (AI Hero).
**How to Tackle Massive Tasks → Set Up Your Issue Tracker → Write Great Specs With This Skill → Split Features Across Context Windows With Tickets → Executing Your Tickets → Should You Keep Your Specs? → Rerouting: When the Destination Changes → The Goal Command → Enforcing Your Coding Standards → The /implement-spec Skill → Ask Matt → Where You Go From Here → More Exercises.**

---

## Part 6 — Shipping

### How to Tackle Massive Tasks

**Q: Why can't a massive task be done in one session?**
A: The context fills, attention degrades, and the agent drifts into the dumb zone long before the work is done. Big work has to be split across sessions.

**Q: What is the high-level workflow for large work?**
A: Grill the idea, write a **spec**, split it into **tickets**, execute one ticket per session, and review each result. The spec survives; the sessions are disposable.

**Q: What is the biggest risk in a large build?**
A: Building the wrong thing perfectly. The spec and grilling exist to make sure the destination is right before the agent spends hours getting there.

**Q: What does "software factory" mean?**
A: A system where sessions are started by triggers such as an issue being labelled or a CI failure, rather than by a human opening each session. Start small: one trigger, one reviewable PR.

### Set Up Your Issue Tracker

**Q: Why does the agent need an issue tracker?**
A: The tracker is where the spec and tickets live. It gives every fresh session a durable place to read the work, its status, and its dependencies.

**Q: What tracker options work?**
A: A real tracker such as GitHub or Linear, or local Markdown files under a scratch directory. The important part is a stable place for tickets and blocking edges, not the vendor.

**Q: What is a blocking edge?**
A: A dependency between tickets: ticket B cannot start until ticket A is done. The set of tickets with no open blockers is the **frontier**, and that is what can run now.

### Write Great Specs With This Skill

**Q: What is a spec?**
A: A **handoff artifact** describing a multi-session piece of work: what is being built, the constraints, the decisions made so far, and the tickets with their status.

**Q: What should a spec contain?**
A: The goal, the user-facing behaviour, the constraints, the decisions and their reasons, the out-of-scope list, the agreed seams, and the ticket breakdown.

**Q: How does a spec get written?**
A: Start from a grilling conversation and record what was decided. The spec should not invent decisions; if it states something you never agreed, that is a defect.

**Q: Why record the "why" as well as the "what"?**
A: A fresh session that sees only the decision will relitigate it. The reasoning prevents the next session from reopening questions that were already settled.

**Q: What is a seam?**
A: A boundary where the feature will be tested. Prefer existing seams, pick the highest seam that works, and aim for one seam per change.

**Q: Why is the out-of-scope list important?**
A: The things you deliberately refused are often the most useful lines in the spec. They stop the agent from quietly adding scope you already rejected.

### Split Features Across Context Windows With Tickets

**Q: What is a ticket?**
A: A **handoff artifact** scoping one session of work. It has a goal, acceptance criteria, context pointers, and blocking edges to other tickets.

**Q: What is the size rule for a ticket?**
A: It must fit in one fresh context window and one session. If sessions routinely degrade before the ticket is done, the ticket is too big; if setup dominates, it is too small.

**Q: What is a tracer bullet?**
A: A narrow but complete vertical slice through every layer of the change: schema, API, UI, and tests. It can be demoed on its own as soon as it lands.

**Q: Why not slice by layer?**
A: A horizontal slice ships nothing until every layer lands, and each ticket's acceptance criteria reach into work another ticket owns. That produces integration pain and rework.

**Q: How do you order the tickets?**
A: Follow the dependency graph, not a linear list. Prefactoring comes first, then the tickets whose blockers are done. The frontier determines what can run in parallel.

**Q: What should every ticket answer?**
A: "What can I demo when this is done?" If the answer is a layer or a file rather than behaviour, the ticket is probably a horizontal slice.

**Q: What is prefactoring?**
A: Making the change easy before making the easy change: a small preparatory refactor that reduces the risk of the feature tickets. It should be ordered first.

**Q: How do you prevent over-decomposition?**
A: Quiz the breakdown before publishing: merge tickets that only make sense together, split ones that cannot finish in a session, and check that every blocking edge is real.

### Executing Your Tickets

**Q: How do you execute a ticket?**
A: Start a fresh session, point it at the ticket, read the referenced files, implement in small steps, run the checks, and review the diff. Then update the ticket's status.

**Q: Why a fresh session per ticket?**
A: Each ticket gets the sharpest part of a context window. The previous ticket's exploration and wrong turns do not become residue that colours the next one.

**Q: What should the agent do first?**
A: Read the ticket and its context pointers, then confirm the acceptance criteria and the tests that will prove them. It should not start editing before it understands the target.

**Q: How does TDD fit in?**
A: Write a failing test at the agreed seam, make it pass, then refactor. The red-green loop gives the agent deterministic feedback and gives you evidence that the behaviour exists.

**Q: What is the review checkpoint?**
A: Read the diff before merging, not just the agent's summary. Automated checks catch mechanical failures; human review decides whether the change is the right change.

### Should You Keep Your Specs?

**Q: Should a spec be kept forever?**
A: No. It is a snapshot of what you knew when the work started, and it goes stale as implementation teaches you more. Treat it as disposable after the work ships.

**Q: What should survive instead?**
A: Durable decisions belong in ADRs, a glossary, or project documentation. The spec records one effort; those files record knowledge that outlives it.

**Q: Why do tickets get deleted or closed?**
A: They are disposable slices sized for one session. Once the work lands, the ticket has served its purpose; keeping it adds maintenance without adding value.

**Q: Why does this matter for agents?**
A: Agents trust the documents you give them. A stale spec is a confident false premise, and the next session will build on it unless you mark or remove it.

### Rerouting: When the Destination Changes

**Q: What should you do when the goal changes mid-build?**
A: Update the spec to the new destination, re-grill the parts that are now unclear, and delete or rewrite the unfinished tickets. Keep the completed work where it is still valid.

**Q: Why not just tell the current session to change direction?**
A: The current session carries the old reasoning and the old context. A fresh session reading the updated spec is less likely to keep building toward the abandoned goal.

**Q: What should happen to completed tickets?**
A: Keep them if they still serve the new destination; otherwise mark them as superseded. Do not silently reuse work that was designed for a different requirement.

### The Goal Command

**Q: What is the `/goal` command?**
A: A lightweight way to state the desired end state for the agent. It is useful as a persistent reminder of what "done" means, especially after a long session or a compaction.

**Q: What does `/goal` not do?**
A: It does not plan the work, split it into sessions, or guarantee that the agent stays on track. A goal statement is not a spec and not a ticket graph.

**Q: When is a goal statement useful?**
A: For short, well-scoped work where the destination is clear, and as a repeated check at the start of each turn. It keeps the agent from drifting into adjacent improvements.

**Q: How do you make a goal statement effective?**
A: Include the success criteria and the constraints, not just the outcome: "add CSV export with these columns, no new dependencies, tests pass". Pair it with automated checks.

### Enforcing Your Coding Standards

**Q: Why are coding standards important with agents?**
A: Agents produce volume, and volume amplifies inconsistency. Standards keep the codebase navigable and make the agent's output easier to review and extend.

**Q: How do you enforce standards mechanically?**
A: Use **automated checks**: types, tests, lint, formatting, and build. They are deterministic, so the agent can self-correct from their output without a human.

**Q: What belongs in `AGENTS.md` for standards?**
A: The rules the agent cannot infer: naming conventions, architectural boundaries, generated files not to edit, and the commands that verify the work.

**Q: What is the role of review?**
A: Automated checks catch what can be asserted; human review catches whether the change fits the codebase and whether it should exist. Reserve human attention for judgement.

**Q: What is the strongest enforcement layer?**
A: CI plus a protected branch. If the checks run before merge, the agent cannot land work that violates the mechanical standards, regardless of what it claims.

### The /implement-spec Skill

**Q: What is `/implement-spec`?**
A: A skill that takes a spec and its tickets and lands the whole thing in one run. It hands each ticket to an implementer subagent with its own git worktree, then merges the results into an integration branch.

**Q: How does it decide what to run first?**
A: It reads the tickets as a task graph, not a list. Blocking edges define a **frontier** of tickets whose blockers have landed, and every ticket on the frontier runs at once.

**Q: Why use subagents and worktrees?**
A: Each ticket gets an isolated context and an isolated branch, so parallel work does not pollute the parent's context or collide in the working tree. The parent keeps the graph and the integration branch.

**Q: What does each implementer do?**
A: Confirm it is based on the integration branch, build the ticket with TDD, merge the integration branch tip into its own branch, and report done. That keeps the final merge fast-forward.

**Q: When should you use `/implement-spec`?**
A: When you have a spec split into tickets with real blocking edges and a harness that runs subagents in the background with worktrees. For one ticket at a time, use the simpler implementation flow.

**Q: What are the risks of parallel implementers?**
A: Two tickets can touch the same file or pick different names for the same concept. Add a blocking edge or fix the shared names in the exploration notes before running them in parallel.

**Q: What is the common false signal in worktrees?**
A: A test can silently skip because a gitignored fixture, local database, or credential is missing from the worktree. Verify the test actually ran, not just that the suite was green.

### Ask Matt

**Q: What is `/ask-matt`?**
A: A router skill that helps you choose the right workflow or skill for the situation. It is useful when you know the goal but not whether to grill, spec, ticket, implement, or review.

**Q: When should you use it?**
A: At a decision point: the work is fuzzy, the plan is too big, or you are unsure whether a spec is needed. It saves you from forcing the wrong process onto the task.

### Where You Go From Here

**Q: What should you practice after the course?**
A: Run the full loop on your own repository: grill a feature, write a spec, split it into tickets, implement them in fresh sessions, and review each diff.

**Q: How do you build the habit of context management?**
A: Watch the context indicator, clear between tasks, compact at phase boundaries, and write decisions to disk. Treat the smart zone as a budget you spend deliberately.

**Q: How do you get better at steering?**
A: Prune `AGENTS.md`, turn repeated prompts into skills, and add pointers instead of pasted docs. Review the always-loaded context regularly.

**Q: How do you safely try AFK work?**
A: Start with a well-specified, low-risk ticket, a sandbox, a permissive permission mode, and automated checks. Review the PR in the morning before merging.

**Q: What is the durable skill from the course?**
A: The loop: understand the model and harness, curate context, grill the requirements, split the work, verify mechanically, and review the result. The tools change; the loop transfers.

### More Exercises

**Q: How can you reuse the course exercises?**
A: Reset to a checkpoint, rebuild the lesson without looking at the solution, then cherry-pick the solution and compare. The gap between your attempt and the solution is the lesson.

**Q: What is a good self-directed exercise?**
A: Pick a small feature in the exercise repo, grill it, write a spec and three tickets, implement one ticket per session, and review the integration. Repeat with a larger feature.

**Q: How do you practice context management deliberately?**
A: Start a task, watch the context grow, and compact or hand off at a boundary before the agent degrades. Compare the result with pushing through the same task in one session.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Massive task | Work too large for one context window and one session |
| Spec | Durable multi-session statement of intent and decisions |
| Ticket | One-session unit of work with acceptance criteria and blockers |
| Blocking edge | Dependency that must finish before a ticket can start |
| Frontier | Tickets whose blockers are done and can run now |
| Tracer bullet | Vertical slice through every layer, demoable on its own |
| Prefactoring | Making the change easy before making the easy change |
| Seam | Boundary where the feature is tested |
| Rerouting | Updating the spec and tickets when the destination changes |
| `/goal` | Short statement of the desired end state, not a plan |
| Automated check | Deterministic verification such as types, tests, or lint |
| `/implement-spec` | Runs a ticket graph with parallel implementer subagents |
| Integration branch | Branch where parallel ticket branches are merged |
| Worktree | Isolated checkout for a subagent's ticket |
| Software factory | Sessions started by triggers instead of a human |

---

*Study aid; for authoritative content, refer to the official AI Hero course.*
