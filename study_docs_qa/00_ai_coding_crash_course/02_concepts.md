# AI Coding Crash Course — Concepts — Q&A

Fast-reference notes for Matt Pocock's *AI Coding Crash Course* (AI Hero).
**Models, Harnesses, Agents, Environments → Non-Determinism → Turns and Model Provider Requests → Sessions and the Context → Smart Zone / Dumb Zone → Statelessness → How Much Did It Cost? → Hallucination → Effort → Choosing a Model → Subagents.**

---

## Part 2 — Concepts

### Models, Harnesses, Agents, Environments

**Q: What is a model?**
A: The **parameters** — the frozen numbers produced by training. A model is stateless and does only **next-token prediction**: tokens in, one likely next token out, repeated.

**Q: What is a harness?**
A: Everything around the model that turns it into an agent: tools, the **system prompt**, context-window management, permissions, and the loop that executes tool calls.

**Q: What is an agent?**
A: A model plus a harness, addressed as one actor. Claude Code and Cursor are agents; the same model in a different harness behaves differently.

**Q: What is the environment?**
A: The world the agent acts on, usually a **filesystem**. The agent perceives it only through tool results and changes it only through tool calls.

**Q: Why is the model alone not an agent?**
A: It cannot read a file, run a command, browse, or remember the last turn. The harness supplies all of that, including re-sending the conversation on every request.

**Q: Why does the same model behave differently in two products?**
A: Different harnesses use different system prompts, tools, permission defaults, and context strategies. Diagnose the harness before blaming the model.

**Q: Why does the agent sometimes describe a file that has changed?**
A: It is reasoning from an old **tool result**. The environment moved, but the snapshot in context did not; the agent only sees the environment when it looks again.

### Non-Determinism

**Q: What is non-determinism?**
A: The same prompt can produce different output on different runs. The model samples the next token from a probability distribution rather than always picking the single most likely one.

**Q: Is non-determinism a bug?**
A: No — it is built into generation. It is why the same task may take a different path, and why "it worked yesterday" is not evidence that the prompt is stable.

**Q: How should you handle non-determinism?**
A: Make the task more constrained: give exact files, acceptance criteria, and checks. Deterministic **automated checks** turn a fuzzy generation into a pass/fail signal.

**Q: Why can the same prompt fail only sometimes?**
A: A small early difference changes the tokens that follow, and the error compounds. Long, open-ended tasks magnify this; short, testable steps contain it.

### Turns and Model Provider Requests

**Q: What is a model provider request?**
A: One round-trip from the harness to the provider. The harness sends the full context, and the provider returns one response: a tool call or a final answer.

**Q: What is a turn?**
A: One user message plus everything the agent does before yielding back to you. A turn can contain many model provider requests when the agent calls tools.

**Q: What is the hierarchy?**
A: **Session > turn > model provider request.** A session holds many turns; a turn holds one or more requests.

**Q: Why can one short question cost so much?**
A: Every tool call triggers another request, and every request re-sends the whole session as input tokens. Cost tracks requests times context size, not the length of your message.

**Q: Why does the agent take so long on one turn?**
A: It may be chaining many tool calls, and output tokens are generated one at a time. Latency is the sum of those requests plus the time spent writing output.

### Sessions and the Context

**Q: What is a session?**
A: One bounded run of interaction. It starts empty, accumulates messages and tool results, and ends when cleared, closed, or compacted into a fresh session.

**Q: What is context?**
A: The task-relevant information the agent currently has. It is a quality measure, not just a quantity: the right type definition can matter more than thousands of stale log lines.

**Q: What is the context window?**
A: The literal token sequence the model sees on each request: system prompt, conversation, and every tool result. Anything outside it does not exist for the model until a tool call brings it in.

**Q: Why does context fill up so quickly?**
A: Tool results are usually the bulk. Every file read, search, and test run lands in full and stays in the history for the rest of the session.

**Q: What is context engineering?**
A: Curating what enters the window: load what the task needs, keep out what it does not, and replace large content with **context pointers** where possible.

**Q: Why does the agent forget an instruction from earlier?**
A: The instruction is still in context, but **attention degradation** has diluted its influence. The fix is usually to clear or compact, not to paste the instruction again.

### Smart Zone / Dumb Zone

**Q: What is the smart zone?**
A: The early part of a session where the agent is sharp, focused, and good at recall. Attention relationships are least strained and the context is still task-relevant.

**Q: What is the dumb zone?**
A: The later part of a session where quality has degraded: the agent forgets constraints, repeats mistakes, and hallucinates more. On frontier models it often begins around 125K to 150K tokens.

**Q: What causes the dumb zone?**
A: **Attention degradation**. Each token has a finite **attention budget**, and as the context grows, the budget is spread across more competitors, so the signal on what matters gets thinner.

**Q: What are the warning signs?**
A: It forgets an instruction from twenty turns ago, re-asks something it was told, or confidently contradicts the context. The decline is gradual, so there is no clean boundary to notice.

**Q: Does the dumb zone start when the context window is full?**
A: No. Quality falls off long before the hard limit. Plan around the smart zone, not the maximum window size.

**Q: How do you stay in the smart zone?**
A: Do one task per session, keep the context small, clear or compact at natural boundaries, and avoid dumping large files that the task does not need.

### Statelessness

**Q: What does stateless mean?**
A: Carries no information forward. The model is stateless across requests and sessions; the harness manufactures continuity by re-sending or reloading context.

**Q: Is a session stateful?**
A: Yes, across turns: the harness appends messages and tool results to the context. It is not stateful across sessions unless a memory system or handoff reloads something.

**Q: Why does the agent not learn from your correction?**
A: Its parameters are frozen after training. A correction changes only the current context, so it disappears when the session is cleared.

**Q: How do you make a correction persist?**
A: Write it somewhere the next session will read: `AGENTS.md`, a project skill, a memory file, or a handoff artifact. The model cannot remember it on its own.

**Q: What survives when a session ends?**
A: The **environment**, usually the filesystem. Files written during one session can be read by the next; everything else in the context is gone.

### How Much Did It Cost?

**Q: What are input and output tokens?**
A: **Input tokens** are everything the harness sends: system prompt, history, and tool results. **Output tokens** are everything the model generates, including tool calls and hidden reasoning.

**Q: Which costs more?**
A: Output tokens, commonly around five times the input rate, because generating them takes more compute. Input volume is usually larger, so both matter.

**Q: What is the prefix cache?**
A: A provider-side store that reuses an identical request prefix, billing it as cheaper **cache tokens**. It makes long sessions affordable because history is append-only.

**Q: When does the prefix cache break?**
A: When anything earlier in the request changes, such as a reordered system prompt, an updated timestamp, or a changed file representation. Everything after the change is billed at full input rate again.

**Q: Why did the bill spike mid-session?**
A: A broken prefix cache is the usual cause: something near the start of the request changed, so the cache missed and the history was re-processed at full price.

**Q: How do you reduce cost?**
A: Clear or compact between tasks, keep tool results small, avoid unnecessary tool calls, use a cheaper model for mechanical work, and lower effort when the task is simple.

### Hallucination

**Q: What is hallucination?**
A: Confidently wrong model output. It comes in two flavors: **factuality** hallucinations invent facts, and **faithfulness** hallucinations drift from information that is actually loaded.

**Q: What causes factuality hallucinations?**
A: Gaps in **parametric knowledge**, especially past the **knowledge cutoff**. The model guesses from similar patterns and cannot tell that it is guessing.

**Q: What causes faithfulness hallucinations?**
A: **Attention degradation**. The correct information is in context, but it is losing the competition for attention deep into a long session.

**Q: How do you fix each flavor?**
A: Factuality: add the missing context — docs, types, the file. Faithfulness: remove context by clearing or compacting, then reload only what matters.

**Q: Why does adding more docs sometimes make it worse?**
A: If the problem is faithfulness, more docs add noise and dilute attention. Check whether the correct information was already in context before adding anything.

**Q: What is the difference between parametric and contextual knowledge?**
A: **Parametric** knowledge is recalled from the frozen parameters; **contextual** knowledge is read from the current window. Contextual usually wins, but stale parametric patterns can still leak through.

**Q: What is sycophancy?**
A: Confidently agreeable output that follows your tone instead of the evidence. Test it by asking neutrally, or by asking "are you sure?" and seeing whether the analysis changes or only the confidence does.

### Effort

**Q: What is effort?**
A: A per-request dial for how much reasoning the model does before answering. The thinking is generated as output tokens, so higher effort costs more and runs slower.

**Q: What are the usual levels?**
A: Low for mechanical edits and lookups, medium for everyday coding, high for tricky bugs and design decisions, and max for the hardest problems where a wrong answer is expensive.

**Q: What happens when effort is too low?**
A: You get a confident, shallow answer that skipped the reasoning the problem needed. It reads fine and is wrong in a way that costs you later.

**Q: What happens when effort is too high?**
A: You wait and pay for deliberation that a simple task did not need. Match effort to the task, not to the whole session.

### Choosing a Model

**Q: How do model tiers differ?**
A: A large model is smartest but slow and expensive; smaller models are faster and cheaper but less capable. Providers usually offer a ladder of tiers.

**Q: Which tier should you use for planning?**
A: The strongest one you have. Planning and architecture decisions are where a shallow answer is most expensive to unwind.

**Q: Which tier should you use for implementation?**
A: A mid-tier model is usually enough when the plan and context are clear. Use a cheaper model for mechanical edits and save the frontier model for ambiguity.

**Q: Why is the model often not the variable?**
A: Most disappointing output traces back to context or harness setup. The same model with the right files, tools, and constraints often performs completely differently.

**Q: Can you switch models mid-session?**
A: Yes, in most harnesses. The conversation continues, so you can plan with a heavy model and implement with a lighter one without losing context.

### Subagents

**Q: What is a subagent?**
A: An agent spawned by another agent via a tool call. It runs in its own session and context window, then reports a single tool result back to the parent.

**Q: How is a subagent different from a handoff?**
A: A subagent has a return path: the parent expects a report. A **handoff** has no return path; it transfers work to a fresh session that continues independently.

**Q: Why use a subagent?**
A: To keep noisy work out of the parent's context. A broad search or long exploration fills the subagent's disposable window, and only the final report lands in the parent.

**Q: Can subagents spawn more subagents?**
A: No, the tree is one level deep. Subagents isolate context; they do not compose a hierarchy.

**Q: Can subagents run in parallel?**
A: Yes. A parent can fan several out over independent pieces of work, which is useful for exploration and for independent tickets.

**Q: What is the risk of a subagent report?**
A: It is a **secondary source**. The parent sees the subagent's account, not the raw results, so anything the report omitted is invisible and may need verification against the primary source.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Model | Frozen parameters that perform next-token prediction |
| Harness | Tools, system prompt, context, and permissions around a model |
| Agent | A model plus a harness, addressed as one actor |
| Environment | The workspace the agent perceives and changes |
| Turn | One user message plus the agent's work before yielding |
| Model provider request | One request-response round-trip to the provider |
| Session | A bounded run that fills the context window |
| Context window | The token sequence the model sees per request |
| Attention budget | Per-token influence spread across the context |
| Smart zone | Early session state where the agent reasons sharply |
| Dumb zone | Later state where context degradation causes slips |
| Parametric knowledge | Facts stored in the model's frozen parameters |
| Contextual knowledge | Facts currently loaded in the window |
| Hallucination | Confidently wrong output; factuality or faithfulness |
| Effort | Reasoning dial that trades cost and latency for depth |
| Subagent | A child agent with its own context and a report back |

---

*Study aid; for authoritative content, refer to the official AI Hero course.*
