# AI Coding Crash Course — Getting to Know Claude Code — Q&A

Fast-reference notes for Matt Pocock's *AI Coding Crash Course* (AI Hero).
**Intro → Managing Your Claude Code Session → Prompting in the Terminal → Claude and Your IDE → Going Forwards and Backwards in Time → Running Bash Commands → Permissions.**

---

## Part 3 — Getting to Know Claude Code

### Intro

**Q: What is Claude Code?**
A: A terminal **harness** around a Claude model. It adds filesystem tools, a Bash tool, search, permissions, context management, and checkpoints, which together make it a coding agent.

**Q: Where does Claude Code run?**
A: In your terminal, from the project root. It can also integrate with an IDE, but the core loop is the same: you type a request, the agent calls tools, and the result returns to the conversation.

**Q: What should you do before your first session?**
A: Open the project root, check `git status`, and run `claude`. A clean working tree makes it easy to see what the agent changed and to undo anything you do not want.

**Q: What is the mental model for the session?**
A: It is a conversation that accumulates tool results. Everything the agent reads or runs stays in the context until you clear or compact, so the session is a budget, not a free unlimited workspace.

### Managing Your Claude Code Session

**Q: How do you start a session?**
A: Run `claude` in the project directory and type your first request. The harness loads the system prompt, project instructions, and tool definitions before it sees your message.

**Q: How do you keep a session focused?**
A: Do one task per session. Unrelated work leaves residue that colours later answers, and starting a second task in the same session spends the smart zone on the first task's leftovers.

**Q: When should you clear?**
A: When a task is finished, when the agent is looping on a polluted context, or when you are switching to unrelated work. `/clear` ends the session and starts empty.

**Q: When should you compact?**
A: At a phase boundary within the same task, when you need to preserve intent but free context. `/compact` summarises the session and seeds a fresh one.

**Q: How do you resume a past session?**
A: Use `/resume` to pick a previous session from the list. Resuming brings back the stored history, but it also brings back the noise, so resume deliberately.

**Q: How do you inspect the session state?**
A: Use `/status` for model, context usage, and session details, and `/context` where available to see what is occupying the window. Read the numbers instead of guessing.

**Q: How do you stop a turn that is going wrong?**
A: Press Esc to interrupt, then redirect with a correction. Most harnesses also let you type while the agent works; the message is read when the current turn completes.

**Q: What is the difference between clearing and starting a new terminal?**
A: `/clear` resets the conversation but keeps the project and harness state. A new terminal starts a new process; both give you a fresh context, but clearing is faster and keeps your setup.

### Prompting in the Terminal

**Q: What makes a good terminal prompt?**
A: State the goal, the relevant files or directories, the constraints, and the acceptance criteria. A specific request with a concrete check beats a broad instruction like "improve the app".

**Q: Why give file paths in the prompt?**
A: They act as **context pointers**: the agent knows where to look and spends fewer tool calls searching. Use paths to the real code rather than descriptions of where you think the code is.

**Q: Should you ask for a plan first?**
A: For non-trivial work, yes. A short plan exposes assumptions before edits, and it gives you a place to correct the approach cheaply.

**Q: How large should a request be?**
A: Small enough to review and verify in one sitting. If the task spans several concerns, split it into steps or tickets instead of asking for everything at once.

**Q: What should you do when the agent asks a clarifying question?**
A: Answer it directly and add the missing constraint. A clarifying question is cheaper than a wrong implementation, so do not punish it by saying "just do it".

**Q: How do you correct the agent effectively?**
A: Point at the specific behaviour and the evidence: "this test fails because the handler returns `undefined`; preserve the existing error shape". Vague displeasure gives the model nothing to act on.

**Q: Why does the agent sometimes ignore a constraint you gave earlier?**
A: **Attention degradation**. The constraint is still in context but has less influence as the window fills; restate it near the work, or clear and reload with a smaller, focused context.

### Claude and Your IDE

**Q: How does Claude Code integrate with an IDE?**
A: It can run in the IDE's integrated terminal or through an extension, so the agent shares the project and you can see diffs in the editor. The harness is still Claude Code; the IDE adds visibility.

**Q: What does the IDE integration help with?**
A: Reviewing changes in a diff view, seeing the current file or selection, and jumping to the code the agent references. It reduces the friction of inspecting the **primary source**.

**Q: Does the IDE change the model's abilities?**
A: Not fundamentally. It changes the interface and the context you can share, but the tools, permissions, and context management still come from the harness.

**Q: Why review the diff in the IDE rather than the agent's summary?**
A: The summary is a **secondary source** written by the party being reviewed. The diff is the **primary source**, and it is where unintended changes and missing edge cases show up.

**Q: How do you use the IDE to steer?**
A: Open the relevant file, select the function, and reference it in the prompt. That gives the agent a precise target and reduces the chance it edits a similarly named file.

### Going Forwards and Backwards in Time

**Q: What is a checkpoint in Claude Code?**
A: A restore point the harness creates as it works, capturing conversation and file state. It lets you rewind after a bad turn without manually undoing every change.

**Q: How do you rewind?**
A: Use `/rewind` or the keyboard shortcut shown by your version, then choose the point to return to. The exact UI varies, so check `/help` if the shortcut is unfamiliar.

**Q: Does rewinding also revert Git commits?**
A: No. Checkpoints are a harness feature, not a replacement for Git. Use `git diff`, `git status`, and commits for durable version control.

**Q: When is rewinding better than fixing forward?**
A: When the agent has taken a wrong turn that polluted the context or produced a large, confused diff. Rewinding to before the mistake is often cheaper than untangling it.

**Q: What is the risk of rewinding?**
A: You can lose work you wanted to keep. Commit or stash first if the session contains changes you have not reviewed, and treat checkpoints as a convenience, not a backup.

**Q: How do you go forward again after rewinding?**
A: Re-send the request with the lesson learned, or resume from a later checkpoint if the harness kept it. Rewinding is a branch in your work, not a time machine for the provider's state.

### Running Bash Commands

**Q: How does Claude Code run shell commands?**
A: Through the **Bash tool**. The model emits a tool call with a command, the harness checks permissions, executes it, and returns the output as a tool result.

**Q: What kinds of commands should the agent run?**
A: Tests, type checks, lints, builds, `git diff`, and project scripts. These are **automated checks**: deterministic signals the agent can self-correct from.

**Q: Why is running tests so important?**
A: The failure output lands in context with a file, line, and assertion, which is exactly what the agent needs to fix the problem. A passing test is evidence; a claim that tests pass is not.

**Q: What should you do before approving a destructive command?**
A: Read it. Watch for `rm`, force pushes, database resets, and commands that touch files outside the project. Approve only when the blast radius is clear.

**Q: How do you make common safe commands less interruptive?**
A: Add them to the project or user permission allowlist, for example read-only `git` commands and the test script. Pre-approve the safe, frequent calls and keep prompts for the risky ones.

**Q: Why does the agent sometimes say it ran a command when it did not?**
A: The model can describe an action without emitting a tool call, or the harness can deny the call. Check the transcript for the tool call and its result, not just the prose.

**Q: How do you inspect a long command's output?**
A: Ask for the relevant lines, or have the agent write the output to a file and search it. Dumping a huge log into context is expensive and dilutes attention.

### Permissions

**Q: What is a permission request?**
A: A pause before a tool call that is not pre-approved. The harness shows the call, and you approve once, approve for the session, or deny it.

**Q: What happens when you deny a request?**
A: The denial is returned to the model as a tool result. The agent can try a different approach, and you can attach a message to steer it toward the right one.

**Q: What are the main permission modes?**
A: Read-only or plan mode, the default that asks on writes and shell, accept-edits that auto-approves edits, and bypass or "YOLO" mode that auto-approves everything.

**Q: How do you choose a permission mode?**
A: Match it to your trust and the blast radius. Use plan mode while shaping the approach, default for delicate edits, accept-edits once the agent understands the change, and bypass only inside a sandbox.

**Q: What is the danger of approving on autopilot?**
A: Rubber-stamping gives you all the interruption with none of the protection. If you are not reading the prompts, tighten the allowlist or use a sandbox instead of pretending to review.

**Q: Why is a sandbox safer than unlimited approvals?**
A: A **sandbox** limits what a bad call can reach, so you can widen permissions without betting the whole machine. Permissions ask before the action; a sandbox contains it if it runs.

**Q: How do you persist permission settings?**
A: Put allow and deny rules in the project or user settings file, such as `.claude/settings.json`. Commit project rules so the team shares the same safe defaults.

**Q: What should always be denied or prompted?**
A: Destructive filesystem commands, force pushes, production database access, secret exfiltration, and anything that leaves the sandbox. When in doubt, prompt.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Claude Code | Terminal harness that turns Claude into a coding agent |
| `/clear` | End the session and start with an empty context |
| `/compact` | Summarise the session and continue in a fresh window |
| `/resume` | Reopen a previous session |
| `/rewind` | Return to an earlier checkpoint |
| `/status` | Show model, context, and session details |
| Checkpoint | Harness restore point for conversation and files |
| Bash tool | Tool that runs shell commands and returns output |
| Permission request | Approval prompt before an unapproved tool call |
| Permission mode | Preset controlling which calls ask or auto-run |
| Plan mode | Read-only mode that blocks edits and encourages research |
| Accept-edits | Mode that auto-approves file edits |
| Bypass mode | Mode that auto-approves all tool calls |
| Sandbox | Isolated environment that limits blast radius |

---

*Study aid; for authoritative content, refer to the official AI Hero course.*
