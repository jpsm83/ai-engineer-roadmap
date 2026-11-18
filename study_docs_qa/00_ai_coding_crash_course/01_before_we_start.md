### Intro

**Q: Why not always use the biggest model at maximum effort?**
A: Cost and latency scale with both. A one-line rename does not need maximum reasoning, and using it there wastes time without improving the result.

**Q: When should you switch models mid-session?**
A: Switch when the task changes character: a heavy model for the plan, a lighter one for repetitive edits, then back for review. The harness keeps the conversation, so the switch is cheap.

**Q: Why does the harness matter more than the model name?**
A: The same model in Claude Code, Cursor, or Claude.ai behaves differently because the **system prompt**, tools, permissions, and context handling differ. Most "model" surprises are harness differences.

**Q: What should you never share?**
A: API keys, tokens, passwords, customer data, or private repository contents. Redact secrets before posting logs or screenshots.
