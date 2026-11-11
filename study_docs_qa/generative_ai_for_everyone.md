# Generative AI for Everyone — Q&A

Fast-reference notes for Andrew Ng's *Generative AI for Everyone* (DeepLearning.AI).
**Introduction → Projects → Business & Society.**

---

## Week 1 — Introduction to Generative AI

### What is Generative AI?

**Q: What is generative AI?**
A: AI that produces new content — text, images, audio, video, or code — from instructions. Unlike supervised learning, which outputs a label or number, it outputs rich, open-ended content.

**Q: How does it relate to other AI?**
A: Generative AI ⊂ AI ⊂ machine learning. Not all AI is generative: supervised learning predicts labels/numbers; generative AI creates content.

**Q: What is a large language model (LLM)?**
A: A model trained on huge amounts of text to predict the next word/token. Repeated prediction generates essays, answers, summaries, translations, and more. Examples: GPT-4, Claude, Gemini, Llama.

**Q: How does an LLM generate text?**
A: Given a prompt, it repeatedly predicts the most likely next token from patterns learned in training; repeating this produces a full response.

**Q: What does "trained on the internet" imply?**
A: LLMs learn from a very large body of public text and other data. They capture broad knowledge and language patterns but can absorb biases, outdated information, and errors, and know only what was in training data (plus later additions).

**Q: What is a token?**
A: A chunk of text — often a word or part of a word — processed by the model. Models have a maximum context (token limit) for input and output.

**Q: What is the knowledge cutoff?**
A: The date after which information was not in a model's training data. Models may not know later events unless given them in the prompt or able to search the web.

### How It Works

**Q: What are the key building blocks?**
A: Large-scale training data, a neural network architecture (the Transformer underlies most modern LLMs), massive compute, and an objective such as next-token prediction. After pretraining, models are fine-tuned and aligned with human feedback.

**Q: What is self-supervised learning here?**
A: Learning from the data itself by predicting hidden parts (e.g., the next word) — no human labels required, so training can use enormous unlabeled text.

**Q: What is fine-tuning?**
A: Further training a pretrained model on a smaller, targeted dataset to improve a task or style (e.g., being a helpful assistant or following a company format).

**Q: What is RLHF?**
A: Reinforcement Learning from Human Feedback: humans rank outputs, and the model is trained to produce preferred outputs — making it more helpful, harmless, and honest.

**Q: What is a hallucination?**
A: When a model confidently states something false or made up. Because it generates plausible text, it can produce incorrect facts, fake citations, or invented details.

**Q: What are LLM limitations?**
A: Hallucinations, knowledge cutoffs, limited context, inconsistent reasoning, bias, inability to verify truth reliably, and sensitivity to prompt phrasing.

**Q: Why can the same prompt give different answers?**
A: Generation is partly random (sampling). **Temperature** controls randomness: higher = more varied/creative; lower = more deterministic.

### Applications

**Q: Common writing uses?**
A: Drafting emails, reports, and essays; summarizing long documents; translating; editing/proofreading; brainstorming; rewriting in a different tone.

**Q: Common reading/analysis uses?**
A: Summarizing reports, extracting key points, classifying text (sentiment, spam), answering questions about a document, and comparing documents.

**Q: Common chat/assistant uses?**
A: Customer support bots, Q&A over a knowledge base, tutoring, coding assistants, and general productivity assistants.

**Q: Common image uses?**
A: Text-to-image generation, editing, upscaling, product/design mockups, and illustrations.

**Q: Chatbot vs. RAG?**
A: A chatbot is an interface to an LLM. **Retrieval-augmented generation (RAG)** retrieves relevant documents (e.g., from a company knowledge base) and puts them in the prompt so answers are current and source-grounded.

**Q: What is prompt engineering?**
A: Writing clear, specific instructions to get better results: give context, specify format, provide examples, and iterate.

**Q: What makes a good prompt?**
A: Be specific about the task, provide relevant context, state the desired output format, give examples when helpful, and specify constraints (length, tone, audience).

**Q: What is few-shot prompting?**
A: Including a few examples of the desired input/output behavior so the model imitates the pattern.

**Q: What is chain-of-thought prompting?**
A: Asking the model to reason step by step before answering, which can improve complex tasks.

**Q: Why review outputs?**
A: Outputs can be wrong, biased, or inappropriate. A human should verify facts, check tone, and confirm requirements.

**Q: Good workflow at work?**
A: (1) Define task and success criteria, (2) write a clear prompt with context and format, (3) generate a draft, (4) review and edit, (5) iterate on the prompt, (6) own the final result.

---

## Week 2 — Generative AI Projects

### Building Software

**Q: How can developers use LLMs?**
A: Through APIs that send a prompt and return generated output. The application controls the prompt, processes the response, and integrates it.

**Q: Main ways to build with LLMs?**
A: (1) Prompt engineering on a hosted model, (2) RAG to ground answers in your data, (3) fine-tuning on your data, (4) training/using specialized models.

**Q: What is an API here?**
A: An interface that lets code call a model over the network — send input (prompt + parameters), receive output (text or data) — without hosting the model.

**Q: What is a system prompt?**
A: Instructions set by the application defining the assistant's role, rules, and behavior, separate from the user's message.

**Q: Key cost and latency considerations?**
A: Token usage (cost grows with input + output length), model choice (larger = costlier/slower), context size, caching, and calls per user action.

**Q: What is an evaluation (eval)?**
A: A systematic way to measure output quality — e.g., a test set of prompts with expected criteria, graded by humans or a model. Essential because outputs are open-ended and change when prompts/models change.

**Q: How to make outputs reliable in production?**
A: Clear prompts and system instructions, RAG with trusted sources, output validation/parsing, guardrails, human review for high-stakes cases, and continuous evals.

### Beyond Prompting

**Q: What does "beyond prompting" mean?**
A: Moving from simple prompts to more capable systems — RAG, fine-tuning, tool use, agents, and specialized models.

**Q: RAG in detail?**
A: (1) Store documents in a searchable index (often with embeddings), (2) retrieve relevant chunks for a query, (3) insert them into the prompt, (4) answer using that context. Reduces hallucinations and enables answers about private or recent data.

**Q: What is an embedding?**
A: A numeric vector representing the meaning of text (or images). Similar meanings have similar vectors, enabling semantic search and clustering.

**Q: What is fine-tuning used for?**
A: Adapting a model to a specific style, format, domain, or behavior — especially when prompting and RAG are not enough. Requires a curated dataset.

**Q: RAG vs. fine-tuning?**
A: RAG for specific or changing knowledge; fine-tuning to change behavior, style, or format consistently. They are often combined.

**Q: What is tool use / function calling?**
A: Letting the model call external tools — calculators, databases, search, APIs — to take actions and access accurate information beyond training data.

**Q: What is an AI agent?**
A: A system where an LLM plans and takes multiple steps, using tools and observations to reach a goal, often with autonomy and iteration.

**Q: Agent risks?**
A: Errors compounding across steps, unintended actions, security concerns, cost, and the need for oversight, permissions, and limits.

**Q: What are guardrails?**
A: Constraints and checks keeping a system safe and on-task — input/output filtering, allowed-tool lists, content policies, and human approval for sensitive actions.

**Q: Why is data privacy key?**
A: Inputs may contain sensitive data. Teams should understand the provider's data handling, avoid sending confidential data to untrusted tools, and follow company and legal policy.

---

## Week 3 — Business and Society

### Business

**Q: How to find good use cases?**
A: Look for tasks that are (1) valuable, (2) feasible with current technology, (3) low-risk to start, and (4) measurable. Start with high-value, low-risk internal productivity, then expand.

**Q: How to prioritize projects?**
A: Score by business value and technical feasibility; pick concrete, well-scoped pilots with clear success metrics, then scale what works.

**Q: Business application examples?**
A: Customer support automation, marketing content, sales assistance, software development, document processing, internal knowledge search, and data analysis.

**Q: Role in productivity?**
A: Automates and accelerates drafting, summarizing, coding, and analysis, freeing people for judgment, creativity, and relationships — an "assistant" or "copilot."

**Q: What is a company AI strategy?**
A: A plan for where and how AI creates value: choosing use cases, building skills and infrastructure, setting governance, measuring impact, and scaling responsibly.

**Q: What organizational factors matter?**
A: Executive sponsorship, clear goals and metrics, cross-functional teams, data quality and access, training, change management, and a culture of experimentation.

**Q: Build vs. buy?**
A: Build for control, differentiation, and higher cost/effort; buy/use existing tools and APIs for speed, lower cost, and less control. Many teams buy first and customize where it matters.

**Q: Common pitfalls?**
A: Vague or low-value use cases, ignoring data quality, underestimating change management, skipping evaluation, and overpromising without safety/review processes.

**Q: AI as a general-purpose technology?**
A: Like electricity or the internet, it can improve many tasks and industries. Impact comes from broad adoption and workflow integration, not one application.

**Q: How should companies think about ROI?**
A: Measure concrete outcomes — time saved, cost reduced, quality improved, revenue gained — in pilots before scaling. Balance quick wins with long-term transformation.

### Society

**Q: Main societal benefits?**
A: Productivity, better access to information and assistance, faster scientific/medical progress, improved education and tutoring, and new creative tools.

**Q: Main societal risks?**
A: Misinformation and deepfakes, bias and fairness issues, job displacement, privacy and surveillance, concentration of power, security risks, and environmental compute costs.

**Q: What is a deepfake?**
A: Synthetic media (image, audio, video) convincingly depicting people or events that did not happen; can spread misinformation and harm reputations.

**Q: Bias and fairness concerns?**
A: Models learn from data containing stereotypes and inequality, so outputs can be biased. Mitigation needs careful data, evaluation, and human oversight.

**Q: How might AI affect jobs?**
A: It automates parts of many jobs, changing tasks rather than simply replacing whole roles; demand grows for judgment, oversight, domain expertise, and working with AI, and new roles appear.

**Q: Automation vs. augmentation?**
A: Automation replaces a task; augmentation helps a person do it better or faster. Much generative AI impact is augmentation, though some tasks are automated.

**Q: How to manage risks responsibly?**
A: Awareness and education, human review for high-stakes decisions, transparency about AI use, content provenance/labeling, security practices, regulation and policy, and ongoing evaluation.

**Q: What is responsible AI?**
A: Designing and deploying AI that is safe, fair, transparent, accountable, privacy-respecting, and aligned with human values throughout its lifecycle.

**Q: How should individuals prepare?**
A: Learn how the tools work and their limits, practice on real tasks, develop judgment and verification skills, and stay current as the technology evolves.

**Q: How can leaders build a healthy culture?**
A: Encourage experimentation within guardrails, train staff, share best practices, set clear policies for data and output use, and celebrate measurable wins while watching for risks.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Generative AI | AI that creates new content (text, images, audio, code) |
| LLM | Large language model trained to predict the next token |
| Prompt | Instruction/input given to a model |
| Prompt engineering | Crafting prompts for better results |
| Token | A chunk of text a model processes |
| Hallucination | Confidently stated but false output |
| Knowledge cutoff | Date after which a model has no training data |
| Embedding | Vector representation of meaning |
| RAG | Grounding answers in retrieved documents |
| Fine-tuning | Further training on a targeted dataset |
| RLHF | Learning from human preferences to align behavior |
| Agent | LLM that plans and acts, often using tools |
| Guardrails | Constraints and checks that keep systems safe |
| Deepfake | Synthetic media falsely depicting people or events |
| Responsible AI | Safe, fair, accountable AI |

---

*Study aid; for authoritative content, refer to the official DeepLearning.AI course.*
