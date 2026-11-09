# Generative AI for Everyone — Questions & Answers

Study notes based on Andrew Ng's *Generative AI for Everyone* course (DeepLearning.AI).
Organized by the course's three main topics: **Introduction**, **Projects**, and **Business & Society**.

---

## Week 1 — Introduction to Generative AI

### What is Generative AI?

**Q: What is generative AI?**
A: Generative AI refers to AI systems that can produce new content — text, images, audio, video, or code — in response to instructions. Unlike traditional supervised learning, which outputs a label or number (e.g., "spam" or "not spam", or a price), generative AI outputs rich, open-ended content.

**Q: How does generative AI relate to other types of AI?**
A: Generative AI is a subset of AI, which itself is a subset of machine learning (ML). Not all AI is generative — supervised learning, for example, predicts labels or numbers. Generative AI is the branch focused on creating content.

**Q: What is a large language model (LLM)?**
A: An LLM is a model trained on huge amounts of text to predict the next word (or token). Repeating this prediction over and over lets it generate essays, answers, summaries, translations, and more. Examples include GPT-4, Claude, Gemini, and Llama.

**Q: How does an LLM actually generate text?**
A: It is given a prompt (input text) and repeatedly predicts the most likely next token based on patterns learned during training. This next-token prediction, repeated many times, produces a full response.

**Q: What does "trained on the internet" mean, and what are its implications?**
A: LLMs learn from a very large body of publicly available text and other data. Implications:
- They capture broad knowledge and language patterns.
- They can also absorb biases, outdated information, and errors from the data.
- Their knowledge is limited to what was in the training data (plus any later additions).

**Q: What is a "token"?**
A: A token is a chunk of text — often a word or part of a word — that the model processes. Models have a maximum context (token limit) for input and output.

**Q: What is the "knowledge cutoff"?**
A: The date after which information was not included in a model's training data. A model may not know about events after its cutoff unless it is given that information in the prompt or can search the web.

### How Generative AI Works (conceptually)

**Q: What are the key building blocks behind an LLM?**
A: Large-scale training data, a neural network architecture (the Transformer is the basis of most modern LLMs), massive compute, and an objective such as next-token prediction. After pretraining, models are often fine-tuned and aligned using human feedback.

**Q: What is "self-supervised learning" in this context?**
A: The model learns from the data itself by predicting hidden parts (e.g., the next word) — no human labels are required. This is why it can train on enormous unlabeled text.

**Q: What is fine-tuning?**
A: Further training a pretrained model on a smaller, targeted dataset so it behaves better for a specific task or style (e.g., being a helpful assistant, or following a company's format).

**Q: What is RLHF (Reinforcement Learning from Human Feedback)?**
A: A technique where humans rank model outputs, and the model is trained to produce outputs humans prefer — making it more helpful, harmless, and honest.

**Q: What is a "hallucination"?**
A: When a model confidently states something false or made up. Because the model generates plausible text, it can produce incorrect facts, fake citations, or invented details.

**Q: What are the main limitations of LLMs?**
A: Hallucinations, knowledge cutoffs, limited context length, inconsistent reasoning, bias, inability to verify truth reliably, and sensitivity to how a prompt is phrased.

**Q: Why can the same model give different answers to the same prompt?**
A: Generation is partly random (sampling). Settings like *temperature* control randomness — higher temperature means more varied, creative output; lower means more deterministic.

### Generative AI Applications

**Q: What are common uses of generative AI for writing?**
A: Drafting emails, reports, and essays; summarizing long documents; translating; editing and proofreading; brainstorming; and rewriting in a different tone.

**Q: What are common uses for reading/analysis?**
A: Summarizing reports, extracting key points, classifying text (e.g., sentiment, spam), answering questions about a document, and comparing documents.

**Q: What are common uses for chatting / assistants?**
A: Customer support bots, Q&A over a knowledge base, tutoring, coding assistants, and general productivity assistants.

**Q: How is generative AI used with images?**
A: Text-to-image generation, image editing, upscaling, generating product or design mockups, and creating illustrations.

**Q: What is a "chatbot" and what is "retrieval-augmented generation" (RAG)?**
A: A chatbot is an interface to an LLM. RAG augments the model by retrieving relevant documents (e.g., from a company knowledge base) and putting them in the prompt, so the model answers with up-to-date, source-grounded information instead of relying only on training data.

**Q: What is "prompt engineering"?**
A: The practice of writing clear, specific instructions to get better results from a generative model. It includes giving context, specifying the desired format, providing examples, and iterating.

**Q: What makes a good prompt?**
A: Be specific and clear about the task, provide relevant context, state the desired output format, give examples when helpful (few-shot prompting), and specify constraints (length, tone, audience).

**Q: What is "few-shot prompting"?**
A: Including a few examples of the desired input/output behavior in the prompt so the model imitates the pattern.

**Q: What is "chain-of-thought" prompting?**
A: Asking the model to reason step by step before answering, which can improve results on complex tasks.

**Q: Why is it important to review generative AI outputs?**
A: Outputs can be wrong, biased, or inappropriate. A human should verify facts, check tone, and confirm the output meets requirements before using or sending it.

**Q: What is a good workflow for using generative AI at work?**
A: (1) Decide the task and success criteria, (2) write a clear prompt with context and format, (3) generate a draft, (4) review and edit, (5) iterate on the prompt, and (6) own the final result.

---

## Week 2 — Generative AI Projects

### Building Software with Generative AI

**Q: How can developers use LLMs in software?**
A: Through APIs that send a prompt and return generated output. The application controls the prompt, processes the response, and integrates it into a product or workflow.

**Q: What are the main ways to build with LLMs?**
A: (1) Prompt engineering on a hosted model, (2) retrieval-augmented generation (RAG) to ground answers in your data, (3) fine-tuning a model on your data, and (4) training or using specialized models.

**Q: What is an API in this context?**
A: An interface that lets your code call a model over the network — you send input (the prompt and parameters) and receive output (generated text or data), without hosting the model yourself.

**Q: What is a "system prompt"?**
A: Instructions set by the application that define the assistant's role, rules, and behavior, separate from the user's message.

**Q: What are key cost and latency considerations when building with LLMs?**
A: Token usage (cost grows with input + output length), model choice (larger models cost more and are slower), context size, caching, and the number of calls per user action.

**Q: What is an "evaluation" (eval) and why is it important?**
A: A systematic way to measure output quality — e.g., a test set of prompts with expected criteria, graded by humans or by a model. Evals are essential because outputs are open-ended and can change when you tweak prompts or models.

**Q: What are ways to make LLM output more reliable in production?**
A: Clear prompts and system instructions, RAG with trusted sources, output validation/parsing, guardrails, human review for high-stakes cases, and continuous evals.

### Advanced Technologies: Beyond Prompting

**Q: What does "beyond prompting" mean?**
A: Moving from simple one-shot prompts to more capable systems — RAG, fine-tuning, tool use, agents, and specialized models.

**Q: What is retrieval-augmented generation (RAG), in more detail?**
A: Steps: (1) store documents in a searchable index (often with embeddings), (2) retrieve the most relevant chunks for a query, (3) insert them into the prompt, (4) let the model answer using that context. It reduces hallucinations and enables answers about private or recent data.

**Q: What is an embedding?**
A: A numeric vector representing the meaning of text (or images). Similar meanings have similar vectors, which enables semantic search and clustering.

**Q: What is fine-tuning used for?**
A: Adapting a model to a specific style, format, domain, or behavior — especially when prompting and RAG are not enough. It requires a curated dataset.

**Q: When should you choose RAG vs. fine-tuning?**
A: Use RAG when the model needs access to specific or changing knowledge. Use fine-tuning when you need to change behavior, style, or format consistently. They are often combined.

**Q: What is "tool use" / function calling?**
A: Letting the model call external tools or functions — calculators, databases, search, APIs — so it can take actions and access accurate information beyond its training data.

**Q: What is an AI agent?**
A: A system where an LLM plans and takes multiple steps, using tools and observations to accomplish a goal, often with some autonomy and iteration.

**Q: What are the risks of agents?**
A: Errors compounding across steps, unintended actions, security concerns, cost, and the need for oversight, permissions, and limits.

**Q: What are "guardrails"?**
A: Constraints and checks that keep a system safe and on-task — input/output filtering, allowed-tool lists, content policies, and human approval for sensitive actions.

**Q: Why is data privacy a key consideration for projects?**
A: Inputs may contain sensitive information. Teams should understand the provider's data handling, avoid sending confidential data to untrusted tools, and follow company and legal policies.

---

## Week 3 — Generative AI in Business and Society

### Generative AI and Business

**Q: How can businesses find good generative AI use cases?**
A: Look for tasks that are (1) valuable, (2) feasible with current technology, (3) low-risk to start, and (4) measurable. Start with high-value, low-risk internal productivity tasks, then expand.

**Q: What is a good way to prioritize AI projects?**
A: Score ideas by business value and technical feasibility; pick concrete, well-scoped pilots with clear success metrics, then scale what works.

**Q: What are examples of business applications?**
A: Customer support automation, marketing content, sales assistance, software development, document processing, internal knowledge search, and data analysis.

**Q: What role does generative AI play in productivity?**
A: It automates and accelerates drafting, summarizing, coding, and analysis, freeing people for judgment, creativity, and relationship-building — often described as an "assistant" or "copilot."

**Q: What is an "AI strategy" for a company?**
A: A plan for where and how to apply AI to create value: choosing use cases, building skills and infrastructure, setting governance, measuring impact, and scaling responsibly.

**Q: What organizational factors matter for success?**
A: Executive sponsorship, clear goals and metrics, cross-functional teams, data quality and access, training, change management, and a culture of experimentation.

**Q: What is the "build vs. buy" decision?**
A: Whether to build custom solutions (control, differentiation, higher cost/effort) or buy/use existing tools and APIs (faster, cheaper, less control). Many teams start by buying and customize where it matters.

**Q: What are common pitfalls in business AI projects?**
A: Choosing vague or low-value use cases, ignoring data quality, underestimating change management, skipping evaluation, and overpromising without safety and review processes.

**Q: What is the concept of "AI as a general-purpose technology"?**
A: Like electricity or the internet, generative AI can improve many different tasks and industries — its impact comes from broad adoption and integration into workflows, not one single application.

**Q: How should companies think about ROI?**
A: Measure concrete outcomes — time saved, cost reduced, quality improved, revenue gained — in pilots before scaling. Balance quick wins with longer-term transformation.

### Generative AI and Society

**Q: What are the main societal benefits of generative AI?**
A: Increased productivity, better access to information and assistance, faster scientific and medical progress, improved education and tutoring, and new creative tools.

**Q: What are the main societal risks?**
A: Misinformation and deepfakes, bias and fairness issues, job displacement and disruption, privacy and surveillance concerns, concentration of power, security risks, and environmental costs of compute.

**Q: What is a "deepfake"?**
A: Synthetic media (image, audio, video) generated to convincingly depict people or events that did not happen. It can spread misinformation and harm reputations.

**Q: What are bias and fairness concerns with generative AI?**
A: Models learn from data that may contain stereotypes and inequality, so outputs can be biased. Mitigation requires careful data, evaluation, and human oversight.

**Q: How might generative AI affect jobs?**
A: It automates parts of many jobs, changing tasks rather than simply replacing whole roles. It raises demand for skills like judgment, oversight, domain expertise, and working with AI — and creates new roles.

**Q: What is the "automation vs. augmentation" framing?**
A: Automation replaces a task; augmentation helps a person do it better or faster. Much of generative AI's impact is augmentation, though some tasks can be automated.

**Q: How can society and organizations manage risks responsibly?**
A: Awareness and education, human review for high-stakes decisions, transparency about AI use, content provenance and labeling, security practices, regulation and policy, and ongoing evaluation.

**Q: What is "responsible AI"?**
A: Designing and deploying AI systems that are safe, fair, transparent, accountable, privacy-respecting, and aligned with human values throughout their lifecycle.

**Q: What should individuals do to prepare for an AI-powered future?**
A: Learn how the tools work and their limits, practice using them on real tasks, develop judgment and verification skills, and stay current as the technology evolves.

**Q: How can leaders set a healthy culture around AI?**
A: Encourage experimentation within guardrails, train staff, share best practices, set clear policies for data and output use, and celebrate measurable wins while watching for risks.

---

## Quick Reference — Key Terms

| Term | Meaning |
| --- | --- |
| Generative AI | AI that creates new content (text, images, audio, code) |
| LLM | Large language model trained to predict the next token |
| Prompt | The instruction/input given to a model |
| Prompt engineering | Crafting prompts for better results |
| Token | A chunk of text a model processes |
| Hallucination | Confidently stated but false output |
| Knowledge cutoff | Date after which a model has no training data |
| Embedding | Vector representation of meaning |
| RAG | Retrieval-augmented generation — grounding answers in retrieved documents |
| Fine-tuning | Further training a model on a targeted dataset |
| RLHF | Learning from human preferences to align behavior |
| Agent | An LLM that plans and acts, often using tools |
| Guardrails | Constraints and checks that keep systems safe |
| Deepfake | Synthetic media that falsely depicts people or events |
| Responsible AI | Building AI that is safe, fair, and accountable |

---

*These notes are a study aid and paraphrase the themes of the course; for authoritative content, refer to the official DeepLearning.AI course.*
