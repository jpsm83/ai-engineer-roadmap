# AI Application Engineer Roadmap for Full-Stack Developers
### Self-Study Topic Map — From Full-Stack to Building AI-Powered Products

You are **not** becoming an ML researcher or model trainer. Your target role is the one described in most "AI Engineer" job ads today: a strong full-stack engineer who builds **production AI applications** — RAG systems, MCP servers, chatbots, agents, and AI features wired front-to-back into real products.

As a Full-Stack Developer with 5+ years of experience, you already have **~85% of the required skills**. The gap is not machine learning theory. It is:

1. **Probabilistic architecture** — designing around non-deterministic models.
2. **Retrieval & context engineering** — grounding models in your data.
3. **Evaluation** — measuring AI behavior instead of asserting it.
4. **AI product engineering** — streaming UX, cost controls, security, observability.

This document maps that path, prioritized by relevance to building AI products, with progress checkboxes for self-tracking.

> **Design principle:** learn the *minimum* ML needed to make good engineering decisions, then spend the rest of your time shipping AI features end-to-end.

> **Python setup reference:** [PYTHON_REFERENCE.md](PYTHON_REFERENCE.md) explains
> `.venv/`, `__pycache__/`, and the `__init__` method for every Python exercise
> folder in this repository.

> **Dependencies:** each Python folder has its own `requirements.txt` (the
> Python equivalent of `package.json`). Install with `pip install -r
> requirements.txt` from inside that folder's activated `.venv/`.

> **Secrets:** API keys and URLs live in a single `.env` at the repository root.
> It is gitignored and never committed; create it locally with the variables
> each exercise needs.

---

## 🎯 Target Role & Scope

**You are optimizing for:** AI Application Engineer / AI Product Engineer / LLM Engineer — the "build RAGs, MCPs, chatbots, and full AI solutions front-to-back" role.

**You are NOT optimizing for:** ML Engineer / Applied Scientist / Research Engineer — the "train, fine-tune, and serve models" role.

**The one hard rule:** don't spend 100 hours training models you will never ship. Learn what a model *is* and *how it fails*; let the model vendors handle the weights.

---

## 📖 How to Work Through This Roadmap

Each phase below is a **self-contained working unit**. Read and work through a phase top to bottom, in this order:

1. **Topic checklist** — the concepts and skills to tick off.
2. **DeepLearning.AI courses & videos** — the guided learning for the phase, with its own checkboxes, durations, and links.
3. **Resource hub** — the official docs and references to fill the gaps.
4. **Milestone** — the artifact that proves the phase is done.
5. **Portfolio project** — the build you do after the milestone (where the phase has one).
6. **Coverage & notes** — deliberate skips, coverage status, and gaps courses don't fill.

> **Portfolio Projects (The Build Syllabus):** Build these in order. Each one is a production-shaped artifact, not a tutorial.

### 🎓 The DeepLearning.AI Course Thread

> A reduced, application-focused route through the DeepLearning.AI catalog. It covers the HIGH-priority phases (0–8) with the smallest sensible set of courses, and drops the ML-training specialization entirely. Built for a working full-stack developer.

**How to read the course checklists:**

- ✅ **Free** — DeepLearning.AI *Short Courses* (1–3 h each). No subscription needed. This is the majority of the route.
- 💳 **Pro** — *Courses* and *Professional Certificates* (require Pro ≈ $25–30/mo, or a Coursera plan). Subscribe **only** when you reach a 💳 anchor, and cancel when done.
- ⏱️ **Time** = the platform's stated duration. Budget **~1.5–2×** for exercises and notes.
- 📅 **Pace assumed**: 10–12 h/week. Week ranges are guidance, not deadlines.
- 🎯 Every stage ends in a **milestone output** — a project or artifact, never just "completed a course."
- 🧩 The roadmap's own **Portfolio Projects** are slotted at the end of the relevant stages.

**The only 💳 anchors on the core path:** `Retrieval Augmented Generation (RAG)` and `Agentic AI`. Everything else on the critical path is free.

---

## 🔴 PHASE 0: Orientation & ML Literacy — HIGH PRIORITY
*A small, deliberate dose of ML — concepts only. This replaces the old 95-hour ML specialization.*

### 🧠 Topic Checklist
- [x] What AI can and can't do; the AI Engineer vs. ML Engineer vs. Data Scientist distinction
- [x] Probabilistic vs. deterministic systems: why the same input can produce different output
- [x] Supervised vs. unsupervised learning in one page (what "training" means, at a high level)
- [x] Overfitting / train-val-test split — the intuition, not the math
- [x] Evaluation metrics **in the retrieval context**: precision, recall, precision@k, recall@k, MRR, nDCG
- [x] Embeddings intuition: what a vector represents, why similar meaning → nearby points
- [x] Distance metrics: cosine similarity, dot product, Euclidean (when each is used)
- [x] Sampling parameters: temperature, top-p, top-k; determinism vs. creativity
- [x] What fine-tuning is (conceptually) and **why you usually shouldn't start there** — compare prompting vs. RAG vs. fine-tuning
- [x] Token economics: tokens, context limits, input/output pricing, rough cost math

**Deliberately excluded from this phase:** backpropagation, gradient descent, XGBoost, random forests, CNNs, RNNs, reinforcement learning. You will never need these to build RAG or agent products.

### 🎓 DeepLearning.AI — Stage 0: Orientation & ML Literacy (Week 1 · ~4 h)

The mental model before any code. Do this instead of a full ML course.

- [x] 💳 `AI for Everyone` — 6h54m — what AI can/can't do, societal impact. *(already done)*
- [x] ✅ `Generative AI for Everyone` — 5h1m — GenAI capabilities, limits, business framing. *(often free to audit; skim)*
- [x] Read/watch: evaluation metrics in retrieval (precision/recall@k, MRR), embeddings intuition, sampling parameters. Use the OpenAI Cookbook + provider docs.

### 📚 Resource Hub (Phase 0)

| Resource / Platform | Topics Covered | Where to Find It |
| :--- | :--- | :--- |
| **OpenAI Cookbook** *(Official)* | Embeddings, structured outputs, token optimization, evals | [cookbook.openai.com](https://cookbook.openai.com) |
| **HuggingFace Course** *(Free)* | Transformer concepts, embeddings, model landscape | [huggingface.co/learn](https://huggingface.co/learn) |

### 🎯 Milestone
Write a one-page decision guide — "When do I prompt, when do I add RAG, when do I fine-tune, when do I train a model?" — and explain it to a non-technical colleague.

### 📌 Coverage & Notes
- **Coverage:** AI for Everyone, GenAI for Everyone, docs — ✅ Sufficient (deliberately shallow).
- **Gap:** Retrieval metrics (precision@k, MRR, nDCG) — no dedicated course in the thread; use search/IR references and build the eval. *(Shared with Phase 4.)*

---

## 🟡 PHASE 1: Python & AI Dev Fluency — MEDIUM PRIORITY (fast-track)
*Skip most of this if you already write Python. The goal is AI idioms, not the language.*

### 🧠 Topic Checklist
- [x] Python fluency check: type hints, async/await, generators, decorators, Pydantic
- [x] Environments & dependency management (uv/poetry/venv)
- [x] Project layout for AI services (config, secrets, logging, tests)

### 🎓 DeepLearning.AI — Stage 1: Python & AI Fluency (Weeks 1–2 · fast-track)

You already program. Treat this as an AI-idiom speedrun, not a from-zero course.

- [x] 💳 `Python` — FreeCodeCamp.
- [ ] *(optional)* `AI Python for Beginners` — only if you want a structured refresher.

### 📚 Resource Hub (Phase 1)

_No dedicated entry in the roadmap's original Resource Hub. The FreeCodeCamp course above plus your existing Python tooling (uv/poetry/venv) is sufficient._

### 🎯 Milestone
Rebuild one small existing script of yours as a typed, tested Python service.

### 📌 Coverage & Notes
- **Coverage:** AI Python for Beginners (optional) — ✅.

---

## 🔴 PHASE 2: LLM Literacy — HIGH PRIORITY
*Enough theory to debug behavior and budget cost — not enough to build a model.*

### 🧠 Topic Checklist
- [x] Transformer at a conceptual level: tokens in → next-token probabilities out
- [ ] Tokenization: why "characters ≠ tokens," and how it affects cost and truncation
- [ ] Context window: what fits, what gets dropped, and how to manage it
- [x] Encoder-only vs. decoder-only vs. encoder-decoder (one paragraph each)
- [ ] Model families & provider trade-offs: GPT, Claude, Gemini, Llama, Mistral
- [ ] Chat vs. completion vs. reasoning models — when each is appropriate
- [ ] Structured outputs & tool calling as first-class model features
- [ ] Hallucination: why it happens and the engineering responses (grounding, citations, evals)
- [ ] What fine-tuning is — and the decision rule from Phase 0

**Deferred (know they exist, don't study deeply):** pretraining from scratch, masked language modeling, attention math, LoRA/QLoRA internals, model distillation.

### 🎓 DeepLearning.AI — Stage 2: LLM Literacy: How Models Behave (Week 2 · ~4 h)

Concepts, not training. Prefer docs and short videos over long courses.

- [x] ✅ `Attention in Transformers: Concepts and Code in PyTorch` (StatQuest) — 1h16m — watch for intuition; you won't implement it in production.
- [ ] ✅ `Finetuning Large Language Models` (Lamini) — ~1h — understand full fine-tune vs. PEFT/LoRA **as a decision**, not a skill.
- [ ] 💳 *(optional)* `Generative AI with Large Language Models` (AWS) — 13h18m — only if you want the lifecycle narrative and Bedrock context.

**Drop from the old plan:** `Transformers in Practice` (11 h), `Build and Train an LLM with JAX`, `Deep Learning Specialization`. These serve the ML path.

### 📚 Resource Hub (Phase 2)

| Resource / Platform | Topics Covered | Where to Find It |
| :--- | :--- | :--- |
| **HuggingFace Course** *(Free)* | Transformer concepts, embeddings, model landscape | [huggingface.co/learn](https://huggingface.co/learn) |
| **Andrej Karpathy** *(YouTube)* | Deep intuition for how LLMs work (watch selectively) | [YouTube @AndrejKarpathy](https://youtube.com) |
| **OpenAI Cookbook** *(Official)* | Embeddings, structured outputs, token optimization, evals | [cookbook.openai.com](https://cookbook.openai.com) |

### 🎯 Milestone
Whiteboard "what happens between sending a prompt and receiving a token," including where cost and latency come from.

### 📌 Coverage & Notes
- **Coverage:** Attention (StatQuest), Fine-tuning (Lamini) — ✅ Conceptual.

---

## 🔴 PHASE 3: Prompting & LLM Integration — HIGH PRIORITY
*Core daily work — the interface between your code and the model.*

### 🧠 Topic Checklist

#### 3.1 Prompt Engineering
- [ ] Instruction-following principles; temperature/top-p/top-k in practice
- [ ] System instructions & role prompting
- [ ] Chain of Thought (CoT) & ReAct patterns
- [ ] Few-shot vs. zero-shot; example selection
- [ ] Prompt evaluation & iteration (treat prompts as code under test)
- [ ] Context engineering: what goes in, in what order, and why

#### 3.2 LLM Integration
- [ ] OpenAI API (Chat Completions, structured outputs, tool use)
- [ ] Anthropic Claude API (Messages API, tool use)
- [ ] One cloud abstraction layer (Bedrock, Vertex, or Azure OpenAI) — auth, cost, latency
- [ ] LiteLLM or equivalent model-agnostic abstraction (provider switching, fallbacks)
- [ ] Pure Python integration with no framework — understand what frameworks hide
- [ ] LangChain & LangGraph fundamentals
- [ ] Streaming responses (SSE / token streaming)

#### 3.3 AI-Assisted Engineering Workflows
- [ ] Code generation, debugging & refactoring with AI agents
- [ ] Large-codebase context and multi-file navigation
- [ ] Test generation & validation
- [ ] Spec-driven development with coding agents
- [x] AI Hero: AI Coding Crash Course — agent skills, steering, planning workflows (aihero.dev)

**Skip unless a job requires it:** Open WebUI, Llama.cpp, local GGUF quantization. These are self-hosting concerns, not application-building concerns. Add later only if you need on-prem inference.

### 🎓 DeepLearning.AI — Stage 3: Prompting, Integration & AI Coding (Weeks 3–4 · ~15 h)

**3.1 Prompt engineering**
- [ ] 💳 `AI Prompting for Everyone` (Andrew Ng) — 7h4m — from finding info to building apps.
- [ ] ✅ `ChatGPT Prompt Engineering for Developers` (OpenAI) — ~1h — zero/few-shot, CoT, instruction refinement.
- [ ] ✅ `Reasoning with o1` (OpenAI) — 1h44m — prompting reasoning models, sampling intuition.

**3.2 LLM integration**
- [ ] ✅ `Building Systems with the ChatGPT API` (OpenAI) — ~1h — chat completions, structured outputs, moderation.
- [ ] ✅ `LangChain for LLM Application Development` (LangChain) — ~1h30m — chains, memory, agents.
- [ ] ✅ `Functions, Tools and Agents with LangChain` (LangChain) — ~1h — tool/function calling.
- [ ] ✅ `LangChain: Chat with Your Data` (LangChain) — ~1h — RAG with LangChain (preview of Stage 4).
- [ ] ✅ `Serverless LLM Apps with Amazon Bedrock` (AWS) — ~1h — cloud provider auth, multi-model, cost/latency.

**3.3 AI-assisted engineering workflows**
- [ ] ✅ `Claude Code: A Highly Agentic Coding Assistant` (Anthropic) — 2h
- [ ] ✅ `Spec-Driven Development with Coding Agents` (JetBrains) — 1h16m
- [ ] ✅ `AI Coding Workflows: From Cloud to Local` (JetBrains) — 1h32m
- [ ] ✅ `AI Code Review` (Qodo) — 1h4m

### 📚 Resource Hub (Phase 3)

| Resource / Platform | Topics Covered | Where to Find It |
| :--- | :--- | :--- |
| **DeepLearning.AI** *(Short Courses)* | LangChain, RAG, prompt engineering, agents, evals | [deeplearning.ai/short-courses](https://deeplearning.ai) |
| **OpenAI Cookbook** *(Official)* | Embeddings, structured outputs, token optimization, evals | [cookbook.openai.com](https://cookbook.openai.com) |
| **Anthropic Docs** *(Official)* | Tool use, MCP, context engineering, prompt guidance | [docs.anthropic.com](https://docs.anthropic.com) |
| **LangChain Docs** *(Official)* | Chains, agents, RAG, tools | [python.langchain.com](https://python.langchain.com) |
| **LiteLLM Docs** *(Official)* | 100+ LLM providers, unified API, fallbacks | [docs.litellm.ai](https://docs.litellm.ai) |
| **Vercel AI SDK Docs** *(Official)* | Streaming, chat UI, tool calls, front-to-back AI features | [sdk.vercel.ai/docs](https://sdk.vercel.ai/docs) |

### 🎯 Milestone
`Strict Schema Data Extractor` — messy text → validated JSON via structured outputs + Pydantic, with retries and failure routing.

### 🛠️ Portfolio Project 1 (after the milestone): Strict Schema Data Extractor — 🔴 HIGH
- **Goal:** Send messy text (receipts, logs, emails) to an LLM and force clean, validated JSON against a schema.
- **Stack:** Python/Pydantic (or TypeScript/Zod), provider API, retries.
- **Skills:** Structured outputs, schema validation, repair loops, failure routing.
- **Eval:** Field-level accuracy on a hand-labeled set.

### 📌 Coverage & Notes
- **Coverage 3.1:** AI Prompting, ChatGPT Prompt Eng, Reasoning with o1 — ✅ Strong.
- **Coverage 3.2:** ChatGPT API, LangChain ×3, Bedrock — ✅ Strong (add Vercel AI SDK for UI).
- **Coverage 3.3:** Claude Code, Spec-Driven Dev, AI Code Review — ✅ Strong.
- **Gap:** LiteLLM / model routing & fallbacks — LiteLLM docs.

---

## 🔴 PHASE 4: Embeddings & RAG — HIGH PRIORITY
*The most common production AI pattern — grounding models in real data.*

### 🧠 Topic Checklist

#### 4.1 Embeddings & Vector Search
- [ ] Sentence & document embeddings (OpenAI embeddings, SBERT, Cohere, open models)
- [ ] Vector databases: ChromaDB, Qdrant, Pinecone, pgvector (pick one to start)
- [ ] KNN vs. ANN; what an index actually buys you
- [ ] Distance metrics and normalization (cosine, dot product, Euclidean)
- [ ] Embedding dimension, cost, and re-embedding strategy
- [ ] Metadata filtering and hybrid (dense + keyword) search
- [ ] FAISS basics (optional; useful for local experiments)

#### 4.2 RAG Architecture
- [ ] Full pipeline: ingest → parse → chunk → embed → store → retrieve → rerank → generate
- [ ] Chunking strategies: fixed-size, semantic, recursive, structure-aware
- [ ] Retrieval strategies: dense vs. sparse vs. hybrid
- [ ] Reranking and contextual compression
- [ ] Query transformation (rewriting, HyDE, multi-query)
- [ ] Citations & grounding; refusing when retrieval is empty
- [ ] RAG evaluation: retrieval metrics + answer groundedness/faithfulness
- [ ] Document Q&A and knowledge-grounded chatbots

**Skip:** Word2Vec, GloVe, FastText, classical NLP preprocessing pipelines. They are historically important and practically irrelevant to your stack.

### 🎓 DeepLearning.AI — Stage 4: Embeddings, Vector Search & RAG (Weeks 5–8 · ~35 h)

- [ ] 💳 `Retrieval Augmented Generation (RAG)` (DeepLearning.AI) — 26h3m — **the anchor**: architecture → chunking → retrieval → deployment → evaluation.
- [ ] ✅ `Advanced Retrieval for AI with Chroma` (Chroma) — 1h2m — reranking, query improvement, spotting bad retrieval.
- [ ] ✅ `Building and Evaluating Advanced RAG` (LlamaIndex / TruEra) — ~1h30m — retrieval + eval metrics.
- [ ] ✅ `Preprocessing Unstructured Data for LLM Applications` (Unstructured) — 1h22m — PDF/PPTX/HTML extraction.
- [ ] ✅ `Building AI Assistants with On-Device Memory` (Qdrant) — 1h4m — vector memory.
- [ ] ✅ `Multi-vector Image Retrieval` (Qdrant) — 1h43m — multimodal retrieval (optional).

**Shipping the RAG app (front-to-back bridge):**
- [ ] 💳 `Fast Prototyping of GenAI Apps with Streamlit` (Snowflake) — 9h21m — or build the UI yourself with the Vercel AI SDK (preferred for your goal).

### 📚 Resource Hub (Phase 4)

| Resource / Platform | Topics Covered | Where to Find It |
| :--- | :--- | :--- |
| **DeepLearning.AI** *(Short Courses)* | LangChain, RAG, prompt engineering, agents, evals | [deeplearning.ai/short-courses](https://deeplearning.ai) |
| **OpenAI Cookbook** *(Official)* | Embeddings, structured outputs, token optimization, evals | [cookbook.openai.com](https://cookbook.openai.com) |
| **LangChain Docs** *(Official)* | Chains, agents, RAG, tools | [python.langchain.com](https://python.langchain.com) |
| **ChromaDB Docs** *(Official)* | Vector database for RAG, local-first | [docs.trychroma.com](https://docs.trychroma.com) |
| **Qdrant Docs** *(Official)* | Vector search, filtering, hybrid retrieval | [qdrant.tech/documentation](https://qdrant.tech/documentation) |
| **FAISS Docs** *(Meta)* | Local similarity search | [github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss) |
| **HuggingFace Course** *(Free)* | Transformer concepts, embeddings, model landscape | [huggingface.co/learn](https://huggingface.co/learn) |
| **Vercel AI SDK Docs** *(Official)* | Streaming, chat UI, tool calls, front-to-back AI features | [sdk.vercel.ai/docs](https://sdk.vercel.ai/docs) |

### 🎯 Milestone
`Multi-Document RAG Application` — parse PDFs, chunk, embed in a vector DB, retrieve + rerank, answer with citations, and an eval set that scores retrieval.

### 🛠️ Portfolio Project 2 (after the milestone): Multi-Document RAG Application — 🔴 HIGH
- **Goal:** Ingest PDFs/docs, chunk and embed them, retrieve + rerank, and chat with citations.
- **Stack:** Vector DB (Chroma/Qdrant/pgvector), embedding model, LLM API, simple UI.
- **Skills:** Parsing, chunking, indexing, hybrid retrieval, reranking, grounding.
- **Eval:** Retrieval precision/recall@k + answer groundedness. **This eval is part of the deliverable.**

### 📌 Coverage & Notes
- **Coverage 4.1:** RAG course, On-Device Memory, Multi-vector — ✅ Strong.
- **Coverage 4.2:** RAG (26h), Advanced Retrieval, Advanced RAG, Unstructured — ✅ Strong.
- **Gap:** pgvector / production vector DB ops — Postgres + pgvector docs, Qdrant docs.
- **Gap:** Retrieval metrics (precision@k, MRR, nDCG) — Search/IR references, build the eval. *(Shared with Phase 0.)*

---

## 🔴 PHASE 5: Agents, Tool Use & Conversational UX — HIGH PRIORITY
*The difference between a demo and a product.*

### 🧠 Topic Checklist

#### 5.1 Agent Fundamentals
- [ ] Agent loop vs. DAG / workflow; when *not* to use an agent
- [ ] Tool/function calling: schemas, validation, error feedback to the model
- [ ] Planning, goal decomposition, and bounded autonomy
- [ ] Memory: conversation state, sliding window, summarization, long-term memory
- [ ] Multi-step and multi-agent orchestration (LangGraph, CrewAI)
- [ ] Human-in-the-loop checkpoints — where automation must stop
- [ ] Failure modes: loops, tool misuse, runaway cost, stale state

#### 5.2 Conversational Product Engineering
- [ ] Chatbot development: multi-turn state, history management, interrupts
- [ ] Streaming UX: token streaming, stop/cancel, optimistic UI, error states
- [ ] Conversation persistence and resumability
- [ ] Guardrails: input/output validation, PII handling, refusal behavior

#### 5.3 Domain Scoping (optional depth)
- [ ] Vertical agents: curated tool sets and domain terminology
- [ ] Domain knowledge injection via RAG or system prompts
- [ ] Compliance boundaries and domain-specific evaluation

### 🎓 DeepLearning.AI — Stage 5: Agents, Tool Use & Chat UX (Weeks 9–11 · ~20 h)

- [ ] 💳 `Agentic AI` (Andrew Ng) — 9h55m — **the anchor**: agent loops, reflection, tool use, planning.
- [ ] ✅ `Multi AI Agent Systems with crewAI` (crewAI) — 3h1m — multi-agent orchestration.
- [ ] ✅ `Long-Term Agentic Memory With LangGraph` (LangChain) — 1h24m — memory + state graphs.
- [ ] ✅ `Building Adaptive AI Agents` (Oracle) — 1h3m — agent traces → reusable skills.
- [ ] ✅ `DSPy: Build and Optimize Agentic Apps` (Databricks) — 59m — programmatic optimization.

**Chat UX (fill from docs, not courses):**
- [ ] Vercel AI SDK: streaming chat, tool calls, generative UI
- [ ] Conversation state, cancellation, error/retry states

**Optional:** `Building AI Browser Agents`, `Agentic Knowledge Graph Construction`, `Knowledge Graphs for AI Agent API Discovery` — only if your product needs them.

### 📚 Resource Hub (Phase 5)

| Resource / Platform | Topics Covered | Where to Find It |
| :--- | :--- | :--- |
| **DeepLearning.AI** *(Short Courses)* | LangChain, RAG, prompt engineering, agents, evals | [deeplearning.ai/short-courses](https://deeplearning.ai) |
| **Vercel AI SDK Docs** *(Official)* | Streaming, chat UI, tool calls, front-to-back AI features | [sdk.vercel.ai/docs](https://sdk.vercel.ai/docs) |
| **Anthropic Docs** *(Official)* | Tool use, MCP, context engineering, prompt guidance | [docs.anthropic.com](https://docs.anthropic.com) |
| **LangChain Docs** *(Official)* | Chains, agents, RAG, tools | [python.langchain.com](https://python.langchain.com) |
| **LangGraph Docs** *(Official)* | Agent orchestration, state graphs, multi-agent | [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph) |
| **CrewAI Docs** *(Official)* | Multi-agent orchestration | [docs.crewai.com](https://docs.crewai.com) |

### 🎯 Milestone
`The Autonomous Database Agent` — NL → safe tool calls → SQL/database → plain-English answer, with a human-review step for destructive actions.

### 🛠️ Portfolio Project 3 (after the milestone): The Autonomous Database/Tool Agent — 🔴 HIGH
- **Goal:** NL input → safe tool calls → database/API → plain-English answer, with human approval for risky actions.
- **Stack:** Tool calling, LangGraph or plain loop, sandboxed tools.
- **Skills:** Function calling, bounded autonomy, tool validation, human-in-the-loop.
- **Eval:** Task success rate + unsafe-action rate (should be zero).

### 📌 Coverage & Notes
- **Coverage:** Agentic AI, crewAI, LangGraph memory, DSPy + AI SDK docs — ✅ Strong.
- **Gap:** Domain-specific vertical agent patterns (Phase 5.3) — Build your own; no course exists.

---

## 🔴 PHASE 6: MCP & Applied LLM Engineering — HIGH PRIORITY
*Production patterns that turn a prototype into a reliable system.*

### 🧠 Topic Checklist
- [ ] MCP (Model Context Protocol): server/client architecture, tools, resources, prompts
- [ ] Building an MCP server that exposes your app's capabilities
- [ ] Building an MCP client with structured requests, retries, and timeouts
- [ ] Structured outputs & schema validation (Pydantic), with repair/retry loops
- [ ] Resiliency: error handling, exponential backoff, idempotency, rate limits
- [ ] Async processing (asyncio, concurrency, background jobs)
- [ ] Context engineering: prompt chaining, dynamic injection, progressive disclosure
- [ ] Prompt-injection defense and tool sandboxing
- [ ] Cost control: token budgeting, caching, model routing/fallbacks
- [ ] Composable agent skills (`grill-me`, `tdd`, `review`, `to-spec`, etc.)

### 🎓 DeepLearning.AI — Stage 6: MCP & Applied LLM Engineering (Weeks 12–13 · ~10 h)

- [ ] ✅ `MCP: Build Rich-Context AI Apps with Anthropic` (Anthropic) — 1h58m — **the MCP anchor**.
- [ ] ✅ `Build AI Apps with MCP Server: Working with Box Files` (Box) — 36m — MCP + multi-agent.
- [ ] ✅ `Pydantic for LLM Workflows` (DeepLearning.AI) — 1h50m — structured outputs, validation, retries.
- [ ] ✅ `Context Engineering` (DeepLearning.AI) — ~1–2h — dynamic context windows and scaffolds.
- [ ] ✅ `Safe and reliable AI via guardrails` (GuardrailsAI) — 1h42m — safety boundaries, PII, production guardrails.

### 📚 Resource Hub (Phase 6)

| Resource / Platform | Topics Covered | Where to Find It |
| :--- | :--- | :--- |
| **Anthropic Docs** *(Official)* | Tool use, MCP, context engineering, prompt guidance | [docs.anthropic.com](https://docs.anthropic.com) |
| **LiteLLM Docs** *(Official)* | 100+ LLM providers, unified API, fallbacks | [docs.litellm.ai](https://docs.litellm.ai) |
| **DeepLearning.AI** *(Short Courses)* | LangChain, RAG, prompt engineering, agents, evals | [deeplearning.ai/short-courses](https://deeplearning.ai) |

### 🎯 Milestone
Add MCP, schema validation, retries, and guardrails to Portfolio Project 3.

### 📌 Coverage & Notes
- **Coverage:** MCP ×2, Pydantic, Context Engineering, Guardrails — ✅ Strong.
- **Gap:** Prompt-injection defense & tool sandboxing (Phase 6–7) — OWASP LLM Top 10, provider security docs.

---

## 🔴 PHASE 7: Full-Stack AI Features (Front-to-Back) — HIGH PRIORITY
*The part the generic AI roadmap misses — and your biggest advantage as a full-stack dev.*

### 🧠 Topic Checklist
- [ ] Streaming chat UI end-to-end (SSE or AI SDK; React/Next.js integration)
- [ ] Server routes / API design for AI endpoints (timeouts, cancellation, retries)
- [ ] Auth & multi-tenancy for AI features (per-user/per-org isolation of data and vectors)
- [ ] Usage metering, quotas, and per-user cost attribution
- [ ] Caching layers: exact-match, semantic cache, prompt caching
- [ ] Persistence: conversations, messages, feedback, embeddings, job state
- [ ] File ingestion UX: upload → parse → index → status, with progress + failures
- [ ] Security: prompt injection, output handling/XSS, PII redaction, secret management
- [ ] Background/async workloads and long-running job orchestration
- [ ] Accessibility & failure UX for probabilistic outputs (retry, edit, regenerate)

**Recommended stack anchor:** Vercel AI SDK for the front-to-back streaming path, plus your existing backend/framework for persistence and business logic.

### 🎓 DeepLearning.AI — No dedicated stage

There is **no single DeepLearning.AI course for this phase** — it is build-driven. Use the Vercel AI SDK docs and your existing full-stack patterns (see Resource Hub and gaps below). *(The Stage 4 Streamlit option and the Stage 5 Vercel AI SDK chat-UX items feed into this phase.)*

### 📚 Resource Hub (Phase 7)

| Resource / Platform | Topics Covered | Where to Find It |
| :--- | :--- | :--- |
| **Vercel AI SDK Docs** *(Official)* | Streaming, chat UI, tool calls, front-to-back AI features | [sdk.vercel.ai/docs](https://sdk.vercel.ai/docs) |
| **OpenAI Cookbook** *(Official)* | Embeddings, structured outputs, token optimization, evals | [cookbook.openai.com](https://cookbook.openai.com) |

### 🎯 Milestone
`Full-Stack AI Product` — a real app with auth, tenancy, streaming UI, RAG, one agentic workflow, usage limits, and eval dashboards.

### 🛠️ Portfolio Project 4 (after the milestone): Full-Stack AI Product (Capstone) — 🔴 HIGH
*A rolling, 3-phase project that mirrors real product development.*

**Phase 1 — Foundation**
- [ ] Auth + multi-tenancy (users/orgs, data isolation)
- [ ] Core domain model + database
- [ ] LLM integration with structured outputs
- [ ] Streaming server endpoint + basic chat UI

**Phase 2 — Intelligence & Workflow**
- [ ] RAG over the product's own data, with citations
- [ ] One agentic workflow with tools and human-in-the-loop
- [ ] MCP server exposing app capabilities (and/or an MCP client)
- [ ] Guardrails, PII handling, prompt-injection defenses
- [ ] Usage metering, quotas, caching, cost controls
- [ ] Dockerize the stack

**Phase 3 — Production**
- [ ] Evaluation harness with golden dataset + regression gates
- [ ] Tracing, observability, quality/latency/cost dashboard
- [ ] CI/CD with eval gates and config/prompt versioning
- [ ] Failure UX, rate limiting, rollback plan, compliance notes

> **Note:** Project 4 is a rolling capstone. Its Phase 1 lands here; Phase 2 draws on Phase 6 (MCP, guardrails) and Phase 9 (Docker); Phase 3 draws on Phase 8 (eval/observability) and Phase 9 (CI/CD, rollback).

### 📌 Coverage & Notes
- **Coverage:** *(no single course — build + AI SDK docs)* — ⚠️ Build-driven.
- **Gap:** Streaming chat UI / front-to-back AI UX — Vercel AI SDK docs, build it.
- **Gap:** Auth, multi-tenancy & per-user cost isolation — Your existing full-stack patterns.

---

## 🔴 PHASE 8: Evaluation & Observability — HIGH PRIORITY
*The single most differentiating AI engineering skill. Treat it as a deliverable, not an afterthought.*

### 🧠 Topic Checklist
- [ ] Build a golden dataset: representative inputs + expected properties
- [ ] Deterministic checks vs. LLM-as-judge; when each is appropriate
- [ ] Retrieval evals (precision@k, recall@k, MRR) and answer evals (groundedness, relevance, safety)
- [ ] Regression testing prompts and models across versions
- [ ] Online evaluation: user feedback, thumbs, correction capture
- [ ] Tracing & observability: LangFuse / OpenTelemetry / provider dashboards
- [ ] Quality/latency/cost dashboards; alerting on failure modes
- [ ] A/B testing model or prompt changes safely

### 🎓 DeepLearning.AI — Stage 7: Evaluation & Observability (Weeks 14–15 · ~10 h)

- [ ] ✅ `Evaluating AI Agents` (Arize AI) — 2h36m — structured assessments, iteration.
- [ ] LangFuse docs — tracing, datasets, evals, cost dashboards (hands-on).
- [ ] Build your own eval harness for Projects 2–4 (golden set + regression gate).

### 📚 Resource Hub (Phase 8)

| Resource / Platform | Topics Covered | Where to Find It |
| :--- | :--- | :--- |
| **LangFuse** *(Open Source)* | LLM observability, tracing, evals, cost | [langfuse.com/docs](https://langfuse.com/docs) |
| **OpenAI Cookbook** *(Official)* | Embeddings, structured outputs, token optimization, evals | [cookbook.openai.com](https://cookbook.openai.com) |
| **DeepLearning.AI** *(Short Courses)* | LangChain, RAG, prompt engineering, agents, evals | [deeplearning.ai/short-courses](https://deeplearning.ai) |

### 🎯 Milestone
Add an eval harness + tracing + a quality/latency/cost dashboard to Portfolio Project 4, with a documented baseline.

### 📌 Coverage & Notes
- **Coverage:** Evaluating AI Agents + LangFuse docs — ✅ Strong (hands-on required).
- **Gap:** LangFuse + OpenTelemetry tracing — LangFuse docs, OpenTelemetry docs.

---

## 🟡 PHASE 9: Deployment & LLMOps — MEDIUM PRIORITY
*You already know DevOps — adapt it for AI workloads. API-first; self-hosting is optional.*

### 🧠 Topic Checklist
- [ ] Containerize the AI service (multi-stage builds)
- [ ] Serving APIs via FastAPI (or your existing backend framework)
- [ ] CI/CD including prompt/config versioning and eval gates
- [ ] Secrets, environment separation, and provider key management
- [ ] Rate limiting, request queuing, retries, and graceful degradation
- [ ] Model/config versioning and rollback
- [ ] Ethics, compliance & responsible AI (bias, hallucination guards, PII, retention)

**Optional, only if self-hosting:** vLLM, batching, GPU/VRAM management, Cerebras/other inference providers. Most product roles call hosted APIs instead.

### 🎓 DeepLearning.AI — Stage 8: Deployment & LLMOps (Weeks 15–16 · ~8 h)

- [ ] ✅ `Orchestrating Workflows for GenAI Applications` (Astronomer) — 1h48m — background/async pipelines.
- [ ] Vercel/your host: deploy the full-stack AI product with secrets and rate limiting.
- [ ] CI/CD with prompt/config versioning + eval gates.

**Skip unless self-hosting:** `Fast & Efficient LLM Inference with vLLM`, `Efficiently Serving LLMs`, `Fast LLM Inference with Cerebras`. Hosted APIs are the product default.

### 📚 Resource Hub (Phase 9)

| Resource / Platform | Topics Covered | Where to Find It |
| :--- | :--- | :--- |
| **vLLM Docs** *(Official)* | Self-hosted inference (optional) | [docs.vllm.ai](https://docs.vllm.ai) |

### 🎯 Milestone
Deploy Portfolio Project 4 with CI eval gates, tracing, and a rollback plan.

### 📌 Coverage & Notes
- **Coverage:** Airflow, deploy hands-on — ✅ Sufficient.
- **Gap:** Self-hosting / vLLM / quantization *(optional)* — vLLM docs, llama.cpp docs. *(Also listed in the Deferred ML-Engineer track.)*

---

## 🟢 DEFERRED / OPTIONAL: The ML-Engineer Track
*Everything below is intentionally out of scope for your target role. Revisit only if you pivot toward model training.*

- [ ] Classical ML: linear/logistic regression, decision trees, random forests, XGBoost
- [ ] Deep learning: neural networks, backpropagation, CNNs, RNNs, LSTMs, GANs
- [ ] Reinforcement learning and RLHF/GRPO
- [ ] Pretraining, full fine-tuning, LoRA/QLoRA
- [ ] Classical NLP: Word2Vec, GloVe, FastText, spaCy NER pipelines
- [ ] GPU internals, CUDA setup, local quantization (Llama.cpp/GGUF)
- [ ] Research reasoning benchmarks (TruthfulQA, BBH, GSM8K)

**Resources for this track:** vLLM docs, llama.cpp docs (self-hosting / quantization).

---

## 🟢 OPTIONAL DEPTH: DeepLearning.AI — Stage 9 (Weeks 17+)

- [ ] ✅ `Post-training of LLMs` (UW / NexusFlow) — 1h26m — SFT, DPO, online RL (concepts only).
- [ ] ✅ `Reasoning with o1` (OpenAI) — 1h44m *(repeat for depth)*.
- [ ] ✅ `Introducing Multimodal Llama 3.2` (Meta) — 1h39m — only if your product is multimodal.
- [ ] ✅ `Voice for AI Agents and Applications` (Vocal Bridge) — 1h26m — only if voice is in scope.
- [ ] ✅ `Document AI: From OCR to Agentic Doc Extraction` (LandingAI) — 3h11m — useful for ingestion-heavy products.

🎯 **Milestone:** Extend Portfolio Project 4 with whichever optional capability is relevant to your product.

---

## 🧭 Suggested Cadence

1. **Weeks 1–2** — Stages 0–2 (orientation, ML literacy, LLM literacy). Cheap and fast; no ML specialization.
2. **Weeks 3–4** — Stage 3 (prompting + integration + AI coding). Mostly free; ship Project 1.
3. **Weeks 5–8** — Stage 4 (RAG). The anchor course; ship Project 2 **with evals**.
4. **Weeks 9–11** — Stage 5 (agents + chat UX). Ship Project 3.
5. **Weeks 12–15** — Stages 6–7 (MCP, applied engineering, eval/observability).
6. **Weeks 15–16** — Stage 8 (deployment). Finish and deploy Project 4.
7. **Week 17+** — Stage 9 optional depth, driven by your product.

**Subscription strategy:** stay free through Stages 0–1 and most of Stage 3. Buy **Pro for ~2 months** to cover `RAG` (Stage 4) + `Agentic AI` (Stage 5), then cancel. Everything else is free short courses plus docs and building. Expected total cost is far lower than the old plan — and you skip ~200 hours of ML theory you would never use.
