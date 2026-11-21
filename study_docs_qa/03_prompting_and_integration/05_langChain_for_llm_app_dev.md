# LangChain for LLM Application Development — Q&A

---

## Part 1 — Introduction

### LangChain

**Q: What is LangChain?**
A: An open-source framework for building **LLM applications** in Python and JavaScript/TypeScript. It is built for **composition**: small pieces you combine into an app.

**Q: What two values does LangChain provide?**
A: **Modular components** you can use alone (models, prompts, indexes, memory), and **use cases** — prebuilt ways to combine those pieces into chains and agents.

**Q: Which components does the course cover?**
A: **Models** (LLMs, chat models, embeddings), **prompts** (templates and parsers), **indexes** (load your data), **memory**, **chains** (fixed sequences of calls), and **agents** (the model chooses tools).

---

## Part 2 — Models, prompts and parsers

### Models

**Q: Why wrap an LLM in LangChain instead of calling the provider API directly?**
A: Direct calls work for one prompt. LangChain adds reusable **prompt templates**, a common model interface so you can switch providers, and **output parsers** so code receives structured data instead of a raw string.

**Q: How do you call a chat model in LangChain?**
A: `ChatOpenAI(temperature=0.0)` builds a chat model. Pass a list of messages with `chat.invoke(messages)` and read `response.content`. Load `OPENAI_API_KEY` from the environment (e.g., `python-dotenv`); do not hard-code it. The model object is not callable — `chat(...)` raises `TypeError`.

**Q: What does `temperature` control?**
A: Sampling randomness. Use `temperature=0.0` when you need a stable, repeatable completion (extraction, routing, eval). Raise it when you want more varied wording.

### Prompt templates

**Q: What is a prompt template?**
A: A reusable string with `{variables}` that you fill at run time. `ChatPromptTemplate.from_template(template)` builds one; `format_messages(...)` substitutes the variables and returns chat messages.

**Q: Why use a template instead of an f-string?**
A: The same instructions can run on many inputs and models without rewriting the prompt. Templates also pair with parsers: you inject format instructions as another variable rather than editing the text by hand.

**Q: What is the order of creation and execution for a LangChain prompt?**
A: Create objects first, then run them: (1) `chat = ChatOpenAI(model=..., temperature=...)`, (2) write a template string with `{placeholders}`, (3) `ChatPromptTemplate.from_template(template)`, (4) `messages = prompt.format_messages(...)` to fill placeholders, (5) `response = chat.invoke(messages)`, (6) read `response.content` (a string). For structured output, also (7) define `ResponseSchema(name, description)` fields, (8) `StructuredOutputParser.from_response_schemas(...)`, (9) put `parser.get_format_instructions()` into the template as `{format_instructions}`, (10) `parser.parse(response.content)` to get a `dict`.

### Output parsers

**Q: What is an output parser?**
A: A component that turns the model's **text** into a Python object. Language models emit strings; parsers let the rest of the program use a `dict` (or other type) instead of scraping the reply.

**Q: How do you parse a structured JSON reply?**
A: (1) Define one `ResponseSchema(name, description)` per field. (2) `StructuredOutputParser.from_response_schemas(...)`. (3) Put `parser.get_format_instructions()` into the prompt. (4) Call the model, then `parser.parse(response.content)` to get a `dict`.

**Q: Why can you not treat the raw completion as a dictionary?**
A: The completion is a string. Indexing it as `response.content["field"]` fails until you parse it.

---

## Part 3 — Memory

### Why memory exists

**Q: Are LLM API calls stateful?**
A: No. Each call sees only the messages you send. **Memory** stores prior turns and injects them into the next prompt so a chatbot can refer to earlier facts.

**Q: How do you attach memory to a conversation?**
A: Build a `ConversationChain(llm=..., memory=..., verbose=True)`. The chain prepends `memory.load_memory_variables({})` (usually a `history` string) to the new user input. `save_context({"input": ...}, {"output": ...})` writes a turn by hand.

### Memory types

**Q: What does `ConversationBufferMemory` store?**
A: The **full** transcript. `memory.buffer` is the raw text; `load_memory_variables({})` returns `{"history": "..."}`. It is simple and accurate, but it grows until it hits the model's **context window**.

**Q: What does `ConversationBufferWindowMemory` keep?**
A: Only the last `k` exchanges (`ConversationBufferWindowMemory(k=1)` keeps one). Older turns are dropped, so the model forgets facts that fell out of the window.

**Q: What does `ConversationTokenBufferMemory` keep?**
A: A recent buffer limited by **token count**, not by number of turns: `ConversationTokenBufferMemory(llm=llm, max_token_limit=n)`. It needs the `llm` so it can count tokens with that model's tokenizer.

**Q: What does `ConversationSummaryBufferMemory` keep?**
A: A running **summary** of older turns plus recent raw text, flushed when `max_token_limit` is exceeded. An LLM writes the summary, so you pay extra calls to compress history instead of dropping it.

**Q: What other memory backends does the course mention?**
A: **Vector-store memory** retrieves the most relevant past spans by embedding similarity. **Entity memory** uses an LLM to track facts about named entities. You can also persist conversation state in a key-value store or SQL.

---

## Part 4 — Chains

### LLMChain and sequential chains

**Q: What is a chain?**
A: A sequence of calls to components (LLMs, prompts, other chains). The basic unit is `LLMChain(llm=..., prompt=...)`: fill the template, call the model, return the text. `chain.run(...)` or the named inputs execute it.

**Q: What is `SimpleSequentialChain`?**
A: A pipeline where each step has **one** input and **one** output, and the output of step `n` is the input of step `n+1`. `SimpleSequentialChain(chains=[chain_one, chain_two], verbose=True)` runs them in order.

**Q: What is `SequentialChain`?**
A: A pipeline with **named** inputs and outputs. Each `LLMChain` sets `output_key`; later steps read those keys. `SequentialChain(..., input_variables=[...], output_variables=[...])` can fan one input into several chains and keep every intermediate field.

**Q: When do you use `verbose=True`?**
A: When you need to see the formatted prompt and intermediate outputs. It is the first debugging switch for chains.

### Router chains

**Q: What is a router chain?**
A: A chain that **selects** which specialist chain should handle the input. `MultiPromptChain` holds `destination_chains` (one `LLMChain` per prompt), a `default_chain` for unmatched input, and an `LLMRouterChain` that picks the destination.

**Q: How does the router decide?**
A: `LLMRouterChain` uses a prompt (`MULTI_PROMPT_ROUTER_TEMPLATE`) that lists each destination **name** and **description**. The model returns JSON `{"destination": ..., "next_inputs": ...}`; `RouterOutputParser` reads it. `destination` must be a known name or `"DEFAULT"`.

---

## Part 5 — Question answering over documents

### Embeddings and retrieval

**Q: How do you answer questions over your own data?**
A: Combine retrieval with an LLM: load documents, embed them, store vectors, retrieve the chunks most similar to the question, then ask the model to answer using those chunks.

**Q: What is an embedding?**
A: A numeric **vector** that captures meaning. Texts with similar content have similar vectors, so you can rank documents by similarity to a query vector instead of by keyword overlap.

**Q: What is the retrieval pipeline in this course?**
A: (1) Load files (`CSVLoader`). (2) Embed each document (`OpenAIEmbeddings`). (3) Store vectors (`DocArrayInMemorySearch.from_documents`). (4) Embed the query. (5) `similarity_search(query)` (or `as_retriever()`). (6) Pass the hits plus the question to the LLM.

**Q: What does `VectorstoreIndexCreator` do?**
A: A shortcut that builds the vector store from loaders: `VectorstoreIndexCreator(vectorstore_cls=DocArrayInMemorySearch).from_loaders([loader])`, then `index.query(query)`.

**Q: What is `RetrievalQA`?**
A: A chain that runs retriever then LLM: `RetrievalQA.from_chain_type(llm=..., chain_type="stuff", retriever=..., verbose=True)`. The retriever supplies documents; the chain type decides how they are packed into prompts.

### Chain types

**Q: What does `chain_type="stuff"` do?**
A: It **stuffs** every retrieved document into one prompt. One LLM call sees all the evidence together. It fails when the combined text exceeds the context window.

**Q: What is map-reduce over documents?**
A: Call the LLM on **each** chunk with the question, then call it again to combine those answers. It scales to many documents at the cost of more calls.

**Q: What is refine?**
A: Answer from the first document, then **update** that answer with each next document in sequence. It is sequential and slower, but it can incorporate a long corpus piece by piece.

**Q: What is map-rerank?**
A: Score an answer from each chunk, then keep the **highest-scoring** one. There is no merge across chunks, so it prefers a single strong passage.

---

## Part 6 — Evaluation

### Example generation

**Q: How do you build an eval set for a Q&A chain?**
A: Write a few `{query, answer}` examples by hand from the documents, and/or generate more with `QAGenerateChain.from_llm(...)`, which proposes question–answer pairs from each document. Combine both lists.

### Manual evaluation

**Q: How do you inspect what a chain actually sent to the model?**
A: Set `langchain.debug = True`. Each step prints its inputs and outputs (retrieved docs, stuffed prompt, completion). Turn it off with `langchain.debug = False`.

### LLM-assisted evaluation

**Q: How does LLM-assisted evaluation work?**
A: Run the Q&A chain on each example, then `QAEvalChain.from_llm(llm).evaluate(examples, predictions)`. A second model grades predicted vs. expected answers (typically `CORRECT` / `INCORRECT`) so you are not limited to exact string match.

**Q: Why not only exact match?**
A: A correct paraphrase fails string equality. The eval chain judges **meaning**, which fits open-ended Q&A.

---

## Part 7 — Agents

### Tools and ReAct

**Q: What is an agent?**
A: A loop where the LLM is a **reasoning engine**: it chooses a **tool**, reads the tool's result, and repeats until it can answer. Unlike a chain, the number and order of steps are not fixed in advance.

**Q: How do you create an agent with built-in tools?**
A: `tools = load_tools(["llm-math", "wikipedia"], llm=llm)` then `initialize_agent(tools, llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True, verbose=True)`. `llm-math` does calculation; Wikipedia looks up facts.

**Q: What does `CHAT_ZERO_SHOT_REACT_DESCRIPTION` mean?**
A: A **ReAct** agent (reason, then act) that uses the chat model and each tool's **description** to pick a tool, with no few-shot tool-use examples.

**Q: What is a Python agent?**
A: `create_python_agent(llm, tool=PythonREPLTool(), verbose=True)` gives the model a Python REPL so it can write and run code (e.g., process a list) instead of guessing the result.

**Q: How do you add a custom tool?**
A: Decorate a function with `@tool` and write a precise **docstring**. The agent uses that description to decide **when** to call it; the type hints describe the input. Register it by appending the function to the tools list.

**Q: Why is the tool docstring so important?**
A: The model never sees your Python. It only sees the name and description, so a vague docstring leads it to skip the tool or call it at the wrong time.

**Q: Do agents always succeed?**
A: No. They can pick the wrong tool, misparse an action, or conclude incorrectly. `handle_parsing_errors=True` recovers from some format mistakes, but you may still need to retry — the course treats agents as powerful but unfinished.

---

## Part 8 — Conclusion

### What you can build

**Q: How do the pieces fit into an application?**
A: Templates and parsers call models; memory keeps chat state; chains fix a pipeline; retrieval adds private data; eval checks quality; agents choose tools when the path is not known in advance. Combined, that is enough to build assistants and specialized chatbots in hours rather than weeks.

**Q: How stable is the LangChain API?**
A: The project moves quickly. The ideas (templates, parsers, memory, chains, retrieval, agents) stay; class names and import paths may change. Prefer the abstractions, and expect to update calls as the library evolves.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| LangChain | Open-source framework to compose LLM apps from modular components |
| `ChatOpenAI` | Chat-model wrapper; call with `.invoke(messages)`, not `chat(...)` |
| Prompt template | Reusable prompt with `{variables}`; `ChatPromptTemplate.from_template` |
| Prompt workflow | model → template → `format_messages` → `invoke` → `content` (then parse) |
| Output parser | Turns model text into a typed object (`StructuredOutputParser`) |
| `ResponseSchema` | Name plus description of one field to extract |
| Memory | Stored turns injected into the next prompt; the API itself is stateless |
| Buffer memory | Full transcript; can overflow the context window |
| Window memory | Last `k` exchanges only |
| Token buffer memory | Recent turns up to `max_token_limit` tokens |
| Summary buffer memory | LLM-compressed older history plus recent raw turns |
| `LLMChain` | Prompt plus model; the basic chain |
| `SimpleSequentialChain` | One-in, one-out steps piped in order |
| `SequentialChain` | Named inputs/outputs shared across steps |
| Router / `MultiPromptChain` | LLM picks a destination chain or `DEFAULT` |
| Embedding | Vector of meaning; similar text → similar vectors |
| Vector store | Index of embeddings you can `similarity_search` |
| `RetrievalQA` | Retriever plus LLM; `chain_type` packs documents into prompts |
| Stuff / map-reduce / refine / map-rerank | One prompt vs. per-chunk then combine vs. sequential update vs. best score |
| `QAGenerateChain` | LLM writes question–answer eval examples from documents |
| `QAEvalChain` | LLM grades a predicted answer against an expected one |
| `langchain.debug` | Print every chain step's inputs and outputs |
| Agent | LLM chooses tools in a loop (ReAct) until it can answer |
| `@tool` | Registers a function; the docstring is what the agent reads |

---
