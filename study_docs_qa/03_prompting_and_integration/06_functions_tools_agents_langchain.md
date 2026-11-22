# Functions, Tools and Agents with LangChain — Q&A

---

## Part 1 — OpenAI tool calling

### What tool calling is

**Q: What is OpenAI tool calling?**
A: You pass JSON **tool** schemas and the model may reply with a tool name plus arguments instead of free text. The model does not run your Python. Your code runs the function, then a **second** call sends that result back so the model can answer in text. The older name for this is function calling.

**Q: What does a tool schema contain?**
A: A dict with `"type": "function"` and a `"function"` object: `name`, `description`, and `parameters`. `parameters` is a JSON Schema with `type`, `properties`, and `required`. Each property has a `type`, a `description`, and optionally an `enum`. The description steers when the model chooses that tool and how it fills each field.

**Q: How do you request a tool call?**
A: `client = OpenAI()` then `client.chat.completions.create(model="gpt-5-nano", messages=messages, tools=tools)`. The completion is an object. Read `response.choices[0].message`. Indexing `response["choices"]` raises `TypeError` because a `ChatCompletion` is not a dict.

**Q: How do you tell a tool call from a normal reply?**
A: A tool call has `content` equal to `None` and a `tool_calls` list. Each item has `.id`, `.function.name`, and `.function.arguments`. `arguments` is a JSON **string**; `json.loads` turns it into a dict you pass with `get_current_weather(**args)`. A normal reply fills `content` and leaves `tool_calls` empty.

### Call modes

**Q: What does `tool_choice` control?**
A: Whether a call is allowed. `"auto"` (the default) lets the model decide; `"none"` forbids every call, so the model answers in text and may invent the fact; `{"type": "function", "function": {"name": "<tool>"}}` forces that tool even on a greeting, so the arguments may not match the user's intent.

### Sending the result back

**Q: Why are there two model calls?**
A: The first call only builds the request: a tool name and JSON arguments, with no weather data in the reply. Your code runs `get_current_weather`. The second call sees that result in the conversation and writes the sentence the user reads. One call cannot both request the tool and know its return value.

**Q: How do you finish the round trip after a tool call?**
A: (1) Append the assistant message: `messages.append(response.choices[0].message)`. (2) Read `tool_call = response.choices[0].message.tool_calls[0]`, parse `tool_call.function.arguments`, and run the function. (3) Append `{"role": "tool", "tool_call_id": tool_call.id, "content": observation}`. This role sits beside `user` and `assistant`, and `tool_call_id` must match the call it answers. (4) Call the model again so it answers from that observation. The second completion can omit `tools`.

---

## Part 2 — LangChain Expression Language

### The pipe

**Q: What is LangChain Expression Language (LCEL)?**
A: A way to compose **Runnables** with `|`. Each step's output is the next step's input. `chain = prompt | model | output_parser` is a chain you call with `chain.invoke({...})`.

**Q: What are the three pieces of a minimal chain?**
A: `ChatPromptTemplate.from_template` holds a string with `{variables}`. `ChatOpenAI` is the chat model. `StrOutputParser` turns the `AIMessage` into a plain string so later steps do not have to read `.content`.

### RunnableParallel

**Q: What does `RunnableParallel` do?**
A: It runs several steps on the **same** input and returns a dict of named outputs. `RunnableMap` is the same class. Use it when the next prompt needs derived fields, such as retrieved context plus the original question.

**Q: How do you ground a chain on retrieved text?**
A: `InMemoryVectorStore.from_texts(..., embedding=OpenAIEmbeddings())` builds an in-memory store; `vectorstore.as_retriever()` searches it. A `RunnableParallel` sets `context` from `retriever.invoke(question)` and copies `question` through. The prompt tells the model to answer only from `{context}`.

### Bind

**Q: What does `bind_tools` do?**
A: `model.bind_tools(tools)` returns a new runnable that sends those tools on every call, so you pipe `prompt | model_with_tools`. Call `bind_tools` again to replace the list. Given several tools, the model picks the one whose description matches the question and fills that tool's arguments. Pass `tool_choice` on the same call: `"auto"`, `"none"`, `"required"`, or one tool name.

### Fallbacks

**Q: What does `with_fallbacks` do?**
A: `chain.with_fallbacks([other])` runs `chain` first and, if it raises, runs the next chain. Use it when a weaker model emits text that `json.loads` cannot parse: the fallback is a chat model piped through `StrOutputParser()` and then `json.loads`.

### Runnable interface

**Q: Which methods does every LCEL chain support?**
A: `invoke` for one input, `batch` for a list of inputs, and `stream` to yield chunks as they arrive. The async forms are `ainvoke`, `abatch`, and `astream`.

---

## Part 3 — Tool calling in LangChain

### Pydantic models

**Q: Why define tool inputs as Pydantic models?**
A: A `BaseModel` validates types, so a `str` cannot land in an `int` field the way it can on a plain class. Nest models with fields such as `students: list[User]`.

### Schema conversion

**Q: How do you turn a Pydantic model into an OpenAI tool?**
A: `convert_to_openai_tool(Model)` returns `{"type": "function", "function": {name, description, parameters}}`. The class name is the tool name. The class docstring is the description; with no docstring the description is an empty string. `Field(description=...)` becomes each parameter's description. A typed field without `Field` still converts, but with no parameter description.

**Q: How do you attach that tool to a chat model?**
A: `model.bind_tools([Model])` sends it on every call. Pipe the bound model as `prompt | model_with_tools`. When you want the parsed object back instead of a tool call your code runs, use `model.with_structured_output(Model)`.

### Forcing and choosing

**Q: How do you force a Pydantic tool?**
A: `model.bind_tools([Model], tool_choice="ClassName")`. The name must match the class. The model then calls that tool even when the user only says hello. The same force is `tool_choice={"type": "function", "function": {"name": "ClassName"}}`.

**Q: How does the model choose among several tools?**
A: Bind the list and leave `tool_choice` on `"auto"`. It picks from the docstrings and field descriptions. If none apply, it answers in `content` and leaves `tool_calls` empty.

---

## Part 4 — Tagging and extraction

### Tagging

**Q: What is tagging?**
A: Assigning labels to a piece of text as structured fields, such as `sentiment` (`pos`, `neg`, or `neutral`) and `language` (an ISO 639-1 code). Put the allowed values in the `Field` description. That description is the instruction the model follows.

**Q: How do you make tagging always return the schema?**
A: `model.with_structured_output(Tagging)`, with a system message that says to tag as instructed. `prompt | structured` returns a `Tagging` instance. `gpt-5-nano` only accepts temperature `1`. To stay on the tool-call path, `bind_tools([Tagging], tool_choice="Tagging")` and parse with `PydanticToolsParser(tools=[Tagging], first_tool_only=True)`.

### Extraction

**Q: How does extraction differ from tagging?**
A: Tagging labels the whole text. **Extraction** pulls out zero or more entities. Wrap them in a model with a list field (`people: list[Person]`) and use `str | None` for attributes that may be missing.

**Q: How do you stop the model from guessing missing fields?**
A: Say so in the system prompt: extract only what is explicit, allow partial records, and allow an empty list. A vague prompt makes the model invent titles, names, or counts that are not in the text.

**Q: How do you unwrap one field from the result?**
A: `with_structured_output` returns the whole model. Read the field, such as `result.people`. `JsonOutputKeyToolsParser(key_name="People", first_tool_only=True)` returns the arguments of the tool **named** `People`, not one key inside those arguments. `JsonOutputToolsParser` returns the tool calls as a list of dicts with `type` and `args`.

### Long documents

**Q: How do you extract over a long document in one chain?**
A: One call only sees the text you send, so a prefix drops later mentions. Split with `RecursiveCharacterTextSplitter(chunk_overlap=0)`, map the string to `[{"input": chunk}, ...]` with a `RunnableLambda`, run `extraction_chain.map()`, and flatten: `prep | extraction_chain.map() | flatten`. A plain function at the end of a pipe is treated as a runnable. `.batch()` runs the same per-item step.

---

## Part 5 — Tools and routing

### Defining a tool

**Q: What does `@tool` do?**
A: It turns a Python function into a LangChain **tool**. `name` comes from the function name, `description` from the docstring, and `args` from the signature. The model only sees that name and description, so a vague docstring makes it skip the tool or call it at the wrong time.

**Q: When do you pass `args_schema`?**
A: When each argument needs a description the signature does not carry. `@tool(args_schema=Model)` uses a Pydantic model with `Field` descriptions. Call the tool with `tool.invoke({...})`.

**Q: How do you give tools to the model?**
A: `ChatOpenAI(model="gpt-5-nano", temperature=1).bind_tools(tools)`. `bind_tools` builds the OpenAI tool schema from each `@tool`. The body (an HTTP call, a search client, anything else) runs only when your code calls `tool.invoke`.

### OpenAPI

**Q: How do you expose an HTTP API as tools?**
A: `OpenAPISpec.from_text(spec)` parses an OpenAPI document. `openapi_spec_to_openai_fn` is deprecated. Bind the operations with `bind_tools` and run the chosen call with an HTTP client. `APIOperation.from_openapi_spec(spec, path, method)` is one operation you can turn into a tool.

### Routing

**Q: What is routing with tool calling?**
A: Binding several tools and letting the model pick from their descriptions. A weather question calls the weather tool; a definition question calls search. A router runs at most one tool and stops.

**Q: What does `OpenAIToolsAgentOutputParser` return?**
A: If the model called tools, a list of actions with `.tool`, `.tool_input`, `.tool_call_id`, and `.message_log`. If it answered in text, an `AgentFinish` whose `.return_values["output"]` is that text.

**Q: How do you run the chosen tool in the chain?**
A: On `AgentFinish`, return `return_values["output"]`. Otherwise call `tool.invoke(action.tool_input)` for `action.tool`. You can skip the parser and read `response.tool_calls`: each item has `"name"`, `"args"`, and `"id"`. The chain stops after that result or the model's text.

---

## Part 6 — Conversational agent

### The agent loop

**Q: How is an agent different from a router?**
A: A **router** calls at most one tool and stops. An **agent** lets the model see each observation and then either call another tool or finish with a natural-language answer. It repeats until the parser returns `AgentFinish`. That loop is the same two-call round trip, repeated.

**Q: What is the agent scratchpad?**
A: Tool calls and observations from the **current** user turn. Put `MessagesPlaceholder("agent_scratchpad")` after the user message. `("placeholder", "{agent_scratchpad}")` is the same slot. `chat_history` is a different placeholder: it holds prior turns.

**Q: What does one pass of the agent loop look like?**
A: Keep `intermediate_steps` as `(action, observation)` pairs and pass `format_to_tool_messages(intermediate_steps)` in as the scratchpad (empty on the first pass). That helper rebuilds the assistant tool call plus a `ToolMessage` (`role` `"tool"`, matching `tool_call_id`). If the result is `AgentFinish`, return it; otherwise run the tool, append `(result, observation)`, and invoke again.

**Q: How do you build the scratchpad inside the chain?**
A: `RunnablePassthrough.assign(agent_scratchpad=lambda x: format_to_tool_messages(x["intermediate_steps"]))` adds that key and keeps `input` and `intermediate_steps`. The caller then passes steps in, and the assign step formats them.

### Executor and memory

**Q: What does `AgentExecutor` replace?**
A: The handwritten `while` loop and the manual name-to-tool dict. `create_tool_calling_agent(llm, tools, prompt)` builds the agent. `AgentExecutor(agent=agent, tools=tools, verbose=True)` looks up each action by name, runs it, stops on `AgentFinish`, and returns a dict whose answer is `output`. Classic ReAct agents send `stop` sequences, which `gpt-5-nano` rejects, so use this tool-calling agent.

**Q: Why does the agent forget facts from the previous invoke?**
A: Each `invoke` sends only that call's input unless you attach memory. Add `MessagesPlaceholder("chat_history")` before the user message, and pass `ConversationBufferMemory(return_messages=True, memory_key="chat_history")` to the executor. `return_messages=True` is required because the placeholder expects a list of messages, and `memory_key` must match the placeholder name.

**Q: How do you add your own tool?**
A: Decorate a function with `@tool`, write a docstring that says when to use it, and append it to `tools`. Pass that list to `create_tool_calling_agent` or `bind_tools`. The executor runs whatever the model selects.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Tool calling | Model returns a tool name and JSON arguments; your code runs the function, then a second call answers from the result |
| Tool schema | `{"type": "function", "function": {name, description, parameters}}`; `parameters` is JSON Schema |
| `tool_choice` | `"auto"` (model decides), `"none"` (never call), `"required"` (must call one), or a tool name / `{"type": "function", "function": {"name": ...}}` |
| `tool_calls` | List on the assistant message; `.function.arguments` is a JSON string, `.id` links the result |
| Tool message | `{"role": "tool", "tool_call_id", "content"}` carrying the function result back to the model |
| Two calls | First call requests the tool; your code runs it; second call writes the answer |
| LCEL | Compose Runnables with the pipe operator; each step's output feeds the next |
| `StrOutputParser` | Turns an `AIMessage` into a string |
| `RunnableParallel` | Runs parallel steps on one input and returns a dict of named outputs; `RunnableMap` is the same class |
| `bind_tools` | Attaches tools to every later invoke; optional `tool_choice` |
| `with_structured_output` | Returns a Pydantic instance (or dict) that matches the schema |
| `with_fallbacks` | On exception, run the next chain (e.g., when `json.loads` fails) |
| Runnable interface | `invoke`, `batch`, `stream`, plus `ainvoke`, `abatch`, `astream` |
| `convert_to_openai_tool` | Pydantic class, `@tool`, or function to an OpenAI tool schema; the class docstring is the description |
| `PydanticToolsParser` | Tool-call arguments validated as the Pydantic model |
| `JsonOutputToolsParser` | Tool calls as a list of dicts with `type` and `args` |
| `JsonOutputKeyToolsParser` | Arguments of the tool whose **name** is `key_name` |
| Tagging | Labels for the whole text, forced into one schema |
| Extraction | Zero or more entities; do not guess; an empty list is valid |
| `extraction_chain.map()` | Runs an extraction chain on each chunk, then flatten the lists |
| `@tool` | Function to a tool; docstring is the description the model reads |
| `args_schema` | Pydantic model of tool arguments, with `Field` descriptions |
| `tool.invoke` | Runs the tool body with a dict of arguments |
| `OpenAPISpec.from_text` | Parses an OpenAPI document; bind operations as tools and call HTTP yourself |
| `OpenAIToolsAgentOutputParser` | Model message to a list of tool actions or `AgentFinish` |
| `AgentFinish` | Final answer in `return_values["output"]`; the loop stops |
| Agent scratchpad | Tool calls and observations inside the current turn |
| `format_to_tool_messages` | `(action, observation)` pairs to an assistant tool call plus `ToolMessage`s |
| `RunnablePassthrough.assign` | Adds a key (the scratchpad) without dropping the other inputs |
| `create_tool_calling_agent` | Builds the agent runnable from the model, tools, and prompt |
| `AgentExecutor` | Runs the agent loop, dispatches tools by name, returns `output` |
| `ConversationBufferMemory` | Prior turns injected as `chat_history`; use `return_messages=True` |

---
