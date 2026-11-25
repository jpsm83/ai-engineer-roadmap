# Functions, Tools and Agents with LangChain — Q&A

---

## Part 1 — OpenAI tool calling

### What tool calling is

**Q: What is OpenAI tool calling?**
A: You pass JSON **tool** schemas and the model may reply with a tool name plus arguments instead of free text. The model does not run your Python. Your code runs the function, then a **second** call sends that result back so the model can answer in text. The older name for this is function calling.

**Q: What does a tool schema contain?**
A: A dict with `"type": "function"` and a `"function"` object: `name`, `description`, and `parameters`. `parameters` is a JSON Schema with `type`, `properties`, and `required`. In `01_openai_function_call.py` the function is `get_current_weather`. `location` is a required string. `unit` is an enum of `celsius` and `fahrenheit`. The description steers when the model chooses that tool and how it fills each field.

**Q: How do you request a tool call?**
A: `client = OpenAI()` then `client.chat.completions.create(model="gpt-5-nano", messages=messages, tools=tools)`. The completion is an object. Read `response.choices[0].message`. Indexing `response["choices"]` raises `TypeError` because a `ChatCompletion` is not a dict.

**Q: How do you tell a tool call from a normal reply?**
A: A tool call has `content` equal to `None` and a `tool_calls` list. Each item has `.id`, `.function.name`, and `.function.arguments`. `arguments` is a JSON **string**; `json.loads` turns it into a dict you pass with `get_current_weather(**args)`. A normal reply fills `content` and leaves `tool_calls` as `None`.

**Q: What does `get_current_weather` return in this lesson?**
A: A JSON string, not a live forecast. The dict is hard-coded: location from the arguments, temperature `"72"`, the requested unit (default `fahrenheit`), and forecast `["sunny", "windy"]`.

### Call modes

**Q: What does `tool_choice` control?**
A: Whether a call is allowed. `"auto"` (the default) lets the model decide. `"none"` forbids every call, so the model answers in text and may invent the weather. `{"type": "function", "function": {"name": "get_current_weather"}}` forces that tool even on a greeting, so the arguments may not match the user's intent. The active example forces it for "What's the weather like in Barcelona!".

### Sending the result back

**Q: Why are there two model calls?**
A: The first call only builds the request: a tool name and JSON arguments, with no weather data in the reply. Your code runs `get_current_weather`. The second call sees that result in the conversation and writes the sentence the user reads. One call cannot both request the tool and know its return value.

**Q: How do you finish the round trip after a tool call?**
A: (1) Append the assistant message: `messages.append(response.choices[0].message)`. (2) Read `tool_call = response.choices[0].message.tool_calls[0]`, parse `tool_call.function.arguments`, and run the function. (3) Append `{"role": "tool", "tool_call_id": tool_call.id, "content": observation}`. This role sits beside `user` and `assistant`, and `tool_call_id` must match the call it answers. (4) Call the model again so it answers from that observation. The second completion omits `tools`. The script prints that second completion.

---

## Part 2 — LangChain Expression Language

### The pipe

**Q: What is LangChain Expression Language (LCEL)?**
A: A way to compose **Runnables** with `|`. Each step's output is the next step's input. `chain = prompt | model | output_parser` is a chain you call with `chain.invoke({...})`.

**Q: What are the three pieces of a minimal chain?**
A: `ChatPromptTemplate.from_template` holds a string with `{variables}` (`"tell me a short joke about {topic}"`). `ChatOpenAI(model="gpt-5-nano", temperature=1)` is the chat model. `StrOutputParser` turns the `AIMessage` into a plain string so later steps do not have to read `.content`.

### RunnableParallel

**Q: What does `RunnableParallel` do?**
A: It runs several steps on the **same** input and returns a dict of named outputs. `RunnableMap` is the same class. Use it when the next prompt needs derived fields, such as retrieved context plus the original question.

**Q: How do you ground a chain on retrieved text?**
A: `InMemoryVectorStore.from_texts` stores two sentences ("harrison worked at kensho", "bears like to eat honey") with `OpenAIEmbeddings(model="text-embedding-3-small")`. `vectorstore.as_retriever()` searches them. The parallel step is `itemgetter("question") | retriever | format_docs` for `context`, and `itemgetter("question")` copied through as `question`. `format_docs` joins each document's `page_content`. The prompt says to answer only from `{context}`. A commented lambda calls `retriever.get_relevant_documents`; the live chain uses the retriever as a runnable in the pipe.

### Bind

**Q: What does `bind_tools` do?**
A: `model.bind_tools(functions)` returns a new runnable that sends those function schemas on every call, so you pipe `prompt | model`. The schemas in this file are plain dicts (`name`, `description`, `parameters`): first `weather_search` (airport code), then the same model bound again with `weather_search` and `sports_search` (team name). Calling `bind_tools` again replaces the previous list. The model picks the tool whose description matches the question and fills that tool's arguments.

### Fallbacks

**Q: What does `with_fallbacks` do?**
A: `simple_chain.with_fallbacks([chain])` runs `simple_chain` first and, if it raises, runs `chain`. `simple_chain` is `gpt-4o-mini` (`temperature=0`, `max_tokens=1000`) piped through `StrOutputParser()` and `json.loads`. The fallback is the tool-bound `gpt-5-nano` model through the same parser and `json.loads`. The prompt asks for three poems as a JSON blob. A bad blob raises `JSONDecodeError` and the fallback runs. Those invokes are commented out.

### Runnable interface

**Q: Which methods does every LCEL chain support?**
A: `invoke` for one input, `batch` for a list of inputs, and `stream` to yield chunks as they arrive. The async forms are `ainvoke`, `abatch`, and `astream`. The active example reuses the tool-bound model with a joke prompt and calls `invoke` (bears), `batch` (bears and frogs), `stream` (bears), and `ainvoke` (bears). `invoke` and `batch` discard their return values. `stream` prints each token. `ainvoke` is run with `asyncio.run`, and the script prints that joke.

---

## Part 3 — Tool calling in LangChain

### Pydantic models

**Q: Why define tool inputs as Pydantic models?**
A: A `BaseModel` validates types, so `pUser(age="bar")` raises `ValidationError`. The plain `User` class accepts that string and stores it. Nest models with fields such as `students: list[pUser]` on `Class`.

### Schema conversion

**Q: How do you turn a Pydantic model into an OpenAI function?**
A: `convert_to_openai_function(WeatherSearch)` returns `{name, description, parameters}`. The class name is the function name. The class docstring is the description. `WeatherSearch1` has no docstring, so the description is an empty string. `Field(description=...)` becomes that parameter's description. `WeatherSearch2` has a docstring but a bare `airport_code: str`, so the parameter has no description of its own.

**Q: How do you attach that function to a chat model?**
A: `model.bind_tools([weather_function])` sends it on every call. `model` is `ChatOpenAI(model="gpt-5-nano")`. Pipe it as `prompt | model_with_function`. `invoke` returns an `AIMessage`. On a tool call, `response.tool_calls` is a list of dicts with `name`, `args` (already a dict), and `id`. That is the LangChain message. The raw client in `01` still gives you `.function.arguments` as a JSON string.

### Forcing and choosing

**Q: How do you force a Pydantic tool?**
A: `model.bind_tools([weather_function], tool_choice="WeatherSearch")`. The name must match the class. The model then calls that tool even when the user only says hello. The same force is `tool_choice={"type": "function", "function": {"name": "WeatherSearch"}}`.

**Q: How does the model choose among several tools?**
A: Convert `WeatherSearch` and `ArtistSearch`, bind that list, and leave `tool_choice` unset so it stays `"auto"`. `ArtistSearch` takes `artist_name` and `n`. The script prints three invokes: San Francisco weather, three songs by Taylor Swift, and "hi!". The first two should carry `tool_calls`. "hi!" can answer in `content` with no tool call.

---

## Part 4 — Tagging and extraction

### Tagging

**Q: What is tagging?**
A: Assigning labels to a piece of text as structured fields. `Tagging` has `sentiment: Literal["pos", "neg", "neutral"]` and `language: str`. The allowed sentiments are the `Literal` values. The `Field` descriptions are "sentiment of the text" and "language of the text (ISO 639-1 code)".

**Q: How do you make tagging always return the schema?**
A: `convert_to_openai_function(Tagging)`, then `model.bind_tools([tagging_function], tool_choice={"type": "function", "function": {"name": "Tagging"}})`. The system message is "Think carefully, and then tag the text as instructed". `prompt | model_with_function | JsonOutputKeyToolsParser(key_name="Tagging", first_tool_only=True)` returns the arguments dict (`sentiment` and `language`). `gpt-5-nano` is the model. This file does not set `temperature`.

### Extraction

**Q: How does extraction differ from tagging?**
A: Tagging labels the whole text. **Extraction** pulls out zero or more entities. `Person` has `name: str` and `age: int | None`. `Information` wraps them in `people: list[Person]`.

**Q: How do you stop the model from guessing missing fields?**
A: Say so in the system prompt. The people prompt says to extract only what is explicit, allow partial records, and not guess. The paper prompt says an empty list is fine, not to extract the article's own title, and not to invent authors. A vague prompt makes the model invent titles, names, or counts that are not in the text.

**Q: How do you unwrap one field from the result?**
A: `JsonOutputKeyToolsParser(key_name="Information", first_tool_only=True)` returns the arguments of the tool **named** `Information` (the whole `{people: [...]}` dict). It does not return one key inside those arguments. The chain then pipes `itemgetter("people")`. The paper chain uses `key_name="Info"` and `itemgetter("papers")`. `Paper` is `title` plus optional `author`.

### Long documents

**Q: How do you extract over a long document in one chain?**
A: One call only sees the text you send, so a prefix drops later mentions. The script downloads Lilian Weng's agent post with `urllib.request`, parses the HTML with BeautifulSoup, and stores it as a `Document`. `RecursiveCharacterTextSplitter(chunk_overlap=0)` splits `page_content`. A `RunnableLambda` maps the string to `[{"input": chunk}, ...]`. Then `prep | extraction_chain.map() | flatten`. `flatten` is a plain function; a function at the end of a pipe is treated as a runnable. `.map()` runs the extraction chain once per chunk. The active call is `chain.invoke(doc.page_content)`, which prints one flat list of papers. `Overview` tagging (summary, language, keywords) is built the same way and its invoke is commented out.

---

## Part 5 — Tools and routing

### Defining a tool

**Q: What does `@tool` do?**
A: It turns a Python function into a LangChain **tool**. `name` comes from the function name, `description` from the docstring, and `args` from the signature. The model only sees that name and description, so a vague docstring makes it skip the tool or call it at the wrong time. The file defines `search` twice. The second decorator replaces the first. Both return the string `"42f"`.

**Q: When do you pass `args_schema`?**
A: When each argument needs a description the signature does not carry. `@tool(args_schema=SearchInput)` uses a Pydantic model with `Field` descriptions. The weather tool uses `OpenMeteoInput`: required `latitude` and `longitude` floats. `get_current_temperature` calls the Open-Meteo forecast API (`hourly=temperature_2m`, one day), picks the hour closest to now in UTC, and returns `The current temperature is {n}°C`. Call it with `tool.invoke({"latitude": 13, "longitude": 14})`.

**Q: How do you give tools to the model?**
A: `convert_to_openai_function` on each `@tool`, then `ChatOpenAI(model="gpt-5-nano", temperature=1).bind_tools(functions)`. The body (the HTTP call, the Wikipedia client) runs only when your code calls `tool.invoke`. `search_wikipedia` searches, takes the first three pages, and joins their summaries. If nothing comes back it returns "No good Wikipedia Search Result was found".

### OpenAPI

**Q: How does this lesson turn an OpenAPI document into tools?**
A: The Petstore spec is an inline OpenAPI 3 JSON string. `parse_obj` from `openapi-pydantic` loads it. The script walks every path and HTTP method, and for each operation builds `{name, description, parameters}`. `name` is `operationId` (`listPets`, `createPets`, `showPetById`). `description` is the operation description or summary. Parameters are grouped by where they sit: query parameters under `params`, headers under `headers`, cookies under `cookies`, path parameters under `path_params`. `bind_tools(pet_openai_functions)` attaches that list. The invokes that would ask for pet names or pet 42 are commented out. This file does not perform those HTTP calls.

### Routing

**Q: What is routing with tool calling?**
A: Binding several tools and letting the model pick from their descriptions. The route chain binds `search_wikipedia` and `get_current_temperature` only. A weather question calls Open-Meteo. "What is langchain?" calls Wikipedia. "hi!" should finish with text. The router runs the first tool action and stops.

**Q: What does `OpenAIToolsAgentOutputParser` return?**
A: If the model called tools, a list of actions. The scripts read `.tool` (the name), `.tool_input` (the argument dict), and `.message_log` (the assistant message that requested the tool). If it answered in text, an `AgentFinish` whose `.return_values["output"]` is that text.

**Q: How do you run the chosen tool in the chain?**
A: `prompt | model | OpenAIToolsAgentOutputParser() | route`. The prompt is a system line ("helpful but sassy assistant") plus the user `{input}`. `route` checks `isinstance(result, AgentFinish)` and returns `return_values["output"]`. Otherwise it looks up `result[0].tool` in a dict of the two tools and calls `.invoke(result[0].tool_input)`. On a LangChain `AIMessage` you can also read `tool_calls` directly (`name`, `args`, `id`) and skip the parser. The active path uses the parser and prints the three route results.

---

## Part 6 — Conversational agent

### The agent loop

**Q: How is an agent different from a router?**
A: A **router** calls at most one tool and stops. An **agent** lets the model see each observation and then either call another tool or finish with a natural-language answer. It repeats until the parser returns `AgentFinish`. That loop is the same two-call round trip, repeated. The tools are `get_current_temperature` and `search_wikipedia`, the same pair as the router.

**Q: What is the agent scratchpad?**
A: Tool calls and observations from the **current** user turn. The prompt puts `MessagesPlaceholder(variable_name="agent_scratchpad")` after the user message. `chat_history` is a different placeholder, placed before the user message: it holds prior turns. The first chain in the file has no scratchpad slot. The later chains do.

**Q: What does one pass of the agent loop look like?**
A: Keep `intermediate_steps` as `(action, observation)` pairs. Pass `format_to_openai_tool_messages(intermediate_steps)` in as the scratchpad (empty on the first pass). That helper rebuilds the assistant tool-call message from `message_log` plus a `ToolMessage` (`tool_call_id` taken from the action). If the result is `AgentFinish`, return it. Otherwise take `result[0]`, run `tool.run(action.tool_input)`, append `(action, observation)`, and invoke again. The name-to-tool dict is `search_wikipedia` and `get_current_temperature`.

**Q: How do you build the scratchpad inside the chain?**
A: `RunnablePassthrough.assign(agent_scratchpad=lambda x: format_to_openai_tool_messages(x["intermediate_steps"]))` adds that key and keeps `input` and `intermediate_steps`. The pipe is that assign step, then `prompt | model | OpenAIToolsAgentOutputParser()`. The caller passes `intermediate_steps`. The assign step formats them.

### Executor and memory

**Q: What does `AgentExecutor` replace?**
A: The handwritten `while` loop and the manual name-to-tool dict. The agent you pass in is the LCEL chain above (`assign` + prompt + bound model + `OpenAIToolsAgentOutputParser`). `AgentExecutor(agent=agent_chain, tools=tools, verbose=True)` looks up each action by name in `tools`, runs it, stops on `AgentFinish`, and returns a dict whose answer is `output`. `verbose=True` prints each step.

**Q: Why does the agent forget facts from the previous invoke?**
A: Each `invoke` sends only that call's input unless you attach memory. Add `MessagesPlaceholder(variable_name="chat_history")` before the user message. `06_conversational_agent.py` defines its own `ConversationBufferMemory(BaseMemory)`: a list of `HumanMessage` and `AIMessage`, `return_messages=True`, `memory_key="chat_history"`. `return_messages=True` is required because the placeholder expects a list of messages, and `memory_key` must match the placeholder name. Pass `memory=memory` to `AgentExecutor`. It loads `chat_history` before each call and appends the new user message and answer afterward. Without that, "my name is bob" followed by "whats my name" has nothing to recall.

**Q: How do you add your own tool?**
A: Decorate a function with `@tool`, write a docstring that says when to use it, and append it to `tools`. `create_your_own` says it can do whatever you fill in, and the body returns `query[::-1]`. The UI list is `get_current_temperature`, `search_wikipedia`, and `create_your_own`. Inside the Panel class those tools are converted with `convert_to_openai_function` and passed to `bind_tools`. `AgentExecutor` runs whatever the model selects.

**Q: How does the chat window run the agent?**
A: `cbfs` holds the panels, a fresh memory, the prompt (history, user input, scratchpad), and an `AgentExecutor` with `verbose=False`. `convchain` clears the text box, calls `qa.invoke({"input": query})`, and appends the user line plus `result["output"]` as Markdown rows. `pn.extension()` loads Panel. `dashboard.show()` starts a local server and opens `QnA_Bot` in a browser. Leave that process running while you chat.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Tool calling | Model returns a tool name and JSON arguments; your code runs the function, then a second call answers from the result |
| Tool schema | `{"type": "function", "function": {name, description, parameters}}`; `parameters` is JSON Schema |
| `tool_choice` | `"auto"` (model decides), `"none"` (never call), a tool name such as `"WeatherSearch"`, or `{"type": "function", "function": {"name": ...}}` |
| `tool_calls` (raw client) | List on the assistant message; `.function.arguments` is a JSON string, `.id` links the result. `None` when the model just answers |
| `tool_calls` (LangChain) | On an `AIMessage`, a list of dicts with `name`, `args` (already parsed), and `id` |
| Tool message | `{"role": "tool", "tool_call_id", "content"}` carrying the function result back to the model |
| Two calls | First call requests the tool; your code runs it; second call writes the answer |
| LCEL | Compose Runnables with the pipe operator; each step's output feeds the next |
| `StrOutputParser` | Turns an `AIMessage` into a string |
| `RunnableParallel` | Runs parallel steps on one input and returns a dict of named outputs; `RunnableMap` is the same class |
| `itemgetter` | Pulls one key in a pipe (`"question"`, `"people"`, `"papers"`) |
| `bind_tools` | Attaches function schemas to every later invoke; calling it again replaces the list. Optional `tool_choice` |
| `with_fallbacks` | On exception, run the next chain. Here `gpt-4o-mini` then `json.loads` falls back to `gpt-5-nano` with the same parser |
| Runnable interface | `invoke`, `batch`, `stream`, plus `ainvoke`, `abatch`, `astream`. The script runs the first four |
| `convert_to_openai_function` | Pydantic class or `@tool` to `{name, description, parameters}`. The class docstring is the description. `bind_tools` accepts that dict |
| `JsonOutputToolsParser` | Tool calls as a list of dicts with `type` and `args` |
| `JsonOutputKeyToolsParser` | Arguments of the tool whose **name** is `key_name`. `first_tool_only=True` returns one args dict |
| Tagging | Labels for the whole text (`Literal` sentiment and a language code), forced with `tool_choice` |
| Extraction | Zero or more entities (`people` or `papers`); do not guess; an empty list is valid |
| `extraction_chain.map()` | Runs the extraction chain on each chunk; `flatten` concatenates the lists |
| `@tool` | Function to a tool; docstring is the description the model reads |
| `args_schema` | Pydantic model of tool arguments, with `Field` descriptions (`SearchInput`, `OpenMeteoInput`) |
| `tool.invoke` / `tool.run` | Runs the tool body with a dict of arguments. The router uses `invoke`; the handwritten agent loop uses `run` |
| `parse_obj` | `openapi-pydantic` loader for the inline Petstore spec. Each `operationId` becomes a function dict |
| `OpenAIToolsAgentOutputParser` | Model message to a list of tool actions (`.tool`, `.tool_input`, `.message_log`) or `AgentFinish` |
| `AgentFinish` | Final answer in `return_values["output"]`; the loop stops |
| Agent scratchpad | Tool calls and observations inside the current turn (`MessagesPlaceholder`) |
| `format_to_openai_tool_messages` | `(action, observation)` pairs to an assistant tool call plus `ToolMessage`s |
| `RunnablePassthrough.assign` | Adds the scratchpad key without dropping `input` and `intermediate_steps` |
| Agent chain | `assign` \| prompt \| bound model \| `OpenAIToolsAgentOutputParser` |
| `AgentExecutor` | Runs that chain, dispatches tools by name, returns `output` |
| `ConversationBufferMemory` | Local `BaseMemory` in `06`: prior turns injected as `chat_history`; `return_messages=True` |
| `dashboard.show()` | Starts the Panel `QnA_Bot` UI on the same agent, memory, and tools |

---
