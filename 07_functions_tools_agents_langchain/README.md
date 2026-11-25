# Functions, Tools and Agents with LangChain — Course Examples

This folder holds the coding examples for *Functions, Tools and Agents with
LangChain* (DeepLearning.AI / LangChain). The scripts keep the course's
lesson flow, updated to the current OpenAI and LangChain packages
(`openai`, `langchain`, `langchain-openai`, `langchain-classic`,
`langchain-text-splitters`), one file per lesson. Together they go from a
raw tool call, through LCEL and structured extraction, to a tool-routing
chain and a conversational agent with a small chat UI.

- `01_openai_function_call.py` — OpenAI tool calling with the raw client.
  Defines a dummy `get_current_weather` (always 72°F, sunny and windy) and
  its JSON schema. The active example forces that tool for "What's the
  weather like in Barcelona!", runs the function, sends the observation
  back as a `tool` message, and prints the second completion. `tool_choice`
  variants (`auto`, `none`, forced) sit in a triple-quoted block.
- `02_langchain_expression_LCEL.py` — LangChain Expression Language. Builds
  a joke chain (`prompt | model | StrOutputParser`), a retrieval chain over
  two in-memory sentences, `bind_tools` for weather and sports search, and
  a `with_fallbacks` JSON chain. The active example is the runnable
  interface: `invoke`, `batch`, `stream`, and `ainvoke` on jokes about
  bears and frogs. Only the stream and the async result are printed.
- `03_openai_function_calling_in_langchain.py` — Pydantic models as tool
  schemas. A plain class accepts a bad `age`; `BaseModel` raises
  `ValidationError`. `convert_to_openai_function` turns `WeatherSearch` and
  `ArtistSearch` into tools. The active example binds both and prints the
  model's tool calls for San Francisco weather, three Taylor Swift songs,
  and "hi!".
- `04_tagging_and_extraction.py` — forced tool calls for tagging and
  extraction, parsed with `JsonOutputKeyToolsParser`. The active example
  downloads Lilian Weng's agent post, splits it with
  `RecursiveCharacterTextSplitter`, and prints papers extracted from every
  chunk. Sentiment tagging and the single-paragraph people demo are
  commented out.
- `05_tools_and_routing.py` — `@tool` functions: a dummy search, live
  Open-Meteo temperature, and Wikipedia summaries. An inline OpenAPI
  Petstore spec is parsed into function schemas. The active example routes
  three questions: San Francisco weather (Open-Meteo), "What is langchain?"
  (Wikipedia), and "hi!" (a direct answer).
- `06_conversational_agent.py` — the same weather and Wikipedia tools, then
  a manual agent loop, `AgentExecutor`, a local `ConversationBufferMemory`,
  and a third tool that reverses its input. The active example opens a
  Panel chat UI (`QnA_Bot`) that keeps history and can call those tools.

Fast-reference Q&A for the same course:
[study_docs_qa/03_prompting_and_integration/06_functions_tools_agents_langchain.md](../study_docs_qa/03_prompting_and_integration/06_functions_tools_agents_langchain.md).

For a beginner-friendly study reference about `.venv/`, `__pycache__/`, and
the `__init__` method, see
[PYTHON_REFERENCE.md](../PYTHON_REFERENCE.md) at the repository root. It applies
to every Python folder in this repository.

## Project layout

```
07_functions_tools_agents_langchain/
├── .venv/                                      # local virtual environment (gitignored)
├── __pycache__/                                # compiled bytecode, if Python created it (gitignored)
├── README.md
├── requirements.txt                            # pinned dependencies for this folder
├── 01_openai_function_call.py
├── 02_langchain_expression_LCEL.py
├── 03_openai_function_calling_in_langchain.py
├── 04_tagging_and_extraction.py
├── 05_tools_and_routing.py
└── 06_conversational_agent.py
```

Each folder that has its own Python code can have its own `.venv/`. The
repository root `.gitignore` ignores every `.venv/` and `__pycache__/`, so
neither is committed.

Credentials live in a single `.env` at the **repository root** (one level above
this folder), so every script in the repository shares it:

```
ai-engineer-roadmap/
├── .env                                    # real credentials (gitignored)
└── 07_functions_tools_agents_langchain/
    └── 01_openai_function_call.py
```

## First-time setup

This folder works with the system Python (here, 3.14). Check your version:

```bash
python3 --version
```

Then:

```bash
cd ~/code/ai-engineer-roadmap/07_functions_tools_agents_langchain
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### What each step does

**`cd ~/code/ai-engineer-roadmap/07_functions_tools_agents_langchain`** moves
into the folder that contains the scripts. The environment is created here,
next to the code it is used for.

**`python3 -m venv .venv`** creates a self-contained virtual environment in
`.venv/`, so packages are installed for this project without modifying your
system Python.

**`source .venv/bin/activate`** makes `python` and `pip` point into `.venv/`.
You will usually see `(.venv)` in your prompt.

**`pip install -r requirements.txt`** installs the pinned packages into
`.venv/`:

- `openai==3.57.0` — OpenAI Python client. `01` uses `OpenAI()` and
  `client.chat.completions.create`. `05` and `06` set `openai.api_key` from
  the environment; the chat calls themselves go through `ChatOpenAI`.
- `python-dotenv==1.2.4` — loads `OPENAI_API_KEY` from `.env`.
- `rich==15.0.0` — `rich.print` for completions, tool calls, and extracted
  records.
- `langchain==1.5.2` — `@tool` in `05_tools_and_routing.py` and
  `06_conversational_agent.py`.
- `langchain-classic==1.1.0` — `OpenAIToolsAgentOutputParser`,
  `AgentExecutor`, `format_to_openai_tool_messages`, and the memory base
  class used by the agent scripts.
- `langchain-openai==1.8.5` — `ChatOpenAI`, `OpenAIEmbeddings`, and
  `JsonOutputKeyToolsParser`.
- `langchain-text-splitters==1.2.0` — `RecursiveCharacterTextSplitter` in
  `04_tagging_and_extraction.py`.
- `openapi-pydantic==0.6.0` — parses the inline Petstore OpenAPI document
  in `05_tools_and_routing.py`.
- `wikipedia==1.4.0` — page search and summaries for the Wikipedia tool in
  `05` and `06`.
- `beautifulsoup4==4.15.0` — turns the downloaded blog HTML into text in
  `04_tagging_and_extraction.py`.
- `numpy==2.5.5` — pinned with this environment. The lesson scripts do not
  import it.
- `panel==1.11.1` — the `QnA_Bot` chat UI in `06_conversational_agent.py`.

`pydantic`, `requests`, and `param` are imported by the scripts and come in
with `langchain`, `wikipedia` / `panel`, and `panel`. They are not pinned on
their own lines in `requirements.txt`.

`requirements.txt` is the Python equivalent of `package.json` in a Node
project: it records the exact versions this folder needs, so the environment can
be recreated elsewhere.

> `os`, `json`, `asyncio`, `operator`, `typing`, `urllib.request`, and
> `datetime` are part of Python's standard library, so they are **not**
> installed with `pip`. Importing them always works.

## Credentials: keep them secret

The scripts read one environment variable:

- `OPENAI_API_KEY`

This is a **critical secret**. It can be used to call OpenAI and bill your
account, so it must never be committed, pasted into chat, or shared.

It lives in a single `.env` file at the **repository root**. Create or edit it:

```bash
cd ~/code/ai-engineer-roadmap
nano .env
```

Add this line (alongside any other keys this repo already uses):

```dotenv
OPENAI_API_KEY=your-secret-key
```

Rules for this file:

- `.env` is listed in the repository-root `.gitignore`, so Git ignores it.
- There is no committed template: never put real keys in a tracked file.
- If you ever commit a key by accident, rotate it immediately in OpenAI.
- The scripts load `.env` with `load_dotenv(find_dotenv())`, which walks up
  from the current working directory. Run them from this folder or
  elsewhere inside the repository so they can find the root `.env`.

## Running the scripts

Every time you open a **new terminal**, activate the environment first:

```bash
cd ~/code/ai-engineer-roadmap/07_functions_tools_agents_langchain
source .venv/bin/activate

python 01_openai_function_call.py
python 02_langchain_expression_LCEL.py
python 03_openai_function_calling_in_langchain.py
python 04_tagging_and_extraction.py
python 05_tools_and_routing.py
python 06_conversational_agent.py
```

By default each file runs its last uncommented example; earlier ones sit in a
triple-quoted block or behind `#`. Uncomment one block at a time if you want
to replay a specific prompt.

`01_openai_function_call.py` makes two chat calls. The first is forced to
`get_current_weather`. The script appends that assistant message, runs the
dummy function, appends a `role: "tool"` message, and prints the second
completion (the sentence about Barcelona). The weather data is hard-coded,
so this file does not call a weather API.

`02_langchain_expression_LCEL.py` embeds two short sentences
(`text-embedding-3-small`) while it builds `InMemoryVectorStore`, even
though the retrieval prints are commented out. The active joke chain then
calls the chat model four ways. `invoke` and `batch` run and discard their
return values; `stream` prints tokens as they arrive; `ainvoke` prints the
full joke. From the terminal, `chain.invoke(...)` on its own shows nothing.

`03_openai_function_calling_in_langchain.py` validates one bad Pydantic
object locally (the error is caught and not printed), then makes three chat
calls and prints each `AIMessage`, including `tool_calls`. "hi!" may answer
in text with no tool call.

`04_tagging_and_extraction.py` downloads
`https://lilianweng.github.io/posts/2023-06-23-agent/` and needs a network.
It then calls the model once per chunk and prints one flat list of papers.
That is many sequential API calls, so it costs more and takes longer than
`01`–`03`. `len(splits)` and `flatten([[1, 2], [3, 4]])` only show a value
in a notebook or REPL.

`05_tools_and_routing.py` parses the Petstore spec locally, then routes
three questions. The weather question calls the Open-Meteo forecast API.
The LangChain question calls Wikipedia. "hi!" should come back as text.
Each `print(result)` is the tool's return value or the model's final
sentence, depending on the route.

`06_conversational_agent.py` still executes the commented-out lesson steps
that are real calls: two model calls about San Francisco weather and one
Open-Meteo request, before `dashboard.show()` starts a local Panel server
and opens `QnA_Bot` in a browser. Leave that process running while you
chat. Weather and "what is langchain?" use the tools; the reverse tool
answers by flipping the string you passed. Ctrl+C stops the server.

You can tell the environment is active because `(.venv)` appears at the start of
your prompt. To check which Python is being used:

```bash
which python
```

It should print a path inside `07_functions_tools_agents_langchain/.venv/bin/`.

`__pycache__/` is created by Python when it compiles a local module. You do
not create it by hand. Running these files as the main program often does
not write a cache for that file; that is normal. Deleting `__pycache__/` is
safe. Python regenerates it when needed.

## When you are done

```bash
deactivate
```

This restores your terminal to the system Python. It does **not** delete the
environment or uninstall anything, so you can activate it again later.

## Coming back later

You do **not** need to reinstall anything:

```bash
cd ~/code/ai-engineer-roadmap/07_functions_tools_agents_langchain
source .venv/bin/activate
python 01_openai_function_call.py
deactivate
```

## Virtual environment rules

- A virtual environment contains **absolute paths**. It cannot be moved or
  renamed. If it is in the wrong folder, delete it and create it again.
- Only one environment can be active in a terminal at a time. Run `deactivate`
  before activating a different one.
- Activation is per terminal. A new terminal starts with the system Python, so
  activate the environment again.

## Course notes that differ from the original notebooks

The notebooks used `functions=` on `chat.completions.create`,
`langchain.chat_models.ChatOpenAI`, `model="gpt-3.5-turbo"`, and
`temperature=0`. This folder passes `tools=` (`01`) and `bind_tools` (`02`
onward), imports `ChatOpenAI` from `langchain_openai`, and sets `llm_model`
to `gpt-5-nano`. Where a temperature is set it is `temperature=1`, the only
value `gpt-5-nano` accepts. The fallback model in `02` is `gpt-4o-mini` with
`temperature=0`; those calls are commented out.

Retrieval in `02` uses `InMemoryVectorStore` and
`OpenAIEmbeddings(model="text-embedding-3-small")`.

`04` fetches the blog with `urllib.request` and parses it with
BeautifulSoup, then splits with `RecursiveCharacterTextSplitter`. Tagging
and extraction read tool arguments through `JsonOutputKeyToolsParser`.

`05` and `06` build tools with `@tool` and route with
`OpenAIToolsAgentOutputParser` from `langchain_classic`. `06` keeps a local
`ConversationBufferMemory` (message list plus `BaseMemory`) instead of the
deprecated `langchain.memory` class, and `AgentExecutor` runs the tool loop.
The chat window is Panel (`dashboard.show()`).

## Troubleshooting

- `ModuleNotFoundError: No module named 'langchain'` / `'langchain_openai'` /
  `'langchain_classic'` / `'langchain_text_splitters'`: the environment is
  not activated, or the packages were installed elsewhere. Activate it and
  run `pip install -r requirements.txt`.
- `ModuleNotFoundError: No module named 'dotenv'`: install with
  `pip install python-dotenv` inside the activated environment, or
  `pip install -r requirements.txt`.
- `ModuleNotFoundError: No module named 'openai'` / `'rich'` /
  `'wikipedia'` / `'bs4'` / `'openapi_pydantic'` / `'panel'`: install with
  `pip install -r requirements.txt` inside the activated environment.
- `BadRequestError: 'temperature' does not support 0 with this model`
  (or a value other than `1`): `gpt-5-nano` rejects non-default temperature.
  Leave those calls at `temperature=1`.
- `BadRequestError` / `AuthenticationError` / `401`: `OPENAI_API_KEY` is
  missing, empty, or wrong in the root `.env`. `05` and `06` read it with
  `os.environ['OPENAI_API_KEY']`, which raises `KeyError` when the variable
  was never set.
- Completions never print and there is no traceback: `find_dotenv()` did not
  find the root `.env`. `cd` into this folder (or the repo) and run again.
- `04_tagging_and_extraction.py` fails in `urlopen`: the blog host is
  unreachable, or the request timed out (30 seconds). Retry when you have
  a network connection.
- `05` or `06` fails inside `get_current_temperature`: Open-Meteo did not
  return HTTP 200, or the model picked coordinates the API rejected. The
  tool raises `Exception` with the status code.
- Wikipedia tool raises `NameError` on `self`: the `except` clause in
  `search_wikipedia` refers to `self.wiki_client`, which this script does
  not define. A missing or disambiguated page hits that branch. A normal
  hit still returns the summaries.
- `06_conversational_agent.py` exits before a browser opens: Panel could
  not bind a port, or the process was interrupted. Run it from this folder
  with the environment activated and leave the terminal open.

## Managing dependencies

`requirements.txt` in this folder lists the packages this example needs, pinned
to exact versions. It plays the same role as `package.json` in a Node project:
it is the record of what must be installed.

To install (or reinstall) everything into an activated environment:

```bash
cd ~/code/ai-engineer-roadmap/07_functions_tools_agents_langchain
source .venv/bin/activate
pip install -r requirements.txt
```

If you add a package you intend to keep, add its pinned version to
`requirements.txt` by hand. Prefer a short list of **direct** imports
(`openai`, `python-dotenv`, `rich`, `langchain`, `langchain-classic`,
`langchain-openai`, `langchain-text-splitters`, `openapi-pydantic`,
`wikipedia`, `beautifulsoup4`, `panel`) over `pip freeze`, which also dumps
transitive packages.
