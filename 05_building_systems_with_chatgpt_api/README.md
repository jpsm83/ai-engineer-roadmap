# Building Systems with the ChatGPT API — Course Examples

This folder holds the coding examples for *Building Systems with the ChatGPT
API* (DeepLearning.AI / OpenAI). The scripts keep the course's helper and
prompt text, updated to the current OpenAI Python SDK
(`client.chat.completions.create` and `client.moderations.create`), one file
per lesson with a notebook. Together they build a customer-service pipeline:
classify the query, moderate it, retrieve product facts, answer, then evaluate.

- `01_language_models_chat_format_and_tokens.py` — a simple completion, the
  chat-completions roles (`system` / `user`), length and style constraints,
  and token usage from the API response.
- `02_classification.py` — routes a customer query into primary and secondary
  categories and returns JSON (`primary`, `secondary`). The active example is
  a TVs inquiry; an account-deletion query is commented out.
- `03_moderation.py` — OpenAI Moderation API, delimiter wrapping against
  prompt injection, and a few-shot `Y`/`N` detector. The active example is
  the injection classifier; the warhead / Italian-reply demos are commented.
- `04_chain_of_thought.py` — a single prompt that walks product lookup,
  assumption checking, and a reply in labeled steps, then strips the inner
  monologue and prints only the customer-facing last step.
- `05_chaining_prompts.py` — splits that work into two calls: extract
  category/product names, look them up in an in-file catalog, then answer
  from the retrieved JSON.
- `06_check_prompts.py` — moderates a sample agent reply, then asks the
  model `Y`/`N` whether the reply is grounded in product facts. The active
  example is the ungrounded "box of chocolates" reply.
- `07_evaluation_ex1.py` — end-to-end Service Assistant: moderate input,
  retrieve products via `utils.py`, answer, moderate output, then a quality
  gate. Opens a Panel chat UI on port 5006. A one-shot CLI demo is commented.
- `08_evaluation_ex2.py` — iterates the product-extraction prompt (v1 vs
  v2 few-shot), then scores a 10-example development set against ideal
  category/product lists. Makes many sequential API calls.
- `09_evaluation_ex3.py` — runs the full retrieve-and-answer pipeline, then
  LLM-as-judge: the active path compares the reply to an expert answer
  (`A`–`E`). A commented block scores the same reply with a groundedness
  rubric.
- `utils.py` — shared catalog helpers used by `07`–`09`: load
  `products.json`, extract mentioned products, look up details, answer a
  customer message. Not meant to be run on its own.
- `products.json` — the electronics catalog (name, category, features,
  price) that `utils.py` reads.

Fast-reference Q&A for the same course:
[study_docs_qa/03_prompting_and_integration/04_building_systems_with_chatgpt_api.md](../study_docs_qa/03_prompting_and_integration/04_building_systems_with_chatgpt_api.md).

For a beginner-friendly study reference about `.venv/`, `__pycache__/`, and
the `__init__` method, see
[PYTHON_REFERENCE.md](../PYTHON_REFERENCE.md) at the repository root. It applies
to every Python folder in this repository.

## Project layout

```
05_building_systems_with_chatgpt_api/
├── .venv/                        # local virtual environment (not committed)
├── __pycache__/                  # compiled bytecode, if Python created it (not committed)
├── README.md
├── requirements.txt              # pinned dependencies for this folder
├── products.json                 # catalog used by utils.py
├── utils.py                      # shared product lookup + answer helpers
├── 01_language_models_chat_format_and_tokens.py
├── 02_classification.py
├── 03_moderation.py
├── 04_chain_of_thought.py
├── 05_chaining_prompts.py
├── 06_check_prompts.py
├── 07_evaluation_ex1.py
├── 08_evaluation_ex2.py
└── 09_evaluation_ex3.py
```

Each folder that has its own Python code can have its own `.venv/`. The
repository root `.gitignore` ignores every `.venv/` and `__pycache__/`, so
neither is committed.

Credentials live in a single `.env` at the **repository root** (one level above
this folder), so every script in the repository shares it:

```
ai-engineer-roadmap/
├── .env                          # real credentials (not committed)
└── 05_building_systems_with_chatgpt_api/
    └── 01_language_models_chat_format_and_tokens.py
```

## First-time setup

This folder works with the system Python (here, 3.14). Check your version:

```bash
python3 --version
```

Then:

```bash
cd ~/code/ai-engineer-roadmap/05_building_systems_with_chatgpt_api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### What each step does

**`cd ~/code/ai-engineer-roadmap/05_building_systems_with_chatgpt_api`** moves
into the folder that contains the scripts. The environment is created here,
next to the code it is used for.

**`python3 -m venv .venv`** creates a self-contained virtual environment in
`.venv/`, so packages are installed for this project without modifying your
system Python.

**`source .venv/bin/activate`** makes `python` and `pip` point into `.venv/`.
You will usually see `(.venv)` in your prompt.

**`pip install -r requirements.txt`** installs the pinned packages into
`.venv/`:

- `openai==3.55.1` — current OpenAI Python client (`OpenAI()` plus
  `client.chat.completions.create` and `client.moderations.create`). The
  course notebooks used the pre-1.0 `openai.ChatCompletion.create` and
  `openai.Moderation.create` APIs, which this version does not have.
- `python-dotenv==1.2.4` — loads `OPENAI_API_KEY` from `.env`.
- `tiktoken==0.14.0` — OpenAI's tokenizer (imported in lessons 1–2).
- `rich==15.0.0` — pretty-prints completions and eval output.
- `panel==1.10.0` — local web UI for `07_evaluation_ex1.py`.

`requirements.txt` is the Python equivalent of `package.json` in a Node
project: it records the exact versions this folder needs, so the environment can
be recreated elsewhere.

> `os`, `json`, `sys`, `collections`, and `pathlib` are part of Python's
> standard library, so they are **not** installed with `pip`. Importing them
> always works.

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
cd ~/code/ai-engineer-roadmap/05_building_systems_with_chatgpt_api
source .venv/bin/activate

python 01_language_models_chat_format_and_tokens.py
python 02_classification.py
python 03_moderation.py
python 04_chain_of_thought.py
python 05_chaining_prompts.py
python 06_check_prompts.py
python 07_evaluation_ex1.py
python 08_evaluation_ex2.py
python 09_evaluation_ex3.py
```

By default each file runs its last uncommented example; earlier ones sit in a
triple-quoted block. Uncomment one block at a time if you want to replay a
specific prompt.

`01`–`06` print completions (or a `Y`/`N` gate) to the terminal. `01` also
prints a token-usage dict (`prompt_tokens`, `completion_tokens`,
`total_tokens`) from the last call.

`07_evaluation_ex1.py` starts a local Panel server on port 5006 and opens a
browser (Service Assistant). Chat there, then stop the server (Ctrl+C in the
terminal). In a notebook a bare `dashboard` is enough to render; from a `.py`
file the script calls `dashboard.show(port=5006)`. Do not run `utils.py`
directly; `07`–`09` import it.

`08_evaluation_ex2.py` and `09_evaluation_ex3.py` make several sequential
API calls (extraction plus a 10-example eval set, or retrieve-and-answer
plus two judge calls). They take longer and cost more than the earlier
lessons.

`utils.py` locates `products.json` from `__file__`, so `07`–`09` can run
from elsewhere inside the repo as long as that JSON file stays next to
`utils.py`.

You can tell the environment is active because `(.venv)` appears at the start of
your prompt. To check which Python is being used:

```bash
which python
```

It should print a path inside `05_building_systems_with_chatgpt_api/.venv/bin/`.

`__pycache__/` is created by Python when it compiles a local module. You do
not create it by hand. Running `python 01_language_models_chat_format_and_tokens.py`
as the main program often does not write a cache for that file; that is
normal. Importing `utils.py` from `07`–`09` does write one. If you want to
see the folder once:

```bash
python -m py_compile 01_language_models_chat_format_and_tokens.py
ls __pycache__
```

Deleting `__pycache__/` is safe. Python regenerates it when needed.

## When you are done

```bash
deactivate
```

This restores your terminal to the system Python. It does **not** delete the
environment or uninstall anything, so you can activate it again later.

## Coming back later

You do **not** need to reinstall anything:

```bash
cd ~/code/ai-engineer-roadmap/05_building_systems_with_chatgpt_api
source .venv/bin/activate
python 01_language_models_chat_format_and_tokens.py
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

The notebooks wrap long strings with `\` at the end of the line. A space after
that backslash (`\ `) is an invalid escape on Python 3.14. The `.py` files keep
the course wraps but should end those lines with `\` and no trailing space.

The notebooks used `openai.ChatCompletion.create`, `openai.Moderation.create`,
`model="gpt-3.5-turbo"`, `temperature=0`, and `max_tokens`. This folder uses
`OpenAI()`, `client.chat.completions.create`,
`client.moderations.create(model="omni-moderation-latest", ...)`,
`gpt-5-nano`, and `max_completion_tokens`. `gpt-5-nano` only allows the
default temperature (`1`), so `temperature=0` is commented out. Completions
are objects: `response.choices[0].message.content` and
`response.usage.prompt_tokens` (not dict lookups). Moderation results are
objects too: `response.results[0].flagged`.

`07_evaluation_ex1.py` imports Panel. In a notebook a bare `dashboard` is
enough to render; from the terminal the script calls
`dashboard.show(port=5006)`.

## Troubleshooting

- `ModuleNotFoundError: No module named 'openai'`: the environment is not
  activated, or the package was installed elsewhere. Activate it and run
  `pip show openai`.
- `ModuleNotFoundError: No module named 'dotenv'`: install with
  `pip install python-dotenv` inside the activated environment, or
  `pip install -r requirements.txt`.
- `ModuleNotFoundError: No module named 'tiktoken'` / `'rich'` / `'panel'`:
  install with `pip install -r requirements.txt` inside the activated
  environment.
- `APIRemovedInV1` / `openai.ChatCompletion` / `openai.Moderation`: leftover
  pre-1.0 syntax. Use `client = OpenAI(...)` with
  `client.chat.completions.create` and `client.moderations.create`.
- `SyntaxWarning: "\ " is an invalid escape sequence`: a course wrap still
  has a space after `\`. Remove that trailing space so the line ends with `\`.
- `BadRequestError: 'temperature' does not support 0 with this model`
  (or a value other than `1`): `gpt-5-nano` rejects non-default temperature.
  Leave `temperature=0` commented out, or pass `1`.
- `BadRequestError` / `AuthenticationError` / `401`: `OPENAI_API_KEY` is
  missing, empty, or wrong in the root `.env`.
- Completions never print and there is no traceback: `find_dotenv()` did not
  find the root `.env`. `cd` into this folder (or the repo) and run again.
- `FileNotFoundError` for `products.json`: `utils.py` expects that file next
  to itself. Do not move it without updating `PRODUCTS_FILE`.
- `json.JSONDecodeError` / `Error: Invalid JSON string` in `05`, `08`, or
  `utils.py`: the model wrapped the list in Markdown or extra prose. The v2
  extractor in `08_evaluation_ex2.py` asks for JSON only; retry, or inspect
  the raw completion.
- `07_evaluation_ex1.py` starts but no browser opens: look at the Panel URL
  printed in the terminal (usually `http://localhost:5006`) and open it
  yourself. If the port is taken, change the `port=` argument on
  `dashboard.show`.

## Managing dependencies

`requirements.txt` in this folder lists the packages this example needs, pinned
to exact versions. It plays the same role as `package.json` in a Node project:
it is the record of what must be installed.

To install (or reinstall) everything into an activated environment:

```bash
cd ~/code/ai-engineer-roadmap/05_building_systems_with_chatgpt_api
source .venv/bin/activate
pip install -r requirements.txt
```

If you add a package you intend to keep, add its pinned version to
`requirements.txt` by hand. Prefer a short list of **direct** imports
(`openai`, `python-dotenv`, `tiktoken`, `rich`, `panel`) over `pip freeze`,
which also dumps transitive packages.

Keep `openai==3.55.1` (or another 1.x/3.x release). Do not pin `0.28.x`; that
old client is what the course notebooks used, and it does not match this
folder's `OpenAI()` client.
