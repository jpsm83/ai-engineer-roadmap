# Building Systems with the ChatGPT API — Course Examples

This folder holds the coding examples for *Building Systems with the ChatGPT
API* (DeepLearning.AI / OpenAI). The scripts keep the course's helper and
prompt text, updated to the current OpenAI Python SDK
(`client.chat.completions.create`), one file per lesson with a notebook:

- `01_language_models_chat_format_and_tokens.py` — a simple completion, the
  chat-completions roles (`system` / `user`), length and style constraints,
  and token usage from the API response.

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
└── 01_language_models_chat_format_and_tokens.py
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
  `client.chat.completions.create`). The course notebooks used the pre-1.0
  `openai.ChatCompletion.create` API, which this version does not have.
- `python-dotenv==1.2.4` — loads `OPENAI_API_KEY` from `.env`.
- `tiktoken==0.14.0` — OpenAI's tokenizer (imported in lesson 1; used to count
  tokens locally in later lessons).

`requirements.txt` is the Python equivalent of `package.json` in a Node
project: it records the exact versions this folder needs, so the environment can
be recreated elsewhere.

> `os` is part of Python's standard library, so it is **not** installed with
> `pip`. Importing it always works.

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
```

The script prints completions to the terminal, then a token-usage dict
(`prompt_tokens`, `completion_tokens`, `total_tokens`) from the last call.

You can tell the environment is active because `(.venv)` appears at the start of
your prompt. To check which Python is being used:

```bash
which python
```

It should print a path inside `05_building_systems_with_chatgpt_api/.venv/bin/`.

`__pycache__/` is created by Python when it compiles a local module. You do
not create it by hand. Running `python 01_language_models_chat_format_and_tokens.py`
as the main program often does not write a cache for that file; that is
normal. If you want to see the folder once:

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

The notebooks used `openai.ChatCompletion.create`, `model="gpt-3.5-turbo"`,
`temperature=0`, and `max_tokens`. This folder uses `OpenAI()` and
`client.chat.completions.create`, `gpt-5-nano`, and `max_completion_tokens`.
`gpt-5-nano` only allows the default temperature (`1`), so `temperature=0` is
commented out. Completions are objects: `response.choices[0].message.content`
and `response.usage.prompt_tokens` (not dict lookups).

## Troubleshooting

- `ModuleNotFoundError: No module named 'openai'`: the environment is not
  activated, or the package was installed elsewhere. Activate it and run
  `pip show openai`.
- `ModuleNotFoundError: No module named 'dotenv'`: install with
  `pip install python-dotenv` inside the activated environment, or
  `pip install -r requirements.txt`.
- `ModuleNotFoundError: No module named 'tiktoken'`: install with
  `pip install -r requirements.txt` inside the activated environment.
- `APIRemovedInV1` / `openai.ChatCompletion`: leftover pre-1.0 syntax. Use
  `client = OpenAI(...)` and `client.chat.completions.create`.
- `SyntaxWarning: "\ " is an invalid escape sequence`: a course wrap still
  has a space after `\`. Remove that trailing space so the line ends with `\`.
- `BadRequestError: 'temperature' does not support 0 with this model`
  (or a value other than `1`): `gpt-5-nano` rejects non-default temperature.
  Leave `temperature=0` commented out, or pass `1`.
- `BadRequestError` / `AuthenticationError` / `401`: `OPENAI_API_KEY` is
  missing, empty, or wrong in the root `.env`.
- Completions never print and there is no traceback: `find_dotenv()` did not
  find the root `.env`. `cd` into this folder (or the repo) and run again.

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
(`openai`, `python-dotenv`, `tiktoken`) over `pip freeze`, which also dumps
transitive packages.

Keep `openai==3.55.1` (or another 1.x/3.x release). Do not pin `0.28.x`; that
old client is what the course notebooks used, and it does not match this
folder's `OpenAI()` client.
