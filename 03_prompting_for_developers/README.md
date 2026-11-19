# Prompting for Developers Course Examples

This folder holds the coding examples for *ChatGPT Prompt Engineering for
Developers* (DeepLearning.AI / OpenAI). The scripts keep the course's helper
and prompt text, updated to the current OpenAI Python SDK
(`client.chat.completions.create`), one `.py` file per course notebook:

- `01_guidelines.py` — clear instructions (delimiters, structured output,
  conditionals, few-shot), giving the model time to think, and a
  hallucination prompt.
- `02_iterative.py` — iterative prompt development: marketing copy from a
  product fact sheet, then length, audience, IDs, and an HTML dimensions table.
- `03_summarizing.py` — summaries with a word limit, a topic focus, extract
  instead of summarize, and a loop over several reviews.
- `04_inferring.py` — sentiment, anger, emotions, entity extraction,
  multi-field JSON, topic lists, and a zero-shot topic alert.
- `05_transforming.py` — translation, tone, JSON-to-HTML conversion, and
  proofreading (including a `redlines` diff and an APA-style rewrite).
- `06_expanding.py` — a sentiment-conditioned customer email. The course used
  `temperature` to vary how creative the reply is; that argument is commented
  out here because `gpt-5-nano` only allows the default (`1`).
- `07_chatbot.py` — chat-completions roles (`system` / `user` / `assistant`),
  conversation context, and a Panel OrderBot UI that can emit a JSON order
  summary.

Fast-reference Q&A for the same course:
[study_docs_qa/03_prompting_and_integration/02_chatgpt_prompt_engineering_for_developers.md](../study_docs_qa/03_prompting_and_integration/02_chatgpt_prompt_engineering_for_developers.md).

For a beginner-friendly study reference about `.venv/`, `__pycache__/`, and
the `__init__` method, see
[PYTHON_REFERENCE.md](../PYTHON_REFERENCE.md) at the repository root. It applies
to every Python folder in this repository.

## Project layout

```
03_prompting_for_developers/
├── .venv/                        # local virtual environment (not committed)
├── __pycache__/                  # compiled bytecode, if Python created it (not committed)
├── README.md
├── requirements.txt              # pinned dependencies for this folder
├── 01_guidelines.py
├── 02_iterative.py
├── 03_summarizing.py
├── 04_inferring.py
├── 05_transforming.py
├── 06_expanding.py
└── 07_chatbot.py
```

Each folder that has its own Python code can have its own `.venv/`. The
repository root `.gitignore` ignores every `.venv/` and `__pycache__/`, so
neither is committed.

Credentials live in a single `.env` at the **repository root** (one level above
this folder), so every script in the repository shares it:

```
ai-engineer-roadmap/
├── .env                          # real credentials (not committed)
└── 03_prompting_for_developers/
    └── 01_guidelines.py
```

## First-time setup

This folder works with the system Python (here, 3.14). Check your version:

```bash
python3 --version
```

Then:

```bash
cd ~/code/ai-engineer-roadmap/03_prompting_for_developers
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### What each step does

**`cd ~/code/ai-engineer-roadmap/03_prompting_for_developers`** moves into the
folder that contains the scripts. The environment is created here, next to the
code it is used for.

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
- `ipython==9.18.1` — `IPython.display` used by the iterative and transforming
  scripts to render HTML or Markdown.
- `redlines==0.6.2` — word-level diffs in `05_transforming.py`.
- `typing_extensions==4.16.0` — required by `redlines` on this Python version.
- `panel==1.10.0` — local web UI for `07_chatbot.py`.

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
cd ~/code/ai-engineer-roadmap/03_prompting_for_developers
source .venv/bin/activate

python 01_guidelines.py
python 02_iterative.py
python 03_summarizing.py
python 04_inferring.py
python 05_transforming.py
python 06_expanding.py
python 07_chatbot.py
```

`01`–`06` print completions to the terminal. By default each file runs its
last uncommented example; earlier ones sit in a triple-quoted block.
Uncomment one block at a time if you want to replay a specific prompt.

`07_chatbot.py` starts a local Panel server and opens a browser (OrderBot).
Chat there, then stop the server (Ctrl+C in the terminal). After that, the
script prints a JSON summary of the order collected in `context`. In a
notebook a bare `dashboard` is enough to render; from a `.py` file the script
calls `dashboard.show()`.

You can tell the environment is active because `(.venv)` appears at the start of
your prompt. To check which Python is being used:

```bash
which python
```

It should print a path inside `03_prompting_for_developers/.venv/bin/`.

`__pycache__/` is created by Python when it compiles a local module. You do
not create it by hand. Running `python 01_guidelines.py` as the main program
often does not write a cache for that file; that is normal. If you want to see
the folder once:

```bash
python -m py_compile 01_guidelines.py
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
cd ~/code/ai-engineer-roadmap/03_prompting_for_developers
source .venv/bin/activate
python 01_guidelines.py
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
the course wraps but end those lines with `\` and no trailing space.

The notebooks used `openai.ChatCompletion.create`, `model="gpt-3.5-turbo"`,
and `temperature=0`. This folder uses `OpenAI()` and
`client.chat.completions.create`, and calls `gpt-5-nano`. That model only
allows the default temperature (`1`), so `temperature` is commented out in the
helpers (including the low-vs-high comparison in `06_expanding.py`).
Completions are objects: `response.choices[0].message.content`.

`02_iterative.py` and `05_transforming.py` import `IPython.display`. In a
notebook that renders HTML; from the terminal you still get the text (and
sometimes raw markup). That is expected.

## Troubleshooting

- `ModuleNotFoundError: No module named 'openai'`: the environment is not
  activated, or the package was installed elsewhere. Activate it and run
  `pip show openai`.
- `ModuleNotFoundError: No module named 'dotenv'`: install with
  `pip install python-dotenv` inside the activated environment, or
  `pip install -r requirements.txt`.
- `ModuleNotFoundError: No module named 'IPython'` / `'redlines'` / `'panel'`:
  install with `pip install -r requirements.txt` inside the activated
  environment.
- `APIRemovedInV1` / `openai.ChatCompletion`: leftover pre-1.0 syntax. Use
  `client = OpenAI(...)` and `client.chat.completions.create`.
- `SyntaxWarning: "\ " is an invalid escape sequence`: a course wrap still
  has a space after `\`. Remove that trailing space so the line ends with `\`.
- `BadRequestError: 'temperature' does not support 0 with this model`
  (or a value other than `1`): `gpt-5-nano` rejects non-default temperature.
  Leave `temperature` commented out, or pass `1`.
- `BadRequestError` / `AuthenticationError` / `401`: `OPENAI_API_KEY` is
  missing, empty, or wrong in the root `.env`.
- Completions never print and there is no traceback: `find_dotenv()` did not
  find the root `.env`. `cd` into this folder (or the repo) and run again.
- `07_chatbot.py` starts but no browser opens: look at the Panel URL printed
  in the terminal (usually `http://localhost:5006`) and open it yourself.

## Managing dependencies

`requirements.txt` in this folder lists the packages this example needs, pinned
to exact versions. It plays the same role as `package.json` in a Node project:
it is the record of what must be installed.

To install (or reinstall) everything into an activated environment:

```bash
cd ~/code/ai-engineer-roadmap/03_prompting_for_developers
source .venv/bin/activate
pip install -r requirements.txt
```

If you add a package you intend to keep, add its pinned version to
`requirements.txt` by hand. Prefer a short list of **direct** imports
(`openai`, `python-dotenv`, `ipython`, `redlines`, `panel`) over `pip freeze`,
which also dumps transitive packages.

Keep `openai==3.55.1` (or another 1.x/3.x release). Do not pin `0.28.x`; that
old client is what the course notebooks used, and it does not match this
folder's `OpenAI()` client.
