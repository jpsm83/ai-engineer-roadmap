# Prompting for Developers Course Examples

This folder holds the coding examples for *ChatGPT Prompt Engineering for
Developers* (DeepLearning.AI / OpenAI). The scripts keep the course's
`openai.ChatCompletion.create` helper and prompt text.

- `01_guidelines.py` — first lesson: write clear instructions (delimiters,
  structured output, conditionals, few-shot) and give the model time to think.
  Calls `gpt-5-nano` and prints each completion.

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
└── 01_guidelines.py
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
folder that contains the script. The environment is created here, next to the
code it is used for.

**`python3 -m venv .venv`** creates a self-contained virtual environment in
`.venv/`, so packages are installed for this project without modifying your
system Python.

**`source .venv/bin/activate`** makes `python` and `pip` point into `.venv/`.
You will usually see `(.venv)` in your prompt.

**`pip install -r requirements.txt`** installs the pinned packages into
`.venv/`:

- `openai==0.28.1` — the course client. This version still has
  `openai.ChatCompletion.create`. `openai` 1.x replaced that API.
- `python-dotenv==1.2.4` — loads `OPENAI_API_KEY` from `.env`.

`requirements.txt` is the Python equivalent of `package.json` in a Node
project: it records the exact versions this folder needs, so the environment can
be recreated elsewhere.

> `os` is part of Python's standard library, so it is **not** installed with
> `pip`. Importing it always works.

## Credentials: keep them secret

The script reads one environment variable:

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
- The script loads `.env` with `load_dotenv(find_dotenv())`, which walks up
  from the current working directory. Run the script from this folder or
  elsewhere inside the repository so it can find the root `.env`.

## Running the scripts

Every time you open a **new terminal**, activate the environment first:

```bash
cd ~/code/ai-engineer-roadmap/03_prompting_for_developers
source .venv/bin/activate
python 01_guidelines.py
```

The script makes several live API calls and prints each completion. You can
tell the environment is active because `(.venv)` appears at the start of your
prompt. To check which Python is being used:

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

## Course notes that differ from the original notebook

The notebook wraps long strings with `\` at the end of the line. A space after
that backslash (`\ `) is an invalid escape on Python 3.14. The `.py` file keeps
the course wraps but ends those lines with `\` and no trailing space.

The notebook used `model="gpt-3.5-turbo"` and `temperature=0`. This folder
calls `gpt-5-nano`. That model only allows the default temperature (`1`), so
`temperature=0` is commented out in `get_completion`.

## Troubleshooting

- `ModuleNotFoundError: No module named 'openai'`: the environment is not
  activated, or the package was installed elsewhere. Activate it and run
  `pip show openai`.
- `ModuleNotFoundError: No module named 'dotenv'`: install with
  `pip install python-dotenv` inside the activated environment, or
  `pip install -r requirements.txt`.
- `AttributeError: module 'openai' has no attribute 'ChatCompletion'`: you
  have `openai` 1.x. This folder needs `openai==0.28.1`.
- `SyntaxWarning: "\ " is an invalid escape sequence`: a course wrap still
  has a space after `\`. Remove that trailing space so the line ends with `\`.
- `InvalidRequestError: 'temperature' does not support 0 with this model`:
  `gpt-5-nano` rejects `temperature=0`. Leave that argument commented out.
- `InvalidRequestError` / `AuthenticationError` / `401`: `OPENAI_API_KEY` is
  missing, empty, or wrong in the root `.env`.
- Completions never print and there is no traceback: `find_dotenv()` did not
  find the root `.env`. `cd` into this folder (or the repo) and run again.

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
(`openai`, `python-dotenv`) over `pip freeze`, which also dumps transitive
packages.

Keep `openai==0.28.1`. Newer releases remove `ChatCompletion.create`, which
this course script still uses.
