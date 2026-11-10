# Fine-tuning vs. Non-fine-tuned Models

This folder compares the output of a fine-tuned Lamini model against the same
base model without fine-tuning.

- `finetuned_vs_non_finetuned.py` — sends the same prompt
  (`"Tell me how to train my dog to sit"`) to a non-fine-tuned
  `meta-llama/Llama-2-7b-hf` model and prints the result.

For a beginner-friendly study reference about `.venv/`, `__pycache__/`, and
the `__init__` method, see
[PYTHON_REFERENCE.md](../PYTHON_REFERENCE.md) at the repository root. It applies
to every Python folder in this repository.

## Project layout

```
finetuning/
├── .venv/                        # local virtual environment (not committed)
├── __pycache__/                  # compiled bytecode (not committed)
├── README.md
├── requirements.txt              # pinned dependencies for this folder
└── finetuned_vs_non_finetuned.py
```

Credentials live in a single `.env` at the **repository root** (one level above
this folder), so every script in the repository shares it:

```
ai-engineer-roadmap/
├── .env                          # real credentials (not committed)
└── finetuning/
    └── finetuned_vs_non_finetuned.py
```

## First-time setup

This folder needs **Python 3.11 or 3.12**. `lamini` pins `numpy<2.0.0`, and
NumPy 1.x has no prebuilt wheels for Python 3.13 or newer. On Python 3.13+ pip
tries to compile NumPy from source, which hangs or fails.

Check your version first:

```bash
python3 --version
```

If it reports 3.11.x or 3.12.x, use it directly:

```bash
cd ~/code/ai-engineer-roadmap/finetuning
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Otherwise, install `uv` (no sudo needed) so it can download a compatible
Python:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

cd ~/code/ai-engineer-roadmap/finetuning
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

> Recent `uv` versions do not create `$HOME/.local/bin/env`; use the
> `export PATH=...` line above, or open a new terminal.

### What each step does

**`cd ~/code/ai-engineer-roadmap/finetuning`** moves into the folder that
contains the script. The environment is created here, next to the code it is
used for.

**`python3 -m venv .venv`** (or **`uv venv --python 3.12 .venv`**) creates a
self-contained virtual environment in `.venv/`, so packages are installed for
this project without modifying your system Python. The `uv` form downloads and
uses a managed Python 3.12 even if the system Python is newer.

**`source .venv/bin/activate`** makes `python` and `pip` point into `.venv/`.
You will usually see `(.venv)` in your prompt.

**`pip install -r requirements.txt`** (or **`uv pip install -r
requirements.txt`**) installs the pinned packages into `.venv/`:

- `lamini==2.5.7` — the client used to call Lamini models. This is the last
  release that still exposes `BasicModelRunner` and whose internals agree with
  each other. `3.0.x` is broken for this class, `3.0.5+` removed it, and
  `3.4.4+` declares a `umap` dependency that does not exist on PyPI.
- `python-dotenv==1.2.4` — loads the credentials from the `.env` file into the
  environment.

`requirements.txt` is the Python equivalent of `package.json` in a Node
project: it records the exact versions this folder needs, so the environment can
be recreated elsewhere.

> `os` is part of Python's standard library, so it is **not** installed with
> `pip`. Importing it always works.

## Credentials: keep them secret

The script reads two values from environment variables:

- `POWERML__PRODUCTION__URL`
- `POWERML__PRODUCTION__KEY`

These are **critical secrets**. The API key can be used to run workloads and
bill your account, so it must never be committed, pasted into chat, or shared.

They live in a single `.env` file at the **repository root**. Create or edit it:

```bash
cd ~/code/ai-engineer-roadmap
nano .env
```

It should contain only these two lines:

```dotenv
POWERML__PRODUCTION__URL=https://api.lamini.ai
POWERML__PRODUCTION__KEY=your-secret-key
```

Do not use `none` or another placeholder as the URL. If the script reports
`Missing or placeholder Lamini credentials`, the value is still empty or `none`.

Rules for this file:

- `.env` is listed in the repository-root `.gitignore`, so Git ignores it.
- There is no committed template: never put real keys in a tracked file.
- If you ever commit a key by accident, rotate it immediately in Lamini.
- The script loads the root `.env` explicitly with
  `load_dotenv(Path(__file__).resolve().parent.parent / ".env")`, so it works
  regardless of which directory you run it from.

The script stops with a clear error if either value is missing or still set to
`none`.

## Running the script

Every time you open a **new terminal**, activate the environment first:

```bash
cd ~/code/ai-engineer-roadmap/finetuning
source .venv/bin/activate
python finetuned_vs_non_finetuned.py
```

You can tell the environment is active because `(.venv)` appears at the start
of your prompt. To check which Python is being used:

```bash
which python
```

It should print a path inside `finetuning/.venv/bin/`.

## When you are done

```bash
deactivate
```

This restores your terminal to the system Python. It does **not** delete the
environment or uninstall anything, so you can activate it again later.

## Coming back later

You do **not** need to reinstall anything:

```bash
cd ~/code/ai-engineer-roadmap/finetuning
source .venv/bin/activate
python finetuned_vs_non_finetuned.py
deactivate
```

## Virtual environment rules

- A virtual environment contains **absolute paths**. It cannot be moved or
  renamed. If it is in the wrong folder, delete it and create it again.
- Only one environment can be active in a terminal at a time. Run `deactivate`
  before activating a different one.
- Activation is per terminal. A new terminal starts with the system Python, so
  activate the environment again.

## Troubleshooting

- `ModuleNotFoundError: No module named 'lamini'`: the environment is not
  activated, or the package was installed elsewhere. Activate it and run
  `pip show lamini`.
- `ModuleNotFoundError: No module named 'dotenv'`: install it with
  `pip install python-dotenv`.
- `ModuleNotFoundError: No module named 'llama'`: the original course snippet
  used `from llama import BasicModelRunner`, which only works on an old
  `lamini` release. This folder uses `from lamini import BasicModelRunner`.
- `ImportError: cannot import name 'BasicModelRunner' from 'lamini'`: you have
  `lamini` 3.0.5 or newer. Install the pinned version with
  `pip install -r requirements.txt`.
- `TypeError: Lamini.__init__() got an unexpected keyword argument
  'local_cache_file'`: you have `lamini` 3.0.0–3.0.4, which is internally
  inconsistent. Install the pinned `2.5.7`.
- `error: No solution found ... umap was not found`: you have `lamini` 3.4.4+,
  which depends on a package that does not exist on PyPI. Install the pinned
  `2.5.7`.
- pip hangs at `Preparing metadata (pyproject.toml)` for `numpy`: your Python is
  3.13+ and NumPy is being compiled from source. Use Python 3.11/3.12 (see
  setup above).
- `RuntimeError: Missing or placeholder Lamini credentials`: the root `.env` is
  missing, empty, or still contains `none`. Set both values in
  `~/code/ai-engineer-roadmap/.env`.
- `requests.exceptions.MissingSchema: Invalid URL 'none/v1/completions'`: the URL
  in the root `.env` is the literal placeholder `none`. Set the real Lamini URL,
  usually `https://api.lamini.ai`.
- `401` or authentication errors from Lamini: the URL or key in the root `.env`
  is wrong, or the key was rotated.

## Managing dependencies

`requirements.txt` in this folder lists the packages this example needs, pinned
to exact versions. It plays the same role as `package.json` in a Node project:
it is the record of what must be installed.

To install (or reinstall) everything into an activated environment:

```bash
cd ~/code/ai-engineer-roadmap/finetuning
source .venv/bin/activate
pip install -r requirements.txt
# or: uv pip install -r requirements.txt
```

If you add or upgrade a package, update the file from the activated environment:

```bash
pip freeze > requirements.txt
# or: uv pip freeze > requirements.txt
```

Keep the `lamini` and `python-dotenv` versions pinned as shown; newer `lamini`
releases break the `BasicModelRunner` import used by this script.
