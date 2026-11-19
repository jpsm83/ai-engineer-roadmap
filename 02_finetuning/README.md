# Fine-tuning Course Examples

This folder holds the coding examples for *Finetuning Large Language Models*
(DeepLearning.AI / Lamini). The scripts walk from inspecting data through a
short local training run, then compare a fine-tuned model with its base
model:

- `01_finetuned_vs_non_finetuned.py` — sends the same prompts to a
  non-fine-tuned `meta-llama/Llama-2-7b-hf` model and to
  `meta-llama/Llama-2-7b-chat-hf`, then prints both results. Needs Lamini
  credentials.
- `02_finetuning_data.py` — streams a few C4 pretraining examples, then
  builds `lamini_docs_processed.jsonl` from `lamini_docs.jsonl` using
  text-only and question/answer prompt templates. Also loads
  `lamini/lamini_docs` from the Hugging Face Hub.
- `03_data_preparation.py` — tokenizer basics on `EleutherAI/pythia-70m`
  (padding, truncation, prompt templating), then tokenized train/test
  splits from the local JSONL. Also peeks at Hub datasets
  (`lamini/lamini_docs`, `lamini/taylor_swift`).
- `04_training_process.py` — a short local Hugging Face training run of
  `EleutherAI/pythia-70m` (CPU friendly, 3 steps), saved under
  `lamini_docs_3_steps/`, then compared with `lamini/lamini_docs_finetuned`.
  Hosted Lamini training is skipped when credentials are missing.
- `05_evaluation.py` — exact-match evaluation of
  `lamini/lamini_docs_finetuned` on the Hub test split, plus an optional
  lm-evaluation-harness ARC Easy benchmark.

Fast-reference Q&A for the same course:
[study_docs_qa/02_llm_literacy/02_finetuning_large_language_models.md](../study_docs_qa/02_llm_literacy/02_finetuning_large_language_models.md).

For a beginner-friendly study reference about `.venv/`, `__pycache__/`, and
the `__init__` method, see
[PYTHON_REFERENCE.md](../PYTHON_REFERENCE.md) at the repository root. It applies
to every Python folder in this repository.

## Project layout

```
02_finetuning/
├── .venv/                        # local virtual environment (not committed)
├── __pycache__/                  # compiled bytecode, if Python created it (not committed)
├── README.md
├── requirements.txt              # pinned dependencies for this folder
├── 01_finetuned_vs_non_finetuned.py
├── 02_finetuning_data.py
├── 03_data_preparation.py
├── 04_training_process.py
├── 05_evaluation.py
├── lamini_docs.jsonl             # raw instruction data
└── lamini_docs_processed.jsonl   # written by 02_finetuning_data.py
```

Each folder that has its own Python code can have its own `.venv/`. The
repository root `.gitignore` ignores every `.venv/` and `__pycache__/`, so
neither is committed.

`04_training_process.py` also writes `lamini_docs_3_steps/` (local
checkpoints). `05_evaluation.py` looks for an optional
`lm-evaluation-harness/` clone next to the scripts.

Credentials live in a single `.env` at the **repository root** (one level above
this folder), so every script in the repository shares it:

```
ai-engineer-roadmap/
├── .env                          # real credentials (not committed)
└── 02_finetuning/
    ├── 01_finetuned_vs_non_finetuned.py
    └── 04_training_process.py
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
cd ~/code/ai-engineer-roadmap/02_finetuning
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Otherwise, install `uv` (no sudo needed) so it can download a compatible
Python:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

cd ~/code/ai-engineer-roadmap/02_finetuning
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

> Recent `uv` versions do not create `$HOME/.local/bin/env`; use the
> `export PATH=...` line above, or open a new terminal.

### What each step does

**`cd ~/code/ai-engineer-roadmap/02_finetuning`** moves into the folder that
contains the scripts. The environment is created here, next to the code it is
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
  each other. Do not upgrade: `3.0.x` is broken for this class, `3.0.5+`
  removed it, and `3.4.4+` declares a `umap` dependency that does not exist on
  PyPI.
- `python-dotenv==1.2.4` — loads the credentials from the `.env` file into the
  environment.
- `pandas==3.0.6` / `jsonlines==4.0.0` / `datasets==3.6.0` — local data
  inspection and train/test splits. `pandas` stays on 3.0.6 because
  `lamini==2.5.7` requires `numpy<2`, which newer pandas does not.
- `transformers==4.57.6` — tokenizers, model classes, and `Trainer` (latest
  4.x; 5.x is a different API).
- `huggingface-hub==0.34.0` / `pyarrow==17.0.0` — required by `transformers`
  and `datasets`.
- `torch==2.15.0` — the deep-learning backend used by `transformers`.
- `accelerate==1.16.0` — required by the Transformers `Trainer`.
- `tqdm==4.70.1` — progress bars in the evaluation script.

`requirements.txt` is the Python equivalent of `package.json` in a Node
project: it records the exact versions this folder needs, so the environment can
be recreated elsewhere.

> `os` is part of Python's standard library, so it is **not** installed with
> `pip`. Importing it always works.

## Credentials: keep them secret

`01_finetuned_vs_non_finetuned.py` requires two values from environment
variables. `04_training_process.py` uses the same values for its hosted
Lamini section and skips that section when they are missing. The other
scripts do not call Lamini; they download models and datasets from the
Hugging Face Hub.

- `POWERML__PRODUCTION__URL`
- `POWERML__PRODUCTION__KEY`

These are **critical secrets**. The API key can be used to run workloads and
bill your account, so it must never be committed, pasted into chat, or shared.

They live in a single `.env` file at the **repository root**. Create or edit it:

```bash
cd ~/code/ai-engineer-roadmap
nano .env
```

Add these lines (alongside any other keys this repo already uses):

```dotenv
POWERML__PRODUCTION__URL=https://api.lamini.ai
POWERML__PRODUCTION__KEY=your-secret-key
```

Do not use `none` or another placeholder as the URL. If `01` reports
`Missing or placeholder Lamini credentials`, the value is still empty or `none`.

Rules for this file:

- `.env` is listed in the repository-root `.gitignore`, so Git ignores it.
- There is no committed template: never put real keys in a tracked file.
- If you ever commit a key by accident, rotate it immediately in Lamini.
- `01` and `04` load the root `.env` explicitly with
  `load_dotenv(Path(__file__).resolve().parent.parent / ".env")`, so they
  work regardless of which directory you run them from.

`01_finetuned_vs_non_finetuned.py` stops with a clear error if either value
is missing or still set to `none`.

## Running the scripts

Every time you open a **new terminal**, activate the environment first:

```bash
cd ~/code/ai-engineer-roadmap/02_finetuning
source .venv/bin/activate

# Requires valid Lamini credentials in the repository-root .env
python 01_finetuned_vs_non_finetuned.py

# Local data inspection; first run downloads C4 and Hub datasets
python 02_finetuning_data.py
python 03_data_preparation.py

# Short local training of pythia-70m; writes lamini_docs_3_steps/
# Lamini-hosted parts are skipped without credentials
python 04_training_process.py

# Exact-match eval of lamini/lamini_docs_finetuned; harness is optional
python 05_evaluation.py
```

`02`–`05` download models or datasets from the Hugging Face Hub on first
run (C4, `EleutherAI/pythia-70m`, `lamini/lamini_docs`,
`lamini/lamini_docs_finetuned`, and related Hub datasets). `01` and the
hosted section of `04` call Lamini instead.

`05_evaluation.py` skips the optional benchmark unless `lm_eval` is installed
or a local `lm-evaluation-harness/` directory exists next to it.

You can tell the environment is active because `(.venv)` appears at the start
of your prompt. To check which Python is being used:

```bash
which python
```

It should print a path inside `02_finetuning/.venv/bin/`.

## When you are done

```bash
deactivate
```

This restores your terminal to the system Python. It does **not** delete the
environment or uninstall anything, so you can activate it again later.

## Coming back later

You do **not** need to reinstall anything:

```bash
cd ~/code/ai-engineer-roadmap/02_finetuning
source .venv/bin/activate
python 02_finetuning_data.py
python 03_data_preparation.py
deactivate
```

Those two scripts need no Lamini credentials. Run `01` only when the root
`.env` has real Lamini values.

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
- Hugging Face Hub download errors on `02`–`05`: those scripts fetch C4,
  `EleutherAI/pythia-70m`, or Lamini Hub datasets/models on first run. Check
  the network, then retry.

## Managing dependencies

`requirements.txt` in this folder lists the packages this example needs, pinned
to exact versions. It plays the same role as `package.json` in a Node project:
it is the record of what must be installed.

To install (or reinstall) everything into an activated environment:

```bash
cd ~/code/ai-engineer-roadmap/02_finetuning
source .venv/bin/activate
pip install -r requirements.txt
# or: uv pip install -r requirements.txt
```

If you add a package you intend to keep, add its pinned version to
`requirements.txt` by hand. Prefer a short list of **direct** imports
(`lamini`, `python-dotenv`, `jsonlines`, `pandas`, `datasets`, `transformers`,
`torch`, `accelerate`, `tqdm`) over `pip freeze`, which also dumps transitive
packages.

Keep `lamini==2.5.7`. Newer `lamini` releases break the `BasicModelRunner`
import used by these scripts. Keep `transformers` on 4.x; 5.x changes the
Trainer API this course uses.
