# Reasoning Models — Course Examples

This folder holds the coding examples for *Reasoning with Reasoning Models*
(DeepLearning.AI / OpenAI). The scripts use the current OpenAI Python SDK
(`OpenAI()` and `client.chat.completions.create`), one file per lesson:

- `01_prompting.py` — prompting `gpt-5-nano`: a vague vs. a simple prompt, a
  structured customer-service policy, and a few-shot legal example. Earlier
  blocks are commented; the currently active example is the few-shot legal
  query. From a terminal, Markdown is written to a temp HTML file and opened
  in the browser.
- `02_planning.py` — orchestrator pattern: the reasoning model writes a
  supply-chain plan; `gpt-6-luna` with `reasoning_effort="none"` executes it
  with tool calls against in-Python inventory/order state. A previous run is
  saved in `02_plannning_response.txt`.
- `03_coding.py` — currently asks the non-reasoning model to clean up a messy
  `process_orders` Python function. A commented block generates a React
  Interview Feedback Form; saved outputs of that run are
  `03_non_reasoning_app.tsx` and `03_reasoning_app.tsx`. Another commented
  block compares both models on the cleanup task.
- `04_reasoning_with_images.py` — encodes `data/org_chart_sample.png`, asks
  what it is, extracts the org hierarchy as JSON, then answers a ranking
  question from that JSON. `data/erd-relation-order.png` is a second sample
  image (its path is printed at the end of the script).
- `05_meta_prompting.py` — converts
  `originalPolicy/flightCancellationsPolicy.md` into an executable routine,
  then evals a non-reasoning agent against `evals/policyEvals.csv` using
  tools from `functionDefinitions.py`. The iterative rewrite loop (reasoning
  model revises the prompt from failures and plots accuracy) is commented
  out because it is expensive.
- `functionDefinitions.py` — airline-cancellation tool schemas used by the
  meta-prompting lesson.

Fast-reference Q&A for the same course:
[study_docs_qa/03_prompting_and_integration/03_reasoning_with_reasoning_models.md](../study_docs_qa/03_prompting_and_integration/03_reasoning_with_reasoning_models.md).

For a beginner-friendly study reference about `.venv/`, `__pycache__/`, and
the `__init__` method, see
[PYTHON_REFERENCE.md](../PYTHON_REFERENCE.md) at the repository root. It applies
to every Python folder in this repository.

## Project layout

```
04_reasoning_models/
├── .venv/                        # local virtual environment (not committed)
├── __pycache__/                  # compiled bytecode, if Python created it (not committed)
├── README.md
├── requirements.txt              # pinned dependencies for this folder
├── 01_prompting.py
├── 02_planning.py
├── 02_plannning_response.txt     # saved planner output from a previous run
├── 03_coding.py
├── 03_non_reasoning_app.tsx      # saved React output from a commented 03_coding.py block
├── 03_reasoning_app.tsx          # saved React output from a commented 03_coding.py block
├── 04_reasoning_with_images.py
├── 05_meta_prompting.py
├── functionDefinitions.py
├── data/
│   ├── org_chart_sample.png      # org chart used by the vision lesson
│   └── erd-relation-order.png    # extra sample image
├── evals/
│   └── policyEvals.csv           # golden set for the meta-prompting agent
└── originalPolicy/
    └── flightCancellationsPolicy.md
```

Each folder that has its own Python code can have its own `.venv/`. The
repository root `.gitignore` ignores every `.venv/` and `__pycache__/`, so
neither is committed.

Credentials live in a single `.env` at the **repository root** (one level above
this folder), so every script in the repository shares it:

```
ai-engineer-roadmap/
├── .env                          # real credentials (not committed)
└── 04_reasoning_models/
    └── 01_prompting.py
```

## First-time setup

This folder works with the system Python (here, 3.14). Check your version:

```bash
python3 --version
```

Then:

```bash
cd ~/code/ai-engineer-roadmap/04_reasoning_models
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### What each step does

**`cd ~/code/ai-engineer-roadmap/04_reasoning_models`** moves into the folder
that contains the scripts. The environment is created here, next to the code
it is used for.

**`python3 -m venv .venv`** creates a self-contained virtual environment in
`.venv/`, so packages are installed for this project without modifying your
system Python.

**`source .venv/bin/activate`** makes `python` and `pip` point into `.venv/`.
You will usually see `(.venv)` in your prompt.

**`pip install -r requirements.txt`** installs the pinned packages into
`.venv/`:

- `openai==3.55.1` — current OpenAI Python client (`OpenAI()` plus
  `client.chat.completions.create`).
- `python-dotenv==1.2.4` — loads `OPENAI_API_KEY` from `.env`.
- `ipython==9.18.1` — `IPython.display` used by `01_prompting.py` when run in
  a notebook.
- `matplotlib==3.11.2` — accuracy chart in the commented meta-prompting
  rewrite loop.
- `pandas==3.1.1` — eval tables in `05_meta_prompting.py`.
- `redlines==0.6.2` — prompt diffs in the meta-prompting lesson.
- `termcolor==3.3.0` — colored transcripts in `05_meta_prompting.py`.
- `tiktoken==0.14.0` — local token counts so the rewrite loop stays inside
  the context window.

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
cd ~/code/ai-engineer-roadmap/04_reasoning_models
source .venv/bin/activate

python 01_prompting.py
python 02_planning.py
python 03_coding.py
python 04_reasoning_with_images.py
python 05_meta_prompting.py
```

Each file may have extra examples commented out; uncomment one block at a time
if you want to replay a specific prompt. Several lessons call the API more
than once and can take a while (reasoning models spend extra tokens thinking).

`02_planning.py` and `05_meta_prompting.py` make many sequential or parallel
API calls. The default `05_meta_prompting.py` run converts the policy and
scores `evals/policyEvals.csv`; leave the rewrite loop at the bottom
commented unless you want to spend a large token budget.

`04_reasoning_with_images.py` reads `data/` with a relative path, so run it
from this folder. `05_meta_prompting.py` locates `originalPolicy/` and
`evals/` from `__file__`, so it can run from elsewhere inside the repo.

You can tell the environment is active because `(.venv)` appears at the start of
your prompt. To check which Python is being used:

```bash
which python
```

It should print a path inside `04_reasoning_models/.venv/bin/`.

`__pycache__/` is created by Python when it compiles a local module. You do
not create it by hand. Deleting it is safe; Python regenerates it when needed.

## When you are done

```bash
deactivate
```

This restores your terminal to the system Python. It does **not** delete the
environment or uninstall anything, so you can activate it again later.

## Coming back later

You do **not** need to reinstall anything:

```bash
cd ~/code/ai-engineer-roadmap/04_reasoning_models
source .venv/bin/activate
python 01_prompting.py
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

The notebooks used older model names (o1 / GPT-4o). This folder uses
`gpt-5-nano` as the reasoning model and `gpt-6-luna` with
`reasoning_effort="none"` as the non-reasoning model.

Helpers call `client.chat.completions.create`. Completions are objects:
`response.choices[0].message.content`.

`01_prompting.py` imports `IPython.display`. In a notebook that renders HTML;
from the terminal you still get the text (and sometimes an HTML file opens in
the browser). That is expected.

The original meta-prompting notebook chained a chat model for structured
JSON. The commented rewrite loop in `05_meta_prompting.py` sends
`response_format` with a JSON schema on the reasoning model instead.

## Troubleshooting

- `ModuleNotFoundError: No module named 'openai'`: the environment is not
  activated, or the package was installed elsewhere. Activate it and run
  `pip show openai`.
- `ModuleNotFoundError: No module named 'dotenv'`: install with
  `pip install python-dotenv` inside the activated environment, or
  `pip install -r requirements.txt`.
- `ModuleNotFoundError: No module named 'IPython'` / `'redlines'` /
  `'pandas'` / `'matplotlib'` / `'tiktoken'` / `'termcolor'`: install with
  `pip install -r requirements.txt` inside the activated environment.
- `APIRemovedInV1` / `openai.ChatCompletion`: leftover pre-1.0 syntax. Use
  `client = OpenAI(...)` and `client.chat.completions.create`.
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
cd ~/code/ai-engineer-roadmap/04_reasoning_models
source .venv/bin/activate
pip install -r requirements.txt
```

If you add a package you intend to keep, add its pinned version to
`requirements.txt` by hand. Prefer a short list of **direct** imports over
`pip freeze`, which also dumps transitive packages.

Keep `openai==3.55.1` (or another 1.x/3.x release). Do not pin `0.28.x`.
