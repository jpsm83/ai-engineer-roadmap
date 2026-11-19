# Attention in Transformers — Course Examples

This folder holds the coding examples for *Attention in Transformers: Concepts
and Code in PyTorch* (StatQuest). The scripts are small, forward-only PyTorch
demos of the attention math, with `d_model=2` so the matrices can be checked
by hand. They do not train a model.

- `self_attention.py` — `SelfAttention`: full self-attention,
  `softmax(QK^T / sqrt(d_k)) V`. Queries, keys, and values all come from the
  same sequence.
- `masked_self_attention.py` — `MaskedSelfAttention`: causal (masked)
  self-attention, where each token may only attend to itself and earlier
  tokens.
- `encoder_decoder_attention.py` — `Attention` (encoder-decoder / cross
  attention) with separate query, key, and value inputs, plus a simplified
  `MultiHeadAttention` that concatenates several heads.

Fast-reference Q&A for the same course:
[study_docs_qa/02_llm_literacy/01_attention_in_transformers.md](../study_docs_qa/02_llm_literacy/01_attention_in_transformers.md).

For a beginner-friendly study reference about `.venv/`, `__pycache__/`, and
the `__init__` method, see
[PYTHON_REFERENCE.md](../PYTHON_REFERENCE.md) at the repository root. It applies
to every Python folder in this repository.

## Project layout

```
01_attention_transformers/
├── .venv/                        # local virtual environment (not committed)
├── __pycache__/                  # compiled bytecode, if Python created it (not committed)
├── README.md
├── requirements.txt              # pinned dependencies for this folder
├── encoder_decoder_attention.py
├── masked_self_attention.py
└── self_attention.py
```

Each folder that has its own Python code can have its own `.venv/`. The
repository root `.gitignore` ignores every `.venv/` and `__pycache__/`, so
neither is committed.

## First-time setup

This folder works with the system Python (here, 3.14). Check your version:

```bash
python3 --version
```

Then:

```bash
cd ~/code/ai-engineer-roadmap/01_attention_transformers
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` pins the packages used here. It is the Python equivalent of
`package.json` in a Node project: it records what to install so the environment
can be recreated on another machine.

The first line, `--extra-index-url https://download.pytorch.org/whl/cpu`,
installs the CPU-only build of PyTorch (`torch==2.15.0+cpu`, about 210 MB).
A plain `pip install torch` on Linux pulls the CUDA build and its NVIDIA
dependencies, which can exceed 3 GB and may fail with
`OSError: [Errno 122] Disk quota exceeded`. Running this small example does
not need CUDA.

### What each step does

**`cd ~/code/ai-engineer-roadmap/01_attention_transformers`** moves into the
folder that contains the example scripts. The environment is created here, next
to the code it is used for.

**`python3 -m venv .venv`** creates a self-contained virtual environment in
`.venv/`, so packages are installed for this project without modifying your
system Python.

**`source .venv/bin/activate`** makes `python` and `pip` point into `.venv/`.
You will usually see `(.venv)` in your prompt.

**`pip install -r requirements.txt`** installs the pinned package into
`.venv/`:

- `torch==2.15.0+cpu` — tensors, `nn.Module`, `nn.Linear`, and `F.softmax`.
  The `+cpu` build comes from the extra index URL at the top of the file.

> Use `pwd` to check the current directory and `cd` to move around. All
> commands below assume you are inside `01_attention_transformers/`.

## Running the examples

Every time you open a **new terminal**, activate the environment first:

```bash
cd ~/code/ai-engineer-roadmap/01_attention_transformers
source .venv/bin/activate
python self_attention.py
python masked_self_attention.py
python encoder_decoder_attention.py
```

Each script uses `torch.manual_seed(42)` and the same 3×2 encodings matrix so
the printed numbers can be compared across files. They print:

- the attention output
- `W_q`, `W_k`, and `W_v` (transposed, so they match the paper's notation)
- the intermediate matrices: `q`, `k`, similarities, scaled scores, and
  softmax weights

`masked_self_attention.py` also prints the boolean mask.
`encoder_decoder_attention.py` then runs `MultiHeadAttention` with 1 head and
with 2 heads.

You can tell the environment is active because `(.venv)` appears at the start
of your prompt. You can also check which Python is being used:

```bash
which python
```

It should print a path inside `01_attention_transformers/.venv/bin/`.

`__pycache__/` is created by Python when it compiles a local module. You do
not create it by hand. Deleting it is safe; Python regenerates it when needed.

## How the mask works

`masked_self_attention.py` creates a causal mask:

```python
mask = torch.tril(torch.ones(3, 3))
mask = mask == 0
```

For three tokens this produces:

```
tensor([[False,  True,  True],
        [False, False,  True],
        [False, False, False]])
```

`True` marks positions that must be hidden: tokens that come *after* the token
being processed. Before softmax, `masked_fill(mask=mask, value=-1e9)` replaces
those scores with a very negative number, so their attention weights become
approximately zero.

This is why the first token can only attend to itself, the second token to the
first two, and so on. This pattern is called **causal** or **masked**
self-attention and is used in decoder-only models such as GPT.

The `W_q` / `W_k` / `W_v` layers use `bias=False`, matching *Attention Is All
You Need*.

## Encoder-decoder (cross) attention

`encoder_decoder_attention.py` uses the same attention formula, but the
`Attention.forward` method accepts three separate inputs:

```python
attention(encodings_for_q, encodings_for_k, encodings_for_v)
```

- queries come from the decoder,
- keys and values come from the encoder.

This is **cross-attention**. The demo uses the same matrix for all three
inputs, so its numbers match self-attention. Passing different matrices would
make the cross-attention behavior easier to see.

## Multi-head attention

The same file also defines a simplified `MultiHeadAttention` class. It creates
several independent `Attention` heads (`nn.ModuleList`) and concatenates their
outputs along `col_dim`.

With `d_model=2` and `num_heads=2`, the output has **4 columns**: two per head.
A full Transformer adds a final output projection that maps the concatenated
result back to `d_model`. That projection is intentionally omitted here to keep
the example small.

## When you are done

```bash
deactivate
```

This restores your terminal to the system Python. It does **not** delete the
environment or uninstall anything, so you can activate it again later.

## Coming back later

You do **not** need to reinstall anything:

```bash
cd ~/code/ai-engineer-roadmap/01_attention_transformers
source .venv/bin/activate
python self_attention.py
python masked_self_attention.py
python encoder_decoder_attention.py
deactivate
```

To check that PyTorch is installed inside the environment:

```bash
cd ~/code/ai-engineer-roadmap/01_attention_transformers
source .venv/bin/activate
python -c "import torch; print(torch.__version__)"
```

## Virtual environment rules

- A virtual environment contains **absolute paths**. It cannot be moved or
  renamed. If it is in the wrong folder, delete it and create it again:

  ```bash
  rm -rf .venv
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

- Only one environment can be active in a terminal at a time. Run `deactivate`
  before activating a different one.
- Activation is per terminal. A new terminal starts with the system Python, so
  activate the environment again.

## Troubleshooting

- `ModuleNotFoundError: No module named 'torch'`: the environment is not
  activated, or PyTorch was installed into a different environment. Activate
  it and run `pip show torch`.
- `OSError: [Errno 122] Disk quota exceeded`: pip ran out of space while
  downloading the CUDA build. Clear pip's download cache with
  `pip cache purge`, then install the CPU-only build shown above.
- `Failed to initialize NumPy: No module named 'numpy'`: only a warning for
  this example. Install NumPy with `pip install numpy` if you want to silence
  it.

## Managing dependencies

`requirements.txt` in this folder lists the packages this example needs, pinned
to exact versions. It plays the same role as `package.json` in a Node project:
it is the record of what must be installed.

To install (or reinstall) everything into an activated environment:

```bash
cd ~/code/ai-engineer-roadmap/01_attention_transformers
source .venv/bin/activate
pip install -r requirements.txt
```

If you add a package you intend to keep, add its pinned version to
`requirements.txt` by hand. Prefer a short list of **direct** imports (`torch`)
over `pip freeze`, which also dumps transitive packages.

Keep the `--extra-index-url` line at the top of the file, and keep the `+cpu`
PyTorch pin. Without that index URL, `pip install -r` will not find
`torch==2.15.0+cpu`.
