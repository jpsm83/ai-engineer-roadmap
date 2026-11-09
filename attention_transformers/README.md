# Attention Examples

Small PyTorch implementations of attention:

- `self_attention.py` — full self-attention:
  `softmax(QK^T / sqrt(d_k)) V`.
- `masked_self_attention.py` — causal (masked) self-attention, where each token
  may only attend to itself and earlier tokens.
- `encoder_decoder_attention.py` — encoder-decoder (cross) attention with
  separate query, key, and value inputs, plus a simplified multi-head
  attention example.

For a beginner-friendly study reference about `.venv/`, `__pycache__/`, and
the `__init__` method, see
[PYTHON_REFERENCE.md](../PYTHON_REFERENCE.md) at the repository root. It applies
to every Python folder in this repository.

## Project layout

```
attention_transformers/
├── .venv/                        # local virtual environment (not committed)
├── __pycache__/                  # compiled bytecode (not committed)
├── README.md
├── encoder_decoder_attention.py
├── masked_self_attention.py
└── self_attention.py
```

Each folder that has its own Python code can have its own `.venv/`. The
repository root `.gitignore` ignores every `.venv/`, `venv/`, `env/`, and
`ENV/` folder, so no environment is ever committed.

## First-time setup

Open a terminal and run these commands from the repository root:

```bash
cd ~/code/ai-engineer-roadmap/attention_transformers
python3 -m venv .venv
source .venv/bin/activate
pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
```

The `--extra-index-url` installs the CPU-only build of PyTorch (about 210 MB).
A plain `pip install torch` on Linux pulls the CUDA build and its NVIDIA
dependencies, which can exceed 3 GB and may fail with
`OSError: [Errno 122] Disk quota exceeded`. Running this small example does
not need CUDA.

### What each step does

**`cd ~/code/ai-engineer-roadmap/attention_transformers`** moves into the
folder that contains the example scripts. The environment is created here, next
to the code it is used for.

**`python3 -m venv .venv`** creates a *virtual environment* in `.venv/`. This
is a self-contained Python installation with its own package folder:

```
.venv/
├── bin/          # python, pip, activate script
├── lib/          # installed packages (site-packages)
└── pyvenv.cfg    # environment config
```

Its purpose is to install packages for this project without modifying your
system Python.

**`source .venv/bin/activate`** temporarily changes the current terminal's
`PATH` so that `python` and `pip` point into `.venv/`. You will usually see
`(.venv)` in your prompt.

**`pip install torch --extra-index-url https://download.pytorch.org/whl/cpu`**
downloads PyTorch into `.venv/lib/.../site-packages`. It is not installed
globally, so it is only available while the environment is activated.

> Use `pwd` to check the current directory and `cd` to move around. All
> commands below assume you are inside `attention_transformers/`.

## Running the examples

Every time you open a **new terminal**, activate the environment first:

```bash
cd ~/code/ai-engineer-roadmap/attention_transformers
source .venv/bin/activate
python self_attention.py
python masked_self_attention.py
python encoder_decoder_attention.py
```

You can tell the environment is active because `(.venv)` appears at the start
of your prompt. You can also check which Python is being used:

```bash
which python
```

It should print a path inside `attention_transformers/.venv/bin/`.

## How the mask works

`masked_self_attention.py` creates a causal mask:

```python
mask = torch.tril(torch.ones(3, 3)) == 0
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

## Encoder-decoder (cross) attention

`encoder_decoder_attention.py` uses the same attention formula, but accepts
three separate inputs:

```python
attention(encodings_for_q, encodings_for_k, encodings_for_v)
```

- queries come from the decoder,
- keys and values come from the encoder.

This is **cross-attention**. The example uses the same matrix for all three
inputs, so its numbers match self-attention. Passing different matrices would
make the cross-attention behavior easier to see.

## Multi-head attention

The same file also defines a simplified `MultiHeadAttention` class. It creates
several independent `Attention` heads and concatenates their outputs along
`col_dim`.

With `d_model=2` and `num_heads=2`, the output has **4 columns**: two per head.
A full Transformer adds a final output projection that maps the concatenated
result back to `d_model`. That projection is intentionally omitted here to keep
the example small.

## When you are done

Yes, it is good practice to leave the environment when you finish:

```bash
deactivate
```

This restores your terminal to the system Python. The `(.venv)` prefix
disappears. It does **not** delete the environment or uninstall anything, so
you can activate it again later.

Closing the terminal also ends the environment for that terminal, but running
`deactivate` is the cleaner and more explicit choice.

## Coming back later

When you want to run the examples again, you do **not** need to reinstall
anything:

```bash
cd ~/code/ai-engineer-roadmap/attention_transformers
source .venv/bin/activate
python self_attention.py
python masked_self_attention.py
python encoder_decoder_attention.py
deactivate
```

To check that PyTorch is installed inside the environment:

```bash
cd ~/code/ai-engineer-roadmap/attention_transformers
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
  pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
  ```

- Only one environment can be active in a terminal at a time. Before
  activating a different one, run `deactivate` first.

- Multiple environments can exist on disk at the same time without
  conflicting. You choose which one is active.

- Activation is per terminal. A new terminal starts with the system Python,
  so activate the environment again.

- Sharing one environment between folders is possible, but all folders then
  share the same installed packages and versions. If folders need different
  dependency versions, give each folder its own `.venv/`.

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

## Optional: recording dependencies

To record the exact package versions used by this environment:

```bash
cd ~/code/ai-engineer-roadmap/attention_transformers
source .venv/bin/activate
pip freeze > requirements.txt
```

To recreate the same packages in another environment:

```bash
pip install -r requirements.txt
```
