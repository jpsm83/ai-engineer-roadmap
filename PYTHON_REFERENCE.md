# Python Study Reference: `.venv`, `__pycache__`, and `__init__`

This document explains two generated folders and one special Python method:

- `.venv/` stores an isolated Python environment and its installed packages.
- `__pycache__/` stores compiled bytecode created automatically by Python.
- `__init__` is the special method Python calls to initialize a new object.

The two folders are generated locally and should not be committed to git.
`__init__` is part of Python's object model and is written by you.

This file lives at the repository root because it applies to every Python
folder in the repository. A typical layout with one environment per folder:

```
ai-engineer-roadmap/
├── .gitignore
├── README.md
├── PYTHON_REFERENCE.md       # this file
└── attention_transformers/
    ├── .venv/                # created with `python3 -m venv .venv`
    ├── __pycache__/          # created automatically by Python
    ├── README.md
    ├── encoder_decoder_attention.py
    ├── masked_self_attention.py
    └── self_attention.py
```

Each future Python folder follows the same pattern and gets its own `.venv/`
and `__pycache__/` as needed.

---

# Part 1: `.venv`

## 1.1 The problem it solves

Python projects depend on third-party packages such as PyTorch, NumPy, Flask,
or pandas. Different projects often need different versions of the same
package.

If every package were installed into one global location:

- Project A requiring `torch==2.15` and Project B requiring `torch==2.20`
  would conflict.
- Upgrading a package for one project could break another.
- It would be difficult to know which packages belong to which project.
- System tools written in Python could break if you change their packages.
- Installing packages might require administrator permissions (`sudo`).

A **virtual environment** solves this by giving each project its own private
package folder.

Analogy: instead of putting every tool in one shared garage, each project gets
its own toolbox. The system Python stays untouched.

## 1.2 What `.venv` is

`.venv` is a normal directory containing a **virtual environment**: an isolated
Python setup with:

- a Python executable (usually a symbolic link to the system Python),
- its own `pip`,
- its own installed packages,
- a configuration file describing the environment.

The name `.venv` is only a convention. Common names are `.venv`, `venv`, `env`,
and `ENV`. Tools and editors recognize these names automatically, which is why
`.venv` is a good default. The leading dot makes it hidden on Linux and macOS
(`ls -a` shows it).

## 1.3 What is inside `.venv`

A typical Linux environment looks like this:

```
.venv/
├── bin/
│   ├── activate          # shell script used to activate the environment
│   ├── python -> ...     # symbolic link to the base Python interpreter
│   ├── python3 -> ...
│   ├── pip               # pip for this environment
│   └── ...               # other installed command-line tools
├── include/              # C headers for compiled packages
├── lib/
│   └── python3.14/
│       └── site-packages/  # installed third-party packages live here
├── lib64 -> lib
└── pyvenv.cfg            # environment configuration
```

The most important file is `pyvenv.cfg`. In this project it contains:

```ini
home = /usr/bin
include-system-site-packages = false
version = 3.14.4
executable = /usr/bin/python3.14
command = /usr/bin/python3 -m venv /home/.../attention_transformers/.venv
```

It records which base Python the environment was created from and whether
system-wide packages are visible. Here `include-system-site-packages = false`
means the environment is isolated from globally installed packages.

## 1.4 Why virtual environments exist

Benefits:

- **Isolation:** packages installed in the environment do not affect the
  system Python or other projects.
- **Independent versions:** each project can use different package versions.
- **Reproducibility:** `pip freeze > requirements.txt` records versions so
  another machine can recreate the same setup.
- **Safety:** no `sudo` is required to install packages.
- **Easy cleanup:** deleting the environment removes all its packages.
- **Experimentation:** you can break and recreate an environment without
  damaging your system.
- **Clear ownership:** dependencies in `.venv` belong to that project folder.

## 1.5 How to create an environment

From the folder that contains the project code:

```bash
cd ~/code/ai-engineer-roadmap/attention_transformers
python3 -m venv .venv
```

Explanation:

- `python3` runs the system Python.
- `-m venv` runs Python's built-in `venv` module.
- `.venv` is the destination folder. Python creates it for you.

Create one environment per folder that has independent dependencies. Do not
copy or move an existing environment; create a new one instead (see 1.11).

## 1.6 How to activate, verify, and deactivate

### Activate

```bash
source .venv/bin/activate
```

Activation is a shell convenience. It changes your terminal so that:

- `python` means `.venv/bin/python`,
- `pip` means `.venv/bin/pip`,
- the prompt usually shows `(.venv)`.

On Windows (PowerShell) the command is:

```powershell
.venv\Scripts\Activate.ps1
```

### Verify

```bash
which python
python --version
python -c "import sys; print(sys.prefix)"
```

`which python` should print a path inside `.venv/bin/`. `sys.prefix` should be
the `.venv` path. Another reliable check inside Python is:

```python
import sys
sys.prefix != sys.base_prefix   # True when a virtual environment is active
```

### Deactivate

```bash
deactivate
```

This restores the previous `PATH` and removes the `(.venv)` prompt. It does not
delete the environment and does not uninstall anything.

Closing the terminal also ends activation for that terminal. Activation is
**per terminal**: a newly opened terminal uses the system Python until you
activate again.

### Run without activating

Activation is optional. You can call the environment's Python directly:

```bash
.venv/bin/python self_attention.py
.venv/bin/pip install some-package
```

This is useful in scripts and tools, but activation is more convenient for
interactive work.

## 1.7 How to use an environment

With the environment activated:

```bash
pip install torch
pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
pip install numpy
pip list                    # show installed packages
pip show torch              # details about one package
pip freeze                  # exact versions, useful for requirements.txt
python self_attention.py
```

Packages are installed into:

```
.venv/lib/python3.14/site-packages/
```

When you activate the environment, that folder is added to Python's import
path, so `import torch` finds the package there.

## 1.8 What `.venv` does not do

A virtual environment is often confused with other tools. It does **not**:

- manage dependency versions by itself (it only isolates them),
- automatically record which packages you installed,
- automatically activate in new terminals,
- automatically activate in your editor or IDE,
- contain your project source code,
- make code portable to another machine by copying the folder,
- replace git, Docker, or a package manager.

You still use `pip` to install packages and `requirements.txt` (or
`pyproject.toml`) to record them.

## 1.9 How it works internally

When Python starts from `.venv/bin/python`, it looks for `pyvenv.cfg` near the
executable. If found, Python treats that directory as its environment prefix
and uses `.venv/lib/.../site-packages` for third-party packages.

You can inspect this inside Python:

```python
import sys
print(sys.prefix)       # the active environment
print(sys.base_prefix)  # the underlying system Python
print(sys.path)         # where Python searches for modules
```

The `activate` script itself does not change the Python interpreter. It only
changes environment variables in your shell (`PATH`, `VIRTUAL_ENV`, prompt).
This is why the environment can be bypassed by calling `.venv/bin/python`
directly.

## 1.10 Multiple environments in one repository

Multiple environments can exist at the same time without conflict:

```
ai-engineer-roadmap/
├── attention_transformers/
│   └── .venv/
└── another-project/
    └── .venv/
```

Only one can be active in a terminal at a time. To switch:

```bash
deactivate
cd ~/code/ai-engineer-roadmap/another-project
source .venv/bin/activate
```

Different terminals can have different environments active independently.

If all folders share exactly the same dependencies, a single root `.venv` is
valid, but each folder having its own `.venv` avoids version conflicts and
makes ownership clearer.

## 1.11 Moving or copying an environment

Do **not** move or rename a virtual environment. Its `activate` script and
`pip` script contain absolute paths from creation time, for example:

```
/home/.../attention_transformers/.venv/bin/python3
```

After moving the folder, those paths are wrong. The reliable fix is to delete
and recreate:

```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If no `requirements.txt` exists, reinstall the packages you need, for example:

```bash
pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
```

To recreate an environment on another machine, copy the project source and
`requirements.txt`, create a fresh `.venv`, and install the requirements.

## 1.12 Common mistakes

- **Installing without activation.** `pip install torch` then installs into the
  system/user Python, not the project. Check with `which pip`.
- **Forgetting to reactivate.** Every new terminal starts with system Python.
- **Using `sudo pip`.** Avoid it; it can modify system packages.
- **Committing `.venv`.** It is large, machine-specific, and not portable.
  Keep it in `.gitignore`.
- **Moving the folder.** Recreate it instead.
- **Assuming an editor uses the environment.** In VS Code, select the
  interpreter at `.venv/bin/python`.
- **Sharing one environment across unrelated projects.** Works until their
  dependency versions differ.
- **Deleting `.venv` and thinking code is lost.** Only packages are removed;
  source files are not inside `.venv`.

## 1.13 Relationship to other tools

- `pip` installs packages into the active environment.
- `requirements.txt` records package versions for recreation.
- `pyproject.toml` is the modern project metadata and dependency format.
- `venv` is built into Python and is sufficient for most learning projects.
- `conda`, `poetry`, `pipenv`, and `uv` are alternative environment and
  dependency managers with additional features. You do not need them to run
  this example.

## 1.14 Command cheat sheet

```bash
# Create
python3 -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Verify
which python
python -c "import sys; print(sys.prefix)"

# Install and inspect
pip install torch
pip list
pip show torch
pip freeze > requirements.txt

# Run
python self_attention.py

# Leave
deactivate

# Recreate from recorded versions
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

# Part 2: `__pycache__`

## 2.1 What it is

`__pycache__` is a folder that Python creates automatically when it imports
Python modules. It contains compiled **bytecode** files with the `.pyc`
extension.

In this project, `__pycache__/self_attention.cpython-314.pyc` was created when
the file was compiled with `python -m py_compile`.

It is not source code and it is not specific to virtual environments. It can
appear in any project that imports Python modules.

## 2.2 Why it exists

Python normally works in two stages:

1. **Compile:** source code (`.py`) is translated into bytecode, a lower-level
   representation executed by the Python Virtual Machine.
2. **Execute:** the bytecode runs.

Compiling takes time. Python caches the result in `__pycache__` so that the
next import can skip compilation and load the bytecode faster.

Benefits:

- faster imports and startup,
- less repeated work across program runs,
- no effect on program behavior.

This is similar to how a compiler for other languages produces object files
that are reused instead of recompiling everything each time.

## 2.3 What is inside and how files are named

Example:

```
__pycache__/
└── self_attention.cpython-314.pyc
```

The name encodes:

- the module name: `self_attention`,
- the Python implementation: `cpython` (standard Python),
- the Python version: `314` means Python 3.14,
- the extension: `.pyc`.

Version and implementation information prevent Python 3.14 from accidentally
loading bytecode made by a different Python version or implementation.

The `.pyc` file contains a header (magic number, flags, source timestamp/size
or hash) followed by the compiled code object. It is not meant to be read or
edited by humans.

## 2.4 When `__pycache__` is created

It is created when Python imports a module from a `.py` file and decides the
cached bytecode is missing or outdated.

Important details:

- Imported modules are cached. For example, if `main.py` imports `helper.py`,
  Python may create `__pycache__/helper.cpython-314.pyc`.
- The main script you run directly (for example `python main.py`) is usually
  **not** cached, because it is executed as the main program rather than
  imported.
- Tools such as `py_compile` and `compileall` can explicitly create `.pyc`
  files for any source file.
- Running a program that imports no local modules may not create
  `__pycache__` at all.

## 2.5 Is it safe to delete?

Yes. Deleting `__pycache__` is completely safe:

```bash
rm -rf __pycache__
```

Python recreates it when needed. Deleting it:

- does not delete your code,
- does not uninstall packages,
- does not change program behavior,
- may make the next import slightly slower.

It is common to delete it when cleaning a repository.

## 2.6 How Python decides a `.pyc` is still valid

Each `.pyc` header records information about the source file, such as its
modification time and size, or a source hash. On import, Python compares that
information with the current `.py` file.

- If they match, the cached bytecode is used.
- If the source changed, Python recompiles and rewrites the `.pyc`.
- If the `.pyc` was made by a different Python version, it is ignored.

This prevents most stale-bytecode problems. If you ever suspect stale cache
issues (rare), deleting `__pycache__` is a safe first step.

## 2.7 Should it be committed to git?

No. Add it to `.gitignore`:

```gitignore
__pycache__/
*.py[cod]
```

Reasons:

- it is generated automatically,
- it is machine- and Python-version-specific,
- it creates noisy diffs,
- it is not needed to distribute the source code.

This repository's root `.gitignore` already ignores `__pycache__/` and
`*.py[cod]`.

## 2.8 How to disable or relocate bytecode caching

Disable writing bytecode for one run:

```bash
python -B self_attention.py
```

Disable it for the current shell session:

```bash
export PYTHONDONTWRITEBYTECODE=1
```

Inside Python:

```python
import sys
sys.dont_write_bytecode = True
```

Store caches somewhere else instead of alongside the source:

```bash
export PYTHONPYCACHEPREFIX=~/.cache/python
```

Precompile files deliberately:

```bash
python -m compileall .
```

Caching is an optimization. Disabling it is fine for small scripts; keeping
it is usually beneficial.

## 2.9 Common misconceptions

- **"`__pycache__` contains my source code."** No, it contains compiled
  bytecode derived from your source.
- **"I must edit or keep `.pyc` files."** No. Edit the `.py` file; Python
  regenerates the cache.
- **"Deleting `__pycache__` breaks the project."** No. It is safe to delete.
- **"`.pyc` files are portable across Python versions."** No. They are tied to
  the Python version and implementation in their filename.
- **"`__pycache__` is part of `.venv`."** No. It belongs to the folder
  containing the imported source files and is independent of the environment.
- **"A `.pyc` file is secure because it is compiled."** No. Bytecode is not an
  encryption or security mechanism. Only run code you trust.

## 2.10 `__pycache__` cheat sheet

```bash
# Delete safely (regenerated later)
rm -rf __pycache__

# Disable bytecode writing for one run
python -B self_attention.py

# Disable for the shell session
export PYTHONDONTWRITEBYTECODE=1

# Put caches elsewhere
export PYTHONPYCACHEPREFIX=~/.cache/python

# Precompile all modules in the current directory
python -m compileall .

# Ignore in git (already present in this repo)
__pycache__/
*.py[cod]
```

---

# Part 3: `__init__`

## 3.1 What `__init__` is

`__init__` is a **special method** in Python. It is called automatically when
you create a new object from a class.

The name has two leading underscores and two trailing underscores:

```
__init__
```

Names with this shape are often called **dunder** names ("double underscore")
or **magic methods**. They are part of Python's object model: Python looks for
these exact names to perform built-in operations.

`__init__` is therefore not just a naming style. It is the standard hook Python
uses to initialize a newly created object. This is why it is always spelled
exactly `__init__`, in lowercase.

Minimal example:

```python
class Dog:
    def __init__(self, name, age=0):
        self.name = name
        self.age = age

dog = Dog("Rex", 3)   # __init__ runs automatically here

print(dog.name)       # Rex
print(dog.age)        # 3
```

`Dog("Rex", 3)` does not call a method named `Dog`. Python creates the object
and then calls `__init__` on it.

## 3.2 Why `__init__` exists

`__init__` gives an object its initial state. It is used to:

- store constructor arguments on the object,
- create attributes the object needs,
- create sub-objects such as layers or helper objects,
- validate inputs and raise errors early,
- ensure the object is usable immediately after creation.

Without `__init__`, every new object would start empty, and every caller would
have to set its attributes manually.

## 3.3 How an object is created

When you write:

```python
obj = MyClass(arg1, arg2)
```

Python roughly does this:

1. Create a new instance using `__new__`.
2. Call `__init__` on that instance with `arg1` and `arg2`.
3. Return the initialized instance and assign it to `obj`.

`__init__` is an **initializer**, not the method that allocates memory. The
method that creates the raw instance is `__new__`, which you rarely need to
override.

`__init__` must return `None`. If it returns anything else, Python raises a
`TypeError`.

You can call `__init__` manually:

```python
dog = Dog("Rex")
Dog.__init__(dog, "Max", 5)   # reinitializes the existing object
```

This is unusual. Normally you let Python call `__init__` for you.

## 3.4 What `self` means

Every instance method receives the instance as its first argument. By
convention that argument is named `self`:

```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
```

`self` is not a Python keyword. It is a conventional name for the first
parameter. Python passes the object automatically:

```python
c = Counter()      # calls Counter.__init__(c)
c.increment()      # calls Counter.increment(c)
```

Assigning `self.count = 0` creates an **instance attribute**: a value that
belongs to that particular object. Another `Counter()` gets its own separate
`count`.

## 3.5 Default arguments

`__init__` supports normal Python default arguments:

```python
class SelfAttention:
    def __init__(self, d_model=2, row_dim=0, col_dim=1):
        self.d_model = d_model
        self.row_dim = row_dim
        self.col_dim = col_dim
```

This allows both of these:

```python
a = SelfAttention()             # uses the defaults
b = SelfAttention(d_model=512)  # overrides only d_model
```

Be careful with **mutable defaults**:

```python
# Wrong: the same list is shared by every instance
class Bad:
    def __init__(self, items=[]):
        self.items = items
```

Use `None` as the default and create a fresh object inside:

```python
# Correct
class Good:
    def __init__(self, items=None):
        self.items = [] if items is None else items
```

Lists, dictionaries, and sets are mutable. Integers, strings, tuples, and
`None` are safe defaults.

## 3.6 Inheritance and `super().__init__()`

When a class inherits from another class, the subclass often needs to run the
parent's initializer:

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)   # run Animal.__init__
        self.breed = breed
```

`super()` refers to the parent class. Calling `super().__init__()` lets the
parent set up its own state before the child adds more.

This is essential in the PyTorch classes in this repository:

```python
class SelfAttention(nn.Module):
    def __init__(self, d_model=2, row_dim=0, col_dim=1):
        super().__init__()   # initialize nn.Module internals
        self.W_q = nn.Linear(in_features=d_model, out_features=d_model, bias=False)
        self.W_k = nn.Linear(in_features=d_model, out_features=d_model, bias=False)
        self.W_v = nn.Linear(in_features=d_model, out_features=d_model, bias=False)
        self.row_dim = row_dim
        self.col_dim = col_dim
```

`nn.Module.__init__()` prepares PyTorch's internal bookkeeping. Without it,
assigning layers such as `self.W_q = nn.Linear(...)` can fail, and PyTorch will
not register the parameters correctly.

Call `super().__init__()` **before** creating or assigning PyTorch layers.

## 3.7 `__init__` is not `forward`

In PyTorch, these two methods have completely different jobs:

| Method | When it runs | Purpose |
|---|---|---|
| `__init__` | once, when the model is created | configure the object and create layers |
| `forward` | every time you call the model | perform the computation |

Example:

```python
model = SelfAttention(d_model=2)   # __init__ runs
output = model(encodings_matrix)   # forward runs
```

The second line does not call `forward` directly. `nn.Module` defines
`__call__`, so `model(...)` goes through `nn.Module.__call__`, which then calls
your `forward(...)`.

Related special methods:

- `__new__` creates the raw instance.
- `__init__` initializes the instance.
- `__call__` makes an object callable with `obj(...)`.
- `forward` is the PyTorch-specific computation hook.

## 3.8 `__init__` is not `__init__.py`

These names look similar but have nothing to do with each other:

| Name | What it is | Where it appears |
|---|---|---|
| `__init__` | special method that initializes an object | inside a class |
| `__init__.py` | file that marks a directory as a Python package | inside a directory |

`__init__.py` is executed when the package is imported. It is often empty. It
is a file, not a method. Do not confuse the two.

Modern Python also supports namespace packages without `__init__.py`, but
regular packages traditionally include it.

## 3.9 Other common dunder methods

You do not need to implement most of these, but you will see them in Python
code and documentation:

| Method | Called when |
|---|---|
| `__init__` | an object is created |
| `__repr__` | `repr(obj)` is used, often for debugging |
| `__str__` | `print(obj)` or `str(obj)` is used |
| `__len__` | `len(obj)` is used |
| `__eq__` | `obj1 == obj2` is used |
| `__getitem__` | `obj[key]` is used |
| `__iter__` | you iterate over the object |
| `__call__` | you use `obj(...)` |
| `__enter__` / `__exit__` | `with obj:` is used |

The double-underscore names are reserved for these language-level hooks. Do
not invent your own `__myThing__` names and expect Python to call them; only
documented special methods have language-defined behavior.

Names such as `__private` with no trailing underscores are different: Python
applies name mangling to them inside classes. They are not special methods.

## 3.10 Common mistakes

- **Forgetting `self`.** `def __init__(d_model=2):` is wrong; the first
  parameter must receive the instance.
- **Forgetting `super().__init__()`** in a subclass, especially an `nn.Module`
  subclass.
- **Returning a value from `__init__`.** It must return `None`. A bare
  `return` is fine; returning a value raises `TypeError`.
- **Using mutable defaults.** Use `None` and create the list/dict inside.
- **Calling `__init__` manually** when you should create a new object.
- **Confusing `__init__` with `__init__.py`.**
- **Setting class attributes by mistake.** Assigning `self.x = ...` creates an
  instance attribute; defining `x = ...` in the class body creates one shared
  class attribute.

## 3.11 How it appears in this project

Every attention class follows the same pattern:

```python
class MaskedSelfAttention(nn.Module):
    def __init__(self, d_model=2, row_dim=0, col_dim=1):
        super().__init__()

        self.W_q = nn.Linear(in_features=d_model, out_features=d_model, bias=False)
        self.W_k = nn.Linear(in_features=d_model, out_features=d_model, bias=False)
        self.W_v = nn.Linear(in_features=d_model, out_features=d_model, bias=False)

        self.row_dim = row_dim
        self.col_dim = col_dim
```

The call:

```python
maskedSelfAttention = MaskedSelfAttention(
    d_model=2,
    row_dim=0,
    col_dim=1,
)
```

does four useful things:

1. Creates a new `MaskedSelfAttention` object.
2. Runs `nn.Module.__init__()` through `super()`.
3. Creates three linear layers and stores them on the object.
4. Stores `row_dim` and `col_dim` for use in `forward()`.

Then, when you call:

```python
maskedSelfAttention(encodings_matrix, mask)
```

PyTorch invokes `forward()`, not `__init__()`.

## 3.12 `__init__` cheat sheet

```python
class Example:
    def __init__(self, value, optional=None):
        super().__init__()          # run parent initializer if inheriting
        self.value = value          # instance attribute
        self.optional = optional

obj = Example(10)                   # __init__ runs automatically
print(obj.value)                    # 10
```

Key points:

- `__init__` runs once when an instance is created.
- It initializes the instance; it does not create it.
- `self` refers to the instance being initialized.
- It must return `None`.
- Call `super().__init__()` when subclassing, especially with `nn.Module`.
- `__init__` configures the object; `forward` performs computation.
- `__init__` is not the same thing as `__init__.py`.

---

# Part 4: How `.venv` and `__pycache__` relate

| | `.venv/` | `__pycache__/` |
|---|---|---|
| Created by | you, with `python3 -m venv .venv` | Python, automatically |
| Purpose | isolate Python and installed packages | speed up imports with cached bytecode |
| Contains | interpreter links, `pip`, `site-packages`, config | compiled `.pyc` bytecode |
| Needed to run code | not strictly, but needed for isolated dependencies | no |
| Safe to delete | yes; recreate and reinstall packages | yes; regenerated automatically |
| Commit to git | never | never |
| Version-specific | yes, tied to the base Python | yes, name includes Python version |
| Portable | no, recreate instead of moving | not needed; regenerated |

`__init__` is different from both folders: it is source code that you write
inside a class. It is not generated, not disposable, and not ignored by git.

Study summary:

- `.venv` controls **which Python and which packages** your project uses.
- `__pycache__` makes **imports faster** and has nothing to do with dependency
  management.
- Both are disposable generated state. Your real project is the source code
  plus the files that describe dependencies, such as `requirements.txt` or
  `pyproject.toml`.
