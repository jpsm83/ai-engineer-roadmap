# Comment a tutorial file

Use this on one file at a time. Do not open, edit, or comment any other file in the same run.

The file is a lesson. Someone is reading it to learn the idea, the order of the steps, and why each library call is there. Add comments that make that readable. Leave the code itself alone.

Target file: `<path the user gives you>`

## What you are doing

Read the whole file first. Find the lesson arc: what it sets up, what it demonstrates in the smallest form, and how later blocks reuse or replace that.

Then add comments so a developer who knows Python, but not this lesson, can follow:

- what this block is for
- what each function in the block is for
- what the library methods do here, in plain language
- what goes in, what comes out, and why the next block needs it

Do not teach the whole library. Teach only the call in front of you, at the moment it matters.

## Do not change the lesson

- Do not change logic, control flow, names, prompts, data, imports, or formatting of the executable code.
- Do not refactor, modernize, delete unused imports, or fix tutorial bugs. If something looks wrong, leave it. The lesson may be showing that shape on purpose.
- Do not add, remove, or rewrite docstrings. A docstring on a tool or function may be sent to a model. A comment above it is safe. A docstring edit is not.
- Do not uncomment examples, and do not delete commented-out lines. Those lines are part of the lesson.
- Use `#` comments only. Do not add module docstrings, function docstrings, or block strings.
- If a stray character makes the file invalid Python and it is clearly not part of the lesson, remove only that character and say so. Do not take that as permission to edit anything else.

After commenting, check that the file still parses. Do not run the lesson if running it calls an API, starts a server, or needs secrets.

## How to write the comments

Write the way you would explain the block to a teammate looking over your shoulder. Straight sentences. Name the thing, then say what it does here.

Put a short comment immediately above each logical block, not above every line. A block is a setup step, a function, a chain, a loop, a group of demo calls, or a class. Two to six lines is the normal size. One line is enough when the block is small. Go longer only when the flow is easy to misunderstand.

Inside a longer function, comment only the parts a reader cannot see from the code: a non-obvious choice, a value picked out of a larger response, or a step that exists so a later step can work.

When you explain a library call, cover the part that matters for this file:

- what it attaches, stores, or transforms
- what the important arguments mean in this lesson
- what it returns, when the return shape is easy to get wrong

Then connect it to the flow. Say what the previous step produced and what the next step consumes. If two names must match, say so the first time both appear.

The first time a lesson idea shows up, explain it. Later uses can be one line that points back, unless this use adds something new.

## What to notice in these files

These lessons are usually one script that runs from top to bottom, like a notebook pasted into a `.py` file. Comment that progression. Do not reorganize it.

- A decorator or schema often describes something to a model. Say what the model sees, and what actually runs later.
- A pipeline that passes one step into the next needs a comment on each stage: what it receives and what it hands on.
- A placeholder, memory key, or dict key is a slot. Say what fills it, and which other name it has to match.
- A hand-written loop that is later replaced by a library object is the same cycle. Say that, and say what the library object takes over.
- If a function or variable is defined again, the second definition replaces the first. Say what changed and why the lesson rebuilds it.
- Commented-out `print` calls are inspection points. One comment on the group is enough: what they would show. Leave them commented.
- A series of demo calls at the end of a section is there to exercise different paths. Say what each call is meant to show, especially when one call depends on the one before it.
- If two similar stores exist, such as notes for the current question and history from earlier turns, say the difference the first time both are in the same block.

## Algorithm or math files

When the lesson is the algorithm itself, comment the data flow. Above each step, say which tensor comes in, which tensor goes out, and why that step is there. The first time a learned weight, a mask, or a stack of heads appears, say what it does to that tensor. When later lines repeat the calculation in the open so each matrix can be printed, say that those lines are the same path and what the last result should match. Still do not change the math, the names, the tensor values, a docstring, or a tutorial bug. A `#` comment is the only addition.

## Shared helpers

When the file is imported by other lessons and is not itself a top-to-bottom script, comment what each function provides to those lessons, so the helper can be read without the lesson open. Say what the importer receives, and the first time say what the model sees versus what actually runs. Later functions that play the same role can be one line. Still do not change lesson code, docstrings, or tutorial bugs. A `#` comment is the only addition.

## Shape of a good comment

Explain the role, the data, and the reason. Do not restate the syntax.

Good:

```python
# bind_tools attaches the tool schemas to the model.
# On each call the model can either answer in text or request one of these tools.
model = ChatOpenAI(model=llm_model, temperature=0).bind_tools(tools)
```

```python
# format_to_openai_tool_messages turns (action, tool output) pairs into
# an assistant message plus a tool message. That is the shape the model expects
# on the next turn.
formatted_messages = format_to_openai_tool_messages([(result1[0], observation)])
```

Not useful:

```python
# Bind the tools.
model = ChatOpenAI(model=llm_model, temperature=0).bind_tools(tools)
```

```python
# Call format_to_openai_tool_messages on the result and the observation.
formatted_messages = format_to_openai_tool_messages([(result1[0], observation)])
```

The first pair tells a reader what the line is for and what moves forward. The second pair only renames the code.

## Order of work

1. Read the whole target file before editing.
2. Mark the sections in your head: setup, each new idea, the place an earlier idea gets reused, the final demo.
3. Add the comments in place. Keep every executable line as it is.
4. Read the file once more from top to bottom and check that a newcomer can answer, at each block: what is this, what does it return, and why is it here.
5. Confirm the file still parses.

## Done when

- The code behavior is unchanged.
- Each block has a comment a developer can learn from, without a wall of comments on obvious lines.
- Library calls are explained where they first matter, including the return shape when it affects the next line.
- The path through the file is visible: why the lesson does this step before the next one.
- Only the target file was edited.
