# Study Docs — Rules & Template

Rules for every document in `study_docs_qa/`. The goal is a consistent, fast-reference Q&A format that can be reread quickly.

---

## 1. Files and placement

- Write each new `.md` file at the exact path the user names.
- The user owns the folder tree. Do not create folders under `study_docs_qa/`. If a named folder does not exist, stop and ask.
- If the user names `study_docs_qa/` with no subfolder, write the file in that directory (e.g., `study_docs_qa/core_ai_concepts.md`).
- One Markdown file per course, or one file per section when a course is split across parts.
- Filename: lowercase `snake_case` derived from the course or section title, ending in `.md`. Add a numeric prefix (`01_`, `02_`, …) only when the user asks for one.
- Existing layout (do not extend it on your own):
  - `study_docs_qa/` — `RULES.md` and standalone files such as `core_ai_concepts.md`
  - `00_ai_coding_crash_course/` — one file per course section
  - `01_orientation/` — one file per course
  - `02_llm_literacy/` — one file per course
  - `03_prompting_and_integration/` — one file per course
- Plain Markdown only: no front matter, no HTML, no generated TOCs.
- UTF-8, LF line endings, final newline.

## 2. Document Skeleton

Every course document follows this exact order:

1. **H1 title:** `# <Course Title> — Q&A`, or `# <Course Title> — <Section> — Q&A` for a file that covers one course section.
2. **Intro:** one or two lines.
   `Fast-reference notes for <Instructor>'s *<Course Title>* (<Publisher>).`
3. **Syllabus flow:** one bold line with the main topics of the course or section, separated by `→`, ending with a period.
   `**Topic 1 → Topic 2 → Topic 3.**`
4. `---`
5. **Body sections** following the course outline.
6. `## Quick Reference` table.
7. Optional `## Formulas` (math/code-heavy courses).
8. `---` then the italic closing note.

Closing note:

`*Study aid; for authoritative content, refer to the official <Publisher> course.*`

## 3. Headings

- Exactly one `#` (H1).
- `##` for course parts or weeks: `## Part 1 — Topic` or `## Week 1 — Topic`.
- `###` for subtopics only. Never use `####` or deeper.
- Follow the course's own order and grouping; do not invent sections.
- Sentence case, preserving proper nouns: `### Machine Learning`, not `### Machine learning`.
- Headings get no closing punctuation.
- Separate `---` after the intro, between major `##` parts/weeks, and before the Quick Reference and closing note.

## 4. Q&A Format

Every content block is a question/answer pair:

```markdown
**Q: Short, direct question?**
A: Direct answer in one to three sentences.
```

- The whole question line is bold, including `Q:`.
- `A:` is plain text and starts on the next line, with no blank line between Q and A.
- Leave one blank line between pairs.
- One question per pair. Merge questions that would produce overlapping answers.
- Start with the answer itself; never restate the question or write "The answer is…".
- Keep answers to 1–3 sentences. Exceed this only for multi-step math or required enumeration.
- Preserve every definition, formula, example, caveat, and nuance. Compress wording, not facts.
- Use a concrete example when it improves recall.
- No filler ("In summary", "It is important to note", "As we have seen").

### Inside answers

- **Bold** a key term the first time it is defined.
- Use inline code for identifiers, parameters, and formulas: `d_model`, `nn.Linear`, `softmax(QKᵀ / √d_k) · V`.
- Prefer prose. Use bullets only for ordered steps, enumerations, or lists of three or more items.
- Use short numbered steps for workflows: `(1) …, (2) …, (3) …`.
- Avoid nested lists.

## 5. Content Rules

- Source only from the course; never invent or add outside material.
- Paraphrase the course; do not copy transcript text verbatim.
- Cover every major concept in the course outline.
- Define jargon at first use; assume basic Python but not deep learning.
- Keep technical precision: e.g., masked positions use `-∞`, not `0`; scaling uses `√d_k`.
- Use the course's terminology consistently.
- If the course is week-based, use `Week`; otherwise use `Part`.
- No external links except the official course reference in the closing note.

## 6. Conventions

- Em dash with spaces in titles/headings: ` — `.
- Write `vs.` with a period.
- Use `e.g.,` and `i.e.,` with a comma.
- Oxford comma in lists.
- No emojis.
- No trailing whitespace; no double blank lines.
- Fenced code blocks use the correct language tag (`python`), are minimal, and are runnable skeletons.
- The Quick Reference table is exactly two columns:

```markdown
| Term | Meaning |
| --- | --- |
| Term | One-line definition |
```

- One term per row; meanings stay on one line.
- Italicize course titles and the closing note.

## 7. Length Targets

- Short course (1–2 hours): **1,500–2,200 words per file**.
- Multi-week course or one section of a split course: **up to ~2,500 words per file**.
- If over target, merge overlapping Q&As and tighten wording. Never drop required information.
- Revised drafts should be measurably shorter than the first draft (aim for 15–25% fewer words).

## 8. Quality Checklist

- [ ] File is at the path the user named; no new folder was created.
- [ ] Filename is lowercase `snake_case`.md; numeric prefix only if the user asked.
- [ ] One H1 in the form `# Course Title — Q&A`, or `# Course Title — Section — Q&A` for a split course.
- [ ] Intro and bold syllabus-flow line present.
- [ ] Structure mirrors the official course outline.
- [ ] Every item uses the `**Q: …**` / `A: …` format.
- [ ] Answers are 1–3 sentences and start with the answer.
- [ ] Key terms bolded; code/formulas in inline code.
- [ ] Quick Reference table present and two columns.
- [ ] Formulas section included when the course is math/code-heavy.
- [ ] Closing note present.
- [ ] No facts lost versus source notes.
- [ ] Word count within target.
- [ ] No emojis, filler, or double blank lines.

---

## 9. Template

Copy this skeleton for a new course document. For a split course, use one file per section and add the section to the H1: `# COURSE TITLE — SECTION — Q&A`.

```markdown
# COURSE TITLE — Q&A

Fast-reference notes for INSTRUCTOR's *COURSE TITLE* (PUBLISHER).
**TOPIC 1 → TOPIC 2 → TOPIC 3.**

---

## Part 1 — TOPIC 1

### SUBTOPIC

**Q: Question?**
A: Direct answer.

**Q: Question?**
A: Direct answer with `inline code` and a **key term**.

---

## Part 2 — TOPIC 2

### SUBTOPIC

**Q: Question?**
A: Direct answer.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Term | One-line definition |
| Term | One-line definition |

---

## Formulas

- **Name:** `formula`
- **Name:** `formula`

---

*Study aid; for authoritative content, refer to the official PUBLISHER course.*
```
