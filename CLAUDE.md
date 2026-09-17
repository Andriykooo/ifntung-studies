# CLAUDE.md — Studies Repository

## Project Overview

Studies repository for **Бойчук Андрій Анатолійович** at ІФНТУНГ (Івано-Франківський національний технічний університет нафти і газу).
- **Year of admission:** 2026 (1st year)
- **Group:** КН-26-1
- **Department:** Кафедра комп'ютерних систем і мереж
- **Specialty:** F3 — Комп'ютерні науки
- **Faculty:** Факультет інформаційних технологій

## Repository Structure

```
Year 1/
  Іноземна мова/                         # Foreign Language
  Програмування/                         # Programming
  Вища математика/                       # Higher Mathematics
  Командна комунікація в ІТ-проєктах/    # Team Communication in IT Projects
  Дискретна математика/                  # Discrete Mathematics
  Технології web-графіки/                # Web Graphics Technologies
  Основи академічного письма/            # Fundamentals of Academic Writing
Semester reports/
```

Each subject folder holds lab/practical assignments, generated reports and reference materials for that course.

## Subjects and Lecturers (Year 1)

| Subject | Lecturer |
|---|---|
| Іноземна мова | Дребот Яна Романівна |
| Програмування | Пашковський Богдан Васильович |
| Вища математика | Григорчук Галина Василівна |
| Командна комунікація в ІТ-проєктах | Кропивницький Д.Р. |
| Дискретна математика | Мойсеєнко Олена Володимирівна |
| Технології web-графіки | Корнута Олена Володимирівна |
| Основи академічного письма | Судук Ірина Ігорівна |

## Language

- Communicate in the same language the user writes in (Ukrainian or English).
- Report language depends on the subject requirements (Ukrainian by default; English for Іноземна мова).

## Document Generation (.docx)

Lab reports are generated programmatically using Node.js + the `docx` npm package.

### Workflow
1. Scripts live in the session scratchpad directory (or `/tmp/docx-work/` if no scratchpad is available).
2. Install dependencies: `npm init -y && npm install docx` in the script directory. The repo also keeps a manifest at `.claude/skills/package.json` with `docx` and `pptxgenjs`.
3. Each lab has its own script: `create1.js`, `create2.js`, etc.
4. Output goes directly to the subject folder (e.g., `Year 1/Програмування/Звіт_N.docx`).
5. Run with `node createN.js` from the script directory.

### Formatting Standard (default, ДСТУ 3008)
Unless a subject specifies otherwise, reports follow these rules:
- **Page:** A4 (width: 11906 DXA, height: 16838 DXA)
- **Margins:** top=1134, bottom=1134, left=1701, right=851 (DXA)
- **Font:** Times New Roman, 14pt (size=28 in docx half-points)
- **Line spacing:** 1.5 (line: 360, lineRule: 'auto')
- **Paragraph indent (first line):** 709 DXA (~1.25 cm)
- **Body text alignment:** justified
- **Headings:** bold, same font/size
- **Tables:** bordered (SINGLE, size 4), header row with light blue shading (#BDD7EE)
- **Page numbers:** centered in footer, same font

If a lecturer provides their own template or requirements (in the subject folder), those take precedence.

### Title Page Data
- **University:** Івано-Франківський національний технічний університет нафти і газу
- **Faculty:** Факультет інформаційних технологій
- **Department:** Кафедра комп'ютерних систем і мереж
- **Student:** студент групи КН-26-1 Бойчук Андрій Анатолійович
- **Lecturer:** from the table above, per subject
- **City/Year:** Івано-Франківськ, current year

### Document Author
Every generated `.docx` MUST include document metadata:
```js
new Document({
  creator: "Andrii Boichuk",
  lastModifiedBy: "Andrii Boichuk",
  // ...
})
```

### Script Structure Pattern
Each `createN.js` follows this pattern:
```
imports → constants (page, font) → helper functions (body, centered, heading1, heading2, formula, emptyLine, buildTable) → content arrays (titlePage, bodyHeader, introduction, tasks, protocol, sections, conclusions) → Document assembly (2 sections: title page + body with footer) → Packer.toBuffer → fs.writeFileSync
```

Reference previous `createN.js` scripts when building new ones to maintain consistency.

## Git Workflow

### Remotes
- `origin` — https://github.com/Andriykooo/phd-studies (this repository)
- `upstream` — the original repository this one was cloned from; not used for day-to-day work

### Branches
- **Main branch:** `main`
- **Feature branches:** English, descriptive, kebab-case
  - Format: `subject-name/lab-N` or `subject-name/description`
  - Subject slugs: `foreign-language`, `programming`, `higher-math`, `team-communication`, `discrete-math`, `web-graphics`, `academic-writing`
  - Examples: `programming/lab-1`, `discrete-math/lab-4`, `web-graphics/project`
- Always create a PR to merge into `main`.

### Commits
Use **Conventional Commits** format:
```
feat(scope): description
fix(scope): description
```
- Scope = subject slug from the list above (or `readme`, `claude`, `skills` for repo housekeeping)
- Description in English, concise

## Working Style

### Step-by-Step Approach for Large Tasks
When a lab or task is large (especially document generation with computations):
- **Break the work into numbered steps** using the todo list.
- **Complete ONE step at a time**, verify it works, then move to the next.
- **Do NOT output the entire file at once** — use incremental edits.
- This prevents exceeding token limits and makes progress trackable.
- After each step, run the script to verify it produces valid output.

### When "покроково" / "step by step" is requested
This means: literally one logical unit of work per response. Do not combine multiple sections or computation blocks. Show progress, verify, then proceed to the next piece.

## Course Materials

Lecture notes, assignment PDFs and templates live inside the corresponding subject folder. When a lab depends on formulas or examples from lectures, cross-reference computed values against the lecture examples to verify correctness.

## Git Staging

Always run `git add` for all new or modified files after creating/changing them. Don't let new files sit untracked.

## Git Commits

**Do NOT commit automatically.** Only create a commit when the user explicitly asks (e.g., "закомітай", "зроби коміт", "commit this").

## Things to Avoid

- Do not generate the entire large file in one go — incremental edits only.
- Do not ask unnecessary clarifying questions when the task is clear.
- Do not add `.DS_Store` or IDE files to commits.
- Do not push to remote without explicit user request.
- Do not commit unless explicitly asked.
