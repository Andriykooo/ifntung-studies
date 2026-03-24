# CLAUDE.md — PhD Studies Repository

## Project Overview

PhD studies repository for **Білозор Дмитро Олександрович** at ЧДТУ (Черкаський державний технологічний університет).
- **Group:** A-F5-25
- **Department:** F5 — Кібербезпека та захист інформації
- **Specialty:** 125 — Кібербезпека
- **Faculty:** Факультет інформаційних технологій та кібербезпеки

## Repository Structure

```
Year 1/
  Етичний хакінг/                          # Ethical Hacking
  Мультиагентні системи/                   # Multi-Agent Systems
  Природно-надійні системи кібербезпеки/   # Cyber Security Systems
  Сучасні пошукові інформаційні системи…/  # Modern Search Systems
  Теорія і практика побудови ПВП/          # PRNG Theory & Practice
Semester reports/
```

## Language

- Communicate in the same language the user writes in (Ukrainian or English).
- Report language depends on the subject requirements.

## Document Generation (.docx)

Lab reports are generated programmatically using Node.js + the `docx` npm package.

### Workflow
1. Scripts live in `/tmp/docx-work/` (create with `mkdir -p /tmp/docx-work`).
2. Install dependencies: `cd /tmp/docx-work && npm init -y && npm install docx`.
3. Each lab has its own script: `create1.js`, `create2.js`, etc.
4. Output goes directly to the subject folder (e.g., `Year 1/Теорія і практика…/Звіт_N.docx`).
5. Run with `node createN.js` from `/tmp/docx-work/`.

### Formatting Standard (ДСТУ-3008-95)
All reports MUST follow these formatting rules:
- **Page:** A4 (width: 11906 DXA, height: 16838 DXA)
- **Margins:** top=1134, bottom=1134, left=1701, right=851 (DXA)
- **Font:** Times New Roman, 14pt (size=28 in docx half-points)
- **Line spacing:** 1.5 (line: 360, lineRule: 'auto')
- **Paragraph indent (first line):** 709 DXA (~1.25 cm)
- **Body text alignment:** justified
- **Headings:** bold, same font/size
- **Tables:** bordered (SINGLE, size 4), header row with light blue shading (#BDD7EE)
- **Page numbers:** centered in footer, same font

### Document Author
Every generated `.docx` MUST include document metadata:
```js
new Document({
  creator: "Dmytro Bilozor",
  lastModifiedBy: "Dmytro Bilozor",
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

### Branches
- **Main branch:** `main`
- **Feature branches:** English, descriptive, kebab-case
  - Format: `subject-name/lab-N` or `subject-name/description`
  - Examples: `ethical-hacking/lab-1`, `prng-theory/lab-4`, `multi-agent/report-3`
- Always create a PR to merge into `main`.

### Commits
Use **Conventional Commits** format:
```
feat(scope): description
fix(scope): description
```
- Scope = short subject identifier (e.g., `ethical-hacking`, `prng`, `readme`)
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

## Lecture Materials

For PRNG course, formulas and examples come from `Лекції.pdf` in the subject folder. Always cross-reference computed values against lecture examples to verify correctness.

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
