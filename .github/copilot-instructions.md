# GitHub Copilot Instructions for This Repository

> Save this file as **`.github/copilot-instructions.md`** at the repo root (or inside `.github/`). Copilot Chat and the Copilot Coding Agent will load and follow these instructions.

---

## 0) Repository Facts (fill these in)

* **Project name:** AI-Lab
* **Primary stack:** Python
* **Package manager:** UV
* **CI:** GitHub Actions

---

## 1) How I want Copilot to work here

1. **Start with a plan.** Before writing code, generate a brief **task plan**:

   * Context summary (1–2 lines)
   * **TODO checklist** of concrete steps
   * Affected files/modules
   * Acceptance criteria / test cases
2. **Ask if unsure.** If requirements are ambiguous, ask up to 3 clarifying questions.
3. **Prefer minimal, composable changes** over large refactors unless requested.
4. **Follow repo standards** (style, lint, tests, security, performance) defined below.
5. **Cite references** (files, lines) in PR descriptions and replies when relevant.

> When I say *“do X”*, produce the plan + checklist first. After I confirm (or after 1 minute with no reply), implement.

---

## 2) Code style & quality

* **Formatting:** Use the configured formatter (see repo facts). Do not change formatters without approval.
* **Linting:** Code must pass linters with zero new warnings. If you must disable a rule, explain why inline.
* **Naming:** Descriptive, consistent, and idiomatic for the language. Avoid abbreviations unless widely standard.
* **Comments & docs:**

  * Add docstrings for public APIs.
  * Explain non-obvious decisions and tradeoffs.
  * Update the README or relevant docs when behavior or setup changes.
* **Types:** Use/strengthen static types where available (TypeScript, mypy, etc.). Prefer explicit types on public boundaries.


---

## 4) Security & privacy

* **Never hardcode secrets**. Use environment variables, secret managers, or GitHub Actions secrets.
* **Input validation** on all external inputs (requests, forms, webhooks). Sanitize user content.
* **Dependencies:** Prefer maintained libraries; avoid deprecated/outdated packages. For new deps, justify in PR description.
* **Auth & authz:** Follow the project’s auth patterns; least privilege.
* **PII:** Avoid storing sensitive data unless explicitly required. Document retention and masking.

---

## 5) Performance & accessibility

* **Performance:**

  * Avoid N+1 queries, unnecessary JSON parsing/stringifying, and repeated heavy computations.
  * For web: prefer lazy-loading, code-splitting, memoization, and efficient list rendering.
* **Accessibility (web):**

  * Meet **WCAG 2.1 AA** where applicable.
  * Proper semantic HTML, focus management, labels, and keyboard navigation.


**PR checklist (auto-include by Copilot):**

* [ ] Plan & TODOs included
* [ ] Acceptance criteria listed
* [ ] Tests updated/added
* [ ] Docs updated
* [ ] Security considerations noted
* [ ] Performance / a11y notes (if applicable)

---

## 7) Project structure & patterns

* Follow the existing project structure; do not introduce parallel patterns without explanation.
* Prefer pure functions, small components, and dependency injection where helpful.
* Isolate I/O (network, file system) from business logic for testability.
* For APIs: document endpoints, request/response shapes, and error formats.

---

## 8) Issue → Plan → Implement loop (what to produce)

When assigned an issue or given a request, Copilot should:

1. **Restate** the request in 1–2 sentences.
2. Produce a **task plan** (bulleted) and a **TODO checklist**.
3. Identify **files to change** and any **new files**.
4. Propose **acceptance criteria** and test cases.
5. After confirmation, implement changes and open a PR with the **PR checklist** filled out.

**Example task plan (template):**

```
Context: Add CSV export to Orders table in admin dashboard.

TODO
- [ ] Add server endpoint `GET /api/orders/export?format=csv`
- [ ] Gate by role: admin only
- [ ] Reuse existing OrderQuery; stream CSV to response
- [ ] Add "Export CSV" button to Orders page; show spinner & error toast
- [ ] Tests: service unit tests, endpoint integration test
- [ ] Docs: README > Admin features > Export

Files
- api/orders/export.ts
- services/orders/csv.ts (new)
- ui/admin/orders/Toolbar.tsx

Acceptance criteria
- Export includes headers and all filterable fields
- Role enforcement tested; 403 for non-admin
- CSV downloads in < 5s for 10k rows
```

---

## 10) Don’ts

* Don’t commit secrets, large binaries, or generated files.
* Don’t disable linters broadly; isolate and justify suppressions.
* Don’t introduce breaking changes without migration notes.
* Don’t add new dependencies without justification.

---

## 12) Glossary / domain context (optional)

List project-specific domain terms, acronyms, and meanings so Copilot learns your language and business context.

* **Example:** "guest" = user without an account; "ticket" = salon appointment reservation

---

## 13) Maintenance

* Treat this file as a **living document**. Update when standards, tools, or workflows change.
* Keep concise and focused on rules Copilot should apply automatically.
