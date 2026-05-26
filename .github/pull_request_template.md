## What does this PR do?
<!-- One-line summary -->

## Task reference
<!-- e.g. Closes TASK-003 -->

## Checklist
- [ ] `uv run pytest` passes locally
- [ ] `uv run ruff check src/ tests/` passes
- [ ] `uv run mypy src/` passes
- [ ] No API keys hardcoded (`grep -r "AIza\|sk-ant\|sk-" src/` returns nothing)
- [ ] Spec updated if behavior changed
- [ ] New public functions have docstrings and type hints
