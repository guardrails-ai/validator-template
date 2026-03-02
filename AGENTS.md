## Objective

Build Guardrails Hub validators that follow the `validator-template` conventions and match production patterns from `guardrails-ai/toxic_language`.

## Non-Negotiable Rules

1. Keep the template repo structure and file names unless there is a strong reason to add files.
2. Always register validators with `@register_validator(name="<namespace>/<validator_name>", data_type="<type>")`.
3. Always return `PassResult(...)` or `FailResult(...)` from validator logic.
4. If validator behavior uses an LLM, always call the model via `litellm` (never direct provider SDKs).
5. For LLM-based validators, expose `model: Optional[str]` in `__init__`, and default it to the latest Claude Haiku model identifier available in LiteLLM at authoring time.
6. Include tests that prove both pass and fail paths.
7. Keep README in validator-card format with install and usage examples.
8. Run lint, typecheck, and tests before finalizing.
9. Every imported runtime package must be declared in `[project.dependencies]` (no undeclared transitive dependency reliance).
10. Every required credential/config key must be listed in `.env` (keys only, no values) and documented in README.
11. If extra install-time assets are required (tokenizers, model files, hub login), implement them in `validator/post-install.py` and document them in README.

## Required Repo Shape

Keep this minimum structure:

```text
.github/workflows/pr_qc.yml
Makefile
pyproject.toml
README.md
validator/__init__.py
validator/main.py
tests/test_validator.py
```

Optional:

```text
validator/post-install.py
.env
```

Only add runtime-serving files (`app.py`, inference specs, docker/deploy files) when remote inference hosting is explicitly required.

## Implementation Contract

### 1) `validator/main.py`

Implement one validator class:

- Inherit from `Validator`.
- Decorate with `register_validator`.
- `__init__` must forward config to `super().__init__(...)`.
- `validate(self, value, metadata)` must return `ValidationResult`.
- On fail, use `FailResult(error_message=..., fix_value=... optional, error_spans=... optional, metadata=metadata optional)`.
- On pass, use `PassResult(metadata=metadata optional)`.

If no metadata is required, accept metadata and ignore it safely.

### 2) LLM usage pattern (mandatory for LLM validators)

- Add dependency: `litellm` in `pyproject.toml`.
- Accept optional `model` init argument.
- Resolve default to latest Claude Haiku LiteLLM id at implementation time.
- Store chosen model in `self._model`.
- Route all completions through `litellm` (for example, `litellm.completion(...)` or `litellm.acompletion(...)`).
- Handle timeout/errors and return deterministic `FailResult` messages when model output is malformed.

Reference skeleton:

```python
from typing import Any, Callable, Dict, Optional
import litellm
from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)

DEFAULT_MODEL = "REPLACE_WITH_LATEST_CLAUDE_HAIKU_LITELLM_ID"


@register_validator(name="guardrails/example_validator", data_type="string")
class ExampleValidator(Validator):
    def __init__(
        self,
        model: Optional[str] = None,
        on_fail: Optional[Callable[..., Any]] = None,
        **kwargs: Any,
    ) -> None:
        chosen_model = model or DEFAULT_MODEL
        super().__init__(on_fail=on_fail, model=chosen_model, **kwargs)
        self._model = chosen_model

    def validate(self, value: Any, metadata: Dict[str, Any]) -> ValidationResult:
        try:
            resp = litellm.completion(
                model=self._model,
                messages=[
                    {"role": "system", "content": "Return strict JSON."},
                    {"role": "user", "content": str(value)},
                ],
                temperature=0,
            )
            # Parse and decide pass/fail here.
        except Exception as exc:
            return FailResult(error_message=f"LLM validation call failed: {exc}")
        return PassResult()
```

### 3) `validator/__init__.py`

Export only the validator class:

```python
from .main import MyValidator

__all__ = ["MyValidator"]
```

### 4) `tests/test_validator.py`

Use `Guard` integration tests, not only unit tests of helper methods.

Minimum:

1. Pass case asserts `validation_passed is True`.
2. Fail case asserts expected exception/message when `on_fail="exception"` or asserts failure summary for non-exception policy.
3. Any custom fix behavior (`fix_value`) has at least one assertion.

### 5) `README.md`

Include:

1. Overview table.
2. Intended use.
3. Dependencies and required keys/env.
4. Install command:
   - `guardrails hub install hub://<namespace>/<validator_name>`
5. Python usage example with `Guard`.
6. API reference for `__init__` and `validate` including metadata keys.

### 6) `pyproject.toml`

Update:

1. `name`, `version`, `description`, `authors`.
2. runtime dependencies (`guardrails-ai` plus validator-specific packages, including `litellm` for LLM validators).
3. dev deps (`pyright`, `pytest`, `ruff`).
4. `requires-python` consistent with template baseline unless validator requires higher.
5. Keep dependency list explicit and minimal; remove unused packages.

### 6.1) Dependency Checklist (apply to every validator)

1. `guardrails-ai` is present in runtime dependencies.
2. `litellm` is present for any LLM-based validator.
3. Any package imported from `validator/*.py` is declared in runtime dependencies.
4. Any package used only by tests/lint/typecheck is declared in dev dependencies.
5. Required API keys/env vars are listed in `.env` (keys only) and README Requirements section.
6. If `post-install.py` downloads assets, README explains what it downloads and why.

### 7) `Makefile` and CI

Keep targets: `dev`, `lint`, `type`, `test`, `qa`.

`qa` must run:

1. lint
2. type
3. tests

CI `pr_qc.yml` should install dev deps and run `make qa`.

## Remote Inference Pattern (Only If Needed)

If hosting validator inference remotely:

1. Set `has_guardrails_endpoint=True` in `register_validator`.
2. Implement local and remote inference paths (for example, `_inference_local`, `_inference_remote`).
3. Ensure remote response parsing is validated and errors are explicit.
4. Add serving files only when requested.

Do not add remote-hosting complexity for local-only validators.

## Definition of Done

Before submitting:

1. Validator imports from `guardrails.hub` path work (`validator/__init__.py` is correct).
2. `make qa` passes locally.
3. README install command and class name match actual package.
4. Register name matches repo/package identity.
5. LLM validators use LiteLLM only and accept optional model override.
6. Default LLM model is set to latest Claude Haiku LiteLLM id at authoring time.

## Naming Rules

1. Use snake_case repo/package names.
2. Avoid names starting with `is_` and avoid `bug` in names.
3. Register format must be `<namespace>/<validator_name>`.
4. Keep validator class names clear and singular (for example, `ToxicLanguage`, `ValidAddress`).
