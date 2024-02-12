# Overview

| Developed by | Guardrails AI |
| Date of development | Feb 15, 2024 |
| Validator type | Format |
| Blog |  |
| License | Apache 2 |
| Input/Output | Output |

# Description

This validator ensures that a generated output is the literal "pass".

# Installation

```bash
$ guardrails hub install hub://guardrails/validator_template
```

# Usage Examples

## Validating string output via Python

In this example, we’ll test that a generated word is `pass`.

```python
# Import Guard and Validator
from guardrails.hub import ValidatorTemplate
from guardrails import Guard

# Initialize Validator
val = ValidatorTemplate()

# Setup Guard
guard = Guard.from_string(
    validators=[val, ...],
)

guard.parse("pass")  # Validator passes
guard.parse("fail")  # Validator fails
```

## Validating JSON output via Python

In this example, we verify that a processes’s status is specified as `pass`.

```python
# Import Guard and Validator
from pydantic import BaseModel
from guardrails.hub import ValidatorTemplate
from guardrails import Guard

val = ValidatorTemplate()

# Create Pydantic BaseModel
class Process(BaseModel):
		process_name: str
		status: str = Field(validators=[val])

# Create a Guard to check for valid Pydantic output
guard = Guard.from_pydantic(output_class=Process)

# Run LLM output generating JSON through guard
guard.parse("""
{
		"process_name": "templating",
		"status": "pass"
}
""")
```

# API Reference

`__init__`
- `arg_1`: A placeholder argument to demonstrate how to use init arguments.
- `arg_2`: Another placeholder argument to demonstrate how to use init arguments.
- `on_fail`: The policy to enact when a validator fails.