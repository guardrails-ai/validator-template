from typing import Any, Callable, Dict, Optional

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)


@register_validator(name="guardrails/validator_template", data_type="string")
class ValidatorTemplate(Validator):
    """Validates that {fill in how you validator interacts with the passed value}.

    **Key Properties**

    | Property                      | Description                       |
    | ----------------------------- | --------------------------------- |
    | Name for `format` attribute   | `guardrails/validator_template`   |
    | Supported data types          | `string`                          |
    | Programmatic fix              | {If you support programmatic fixes, explain it here. Otherwise `None`} |

    Args:
        arg_1 (string): {Description of the argument here}
        arg_2 (string): {Description of the argument here}
    """  # noqa

    # If you don't have any init args, you can omit the __init__ method.
    def __init__(
        self,
        arg_1: str,
        arg_2: str,
        on_fail: Optional[Callable] = None,
    ):
        super().__init__(on_fail=on_fail, arg_1=arg_1, arg_2=arg_2)
        self._arg_1 = arg_1
        self._arg_2 = arg_2

    def validate(self, value: Any, metadata: Dict) -> ValidationResult:
        """Validates that {fill in how you validator interacts with the passed value}."""
        # Add your custom validator logic here and return a PassResult or FailResult accordingly.
        if value != "pass": # FIXME
            return FailResult(
                error_message="{A descriptive but concise error message about why validation failed}",
                fix_value="{The programmtic fix if applicable, otherwise remove this kwarg.}",
            )
        return PassResult()
