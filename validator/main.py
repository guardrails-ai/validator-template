from typing import Any, Callable, Dict, List, Optional, Union

from guardrails.validator_base import (
    ErrorSpan,
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)


@register_validator(
    name="guardrails/validator_template",
    data_type="string",
    has_guardrails_endpoint=True,
)
class ValidatorTemplate(Validator):
    """Validates that {fill in how your validator interacts with the passed value}.

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
        **kwargs,
    ):
        super().__init__(on_fail=on_fail, arg_1=arg_1, arg_2=arg_2, **kwargs)
        self._arg_1 = arg_1
        self._arg_2 = arg_2

    def validate(self, value: Any, metadata: Dict[str, Any] = {}) -> ValidationResult:
        """Validates that {fill in how your validator interacts with the passed value}."""

        # 1. Run inference (this dispatches to _inference_local or _inference_remote
        #    depending on how the validator was configured at usage time).
        prediction = self._inference(value)

        # 2. Check the prediction and return a PassResult or FailResult.
        #    Replace this placeholder logic with your own.
        if prediction is not None:  # FIXME: replace with your pass/fail condition
            return PassResult()

        # 3. On failure, return a FailResult with:
        #    - error_message: a human-readable explanation of the failure
        #    - fix_value: the programmatic fix (or omit if not applicable)
        #    - error_spans: character-level locations of the errors (or omit if not applicable)
        return FailResult(
            error_message="...",  # FIXME
            fix_value="...",  # FIXME (or remove if no programmatic fix)
            error_spans=[
                ErrorSpan(
                    start=0,
                    end=len(value),
                    reason="...",  # FIXME
                )
            ],
        )

    def _inference_local(self, model_input: Any) -> Any:
        """Run inference locally.

        This is called when the validator is used with `use_local=True`.
        Implement your model/logic here (e.g. load a HuggingFace model, call
        an nltk function, run a regex, etc.).
        """
        # FIXME: Replace with your local inference logic.
        return model_input

    def _inference_remote(self, model_input: Any) -> Any:
        """Run inference via a remote endpoint.

        This is called when the validator uses the Guardrails Hub inference
        endpoint (i.e. `use_local=False`, the default). The base class
        `_hub_inference_request` helper handles the HTTP call for you.
        """
        # FIXME: Replace with your remote inference request format.
        request_body = {
            "inputs": [
                {
                    "name": "text",
                    "shape": [1],
                    "data": [model_input],
                    "datatype": "BYTES",
                },
            ]
        }
        response = self._hub_inference_request(request_body, self.validation_endpoint)
        return response
