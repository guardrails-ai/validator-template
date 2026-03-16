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

    def _validate(self, value: Any, metadata: Dict = {}) -> ValidationResult:
        """Validates that {fill in how you validator interacts with the passed value}."""
        # Add your custom validator logic here and return a PassResult or FailResult accordingly.
        if value != "pass": # FIXME
            return FailResult(
                error_message="{A descriptive but concise error message about why validation failed}",
                fix_value="{The programmtic fix if applicable, otherwise remove this kwarg.}",
            )
        return PassResult()

    def _inference_local(self, model_input: Any) -> Any:
        """
        Runs a machine learning pipeline on some input on the local
        machine. This function should receive the expected input to the
        ML model, and output the results from the ml model.
        """
        raise NotImplementedError

    def _inference_remote(self, model_input: Any) -> Any:
        """
        Runs a machine learning pipeline on some input on a remote
        machine. This function should receive the expected input to the
        ML model, and output the results from the ml model.

        """
        raise NotImplementedError

    def _inference(self, model_input: Any) -> Any:
        """Calls either a local or remote inference engine for use in the
        validation call.

        Args:
            model_input (Any): Receives the input to be passed to your ML model.

        Returns:
            Any: Returns the output from the ML model inference.
        """
        # Only use if both are set, otherwise fall back to local inference
        if self.use_local:
            return self._inference_local(model_input)
        if not self.use_local and self.validation_endpoint:
            return self._inference_remote(model_input)

        raise RuntimeError(
            "No inference endpoint set, but use_local was false. "
            "Please set either use_local=True or "
            "set an validation_endpoint to perform inference in the validator."
        )
