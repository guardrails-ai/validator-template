# to run these, run 
# make tests

from guardrails import Guard
import pytest
from validator import ValidatorTemplate

# We use 'exception' as the validator's fail action,
#  so we expect failures to always raise an Exception
# Learn more about corrective actions here:
#  https://www.guardrailsai.com/docs/concepts/output/#%EF%B8%8F-specifying-corrective-actions
guard = Guard.from_string(validators=[ValidatorTemplate(arg_1="arg_1", arg_2="arg_2", on_fail="exception")])

def test_pass():
  test_output = "pass"
  result = guard.parse(test_output)
  
  assert result.validation_passed is True
  assert result.validated_output == test_output

def test_fail():
  with pytest.raises(Exception) as exc_info:
    test_output = "fail"
    guard.parse(test_output)
  
  # Assert the exception has your error_message
  assert str(exc_info.value) == "Validation failed for field with errors: {A descriptive but concise error message about why validation failed}"
