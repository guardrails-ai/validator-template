# to run these, run
# make test

from guardrails import Guard
import pytest
from validator import ValidatorTemplate

# Create guards using the modern Guard().use() API.
# Learn more about corrective actions here:
#  https://www.guardrailsai.com/docs/concepts/output/#%EF%B8%8F-specifying-corrective-actions

guard = Guard().use(
    ValidatorTemplate,
    arg_1="arg_1",
    arg_2="arg_2",
    on_fail="exception",
    use_local=True,
)

fix_guard = Guard().use(
    ValidatorTemplate,
    arg_1="arg_1",
    arg_2="arg_2",
    on_fail="fix",
    use_local=True,
)


def test_pass():
    result = guard.validate("pass")

    assert result.validation_passed is True
    assert result.validated_output == "pass"


def test_fail_exception():
    with pytest.raises(Exception):
        guard.validate("fail")


def test_fail_fix():
    result = fix_guard.validate("fail")

    assert result.validation_passed is False
    # When on_fail="fix", the validated_output should be the fix_value
    # from the FailResult (if your validator provides one).
    assert result.validated_output is not None
