# to run these, run 
# pytest test/test-validator.py

from guardrails import Guard
from validator import RegexMatch

guard = Guard.from_string(validators=[RegexMatch(regex="a.*", match_type="fullmatch", on_fail="filter")])

def test_pass():
  TEST_OUTPUT = "a test value"
  raw_output, guarded_output, *rest = guard.parse(TEST_OUTPUT)
  assert(guarded_output is TEST_OUTPUT)

def test_fail():
  TEST_FAIL_OUTPUT = "b test value"
  raw_output, guarded_output, *rest = guard.parse(TEST_FAIL_OUTPUT)
  assert(guarded_output is None)