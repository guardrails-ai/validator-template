from guardrails import Guard
from pydantic import BaseModel, Field
from validator import RegexMatch


class ValidatorTestObject(BaseModel):
    test_val: str = Field(validators=[RegexMatch("a.*")])


TEST_OUTPUT = """
{
  "test_val": "a string"
}
"""

guard = Guard.from_pydantic(output_class=ValidatorTestObject)

raw_output, guarded_output, *rest = guard.parse(TEST_OUTPUT)

print("validated output: ", guarded_output)