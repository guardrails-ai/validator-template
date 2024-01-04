# Installation instructions
- Add any commands here that are required before installing the pre-requisites e.g. Huggingface Hub authentication etc.
- Install the requirements using the following command:
```bash
pip install -r <path-to-this-directory>/requirements.txt
# e.g
pip install -r test_validator/requirements.txt
```
- Wherever you're using the validator, add the following import statement:
```python
from <path-to-this-directory> import <your-validator-name>
# e.g.
from test_validator import RegexMatch
```

