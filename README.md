# test_validator
Template repository that hosts a sample validator to be used within GuardrailsHub.

# Installation instructions
- Update the [pyproject.toml](pyproject.toml) file and make necessary changes as follows:
    - Update the `name` field to the name of your validator
    - Update the `description` field to a short description of your validator
    - Update the `authors` field to your name and email
    - Add/update the `dependencies` field to include all dependencies your validator needs.
- If there are are any post-installation steps such as downloading tokenizers, logging into huggingface etc., update the [post-install.py](validator/post-install.py) file accordingly.
- You can add additional files to the [validator](validator) directory, but don't rename any existing files/directories.
    - e.g. Add any environment variables (without the values, just the keys) to the [.env](.env) file.
- Ensure that there are no other dependencies or any additional steps required to run your validator.


# Run instructions
- Wherever you're using the validator, add the following import statement:
```python
from <path-to-this-directory> import <your-validator-name>
# e.g.
from validator import RegexMatch
```
- That's it! Now, you can use the validator in Guardrails.

