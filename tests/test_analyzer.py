import pandas as pd

from src.analyzer import run_validations
from src.validators.required_fields import RequiredFieldsValidator


def test_run_validations():
    dataframe = pd.DataFrame(
        [
            {
                "closure_id": 1,
                "book": "",
                "commodity": "GAS",
            }
        ]
    )

    validators = [
        RequiredFieldsValidator(["book", "commodity"])
    ]

    errors = run_validations(dataframe, validators)

    assert len(errors) == 1
    assert errors[0].validation_code == "REQUIRED_FIELD"