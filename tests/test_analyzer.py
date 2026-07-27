import pandas as pd

from src.analyzer import run_validations
from src.validators.required_fields import RequiredFieldsValidator
from src.validators.commodity import CommodityValidator


def test_run_multiple_validations():
    dataframe = pd.DataFrame(
        [
            {
                "closure_id": 1,
                "book": "",
                "commodity": "WATER",
            }
        ]
    )

    validators = [
        RequiredFieldsValidator(["book", "commodity"]),
        CommodityValidator(["GAS", "POWER"]),
    ]

    errors = run_validations(dataframe, validators)

    assert len(errors) == 2
    assert errors[0].validation_code == "REQUIRED_FIELD"
    assert errors[1].validation_code == "INVALID_COMMODITY"