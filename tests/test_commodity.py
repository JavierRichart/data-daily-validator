import pandas as pd

from src.validators.commodity import CommodityValidator


def test_detects_invalid_commodity():
    dataframe = pd.DataFrame(
        [
            {
                "closure_id": 1,
                "commodity": "WATER",
            }
        ]
    )

    validator = CommodityValidator(["GAS", "POWER"])

    errors = validator.validate(dataframe)

    assert len(errors) == 1
    assert errors[0].validation_code == "INVALID_COMMODITY"
    assert errors[0].current_value == "WATER"
