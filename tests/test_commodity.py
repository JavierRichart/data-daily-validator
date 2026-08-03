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


def test_ignores_null_empty_and_blank_commodities():
    dataframe = pd.DataFrame(
        [
            {"closure_id": 1, "commodity": None},
            {"closure_id": 2, "commodity": float("nan")},
            {"closure_id": 3, "commodity": ""},
            {"closure_id": 4, "commodity": "   "},
        ]
    )

    errors = CommodityValidator(["GAS", "POWER"]).validate(dataframe)

    assert errors == []
