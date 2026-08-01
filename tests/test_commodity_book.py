import pandas as pd

from src.validators.commodity_book import CommodityBookValidator


VALID_COMBINATIONS = {
    "GAS": "GAS_SPOT",
    "POWER": "POWER_FORWARD",
}


def test_accepts_valid_commodity_book_combinations():
    dataframe = pd.DataFrame(
        [
            {"closure_id": 1, "commodity": "GAS", "book": "GAS_SPOT"},
            {"closure_id": 2, "commodity": "POWER", "book": "POWER_FORWARD"},
        ]
    )

    errors = CommodityBookValidator(VALID_COMBINATIONS).validate(dataframe)

    assert errors == []


def test_uses_injected_combinations_configuration():
    custom_combinations = {
        "GAS": "POWER_FORWARD",
        "POWER": "GAS_SPOT",
    }
    dataframe = pd.DataFrame(
        [
            {"closure_id": 1, "commodity": "GAS", "book": "POWER_FORWARD"},
            {"closure_id": 2, "commodity": "GAS", "book": "GAS_SPOT"},
        ]
    )

    errors = CommodityBookValidator(custom_combinations).validate(dataframe)

    assert len(errors) == 1
    assert errors[0].closure_id == 2
    assert errors[0].expected_value == "POWER_FORWARD"


def test_detects_invalid_commodity_book_combinations():
    dataframe = pd.DataFrame(
        [
            {"closure_id": 1, "commodity": "GAS", "book": "POWER_FORWARD"},
            {"closure_id": 2, "commodity": "POWER", "book": "GAS_SPOT"},
        ]
    )

    errors = CommodityBookValidator(VALID_COMBINATIONS).validate(dataframe)

    assert len(errors) == 2
    assert [error.validation_code for error in errors] == [
        "INVALID_COMMODITY_BOOK",
        "INVALID_COMMODITY_BOOK",
    ]
    assert errors[0].severity == "ERROR"
    assert errors[0].field == "book"
    assert errors[0].current_value == "POWER_FORWARD"
    assert errors[0].expected_value == "GAS_SPOT"
    assert errors[0].closure_id == 1


def test_ignores_empty_values():
    dataframe = pd.DataFrame(
        [
            {"closure_id": 1, "commodity": None, "book": "GAS_SPOT"},
            {"closure_id": 2, "commodity": "GAS", "book": None},
            {"closure_id": 3, "commodity": "   ", "book": "GAS_SPOT"},
            {"closure_id": 4, "commodity": "GAS", "book": "   "},
        ]
    )

    errors = CommodityBookValidator(VALID_COMBINATIONS).validate(dataframe)

    assert errors == []


def test_ignores_unknown_commodity_or_book():
    dataframe = pd.DataFrame(
        [
            {"closure_id": 1, "commodity": "WATER", "book": "GAS_SPOT"},
            {"closure_id": 2, "commodity": "GAS", "book": "UNKNOWN"},
        ]
    )

    errors = CommodityBookValidator(VALID_COMBINATIONS).validate(dataframe)

    assert errors == []


def test_comparison_is_exact_and_does_not_normalize_values():
    dataframe = pd.DataFrame(
        [
            {"closure_id": 1, "commodity": "gas", "book": "GAS_SPOT"},
            {"closure_id": 2, "commodity": "GAS", "book": "GAS_SPOT "},
        ]
    )

    errors = CommodityBookValidator(VALID_COMBINATIONS).validate(dataframe)

    assert errors == []


def test_does_not_modify_dataframe():
    dataframe = pd.DataFrame(
        [{"closure_id": 1, "commodity": "GAS", "book": "POWER_FORWARD"}]
    )
    original = dataframe.copy(deep=True)

    CommodityBookValidator(VALID_COMBINATIONS).validate(dataframe)

    pd.testing.assert_frame_equal(dataframe, original)
