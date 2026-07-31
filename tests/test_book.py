import pandas as pd

from src.validators.book import BookValidator


def test_accepts_valid_book():
    dataframe = pd.DataFrame(
        [
            {"closure_id": 1, "book": "GAS_SPOT"},
            {"closure_id": 2, "book": "POWER_FORWARD"},
        ]
    )

    errors = BookValidator().validate(dataframe)

    assert errors == []


def test_detects_invalid_book():
    dataframe = pd.DataFrame(
        [
            {
                "closure_id": 1,
                "book": "GAS_FORWARD",
            }
        ]
    )

    errors = BookValidator().validate(dataframe)

    assert len(errors) == 1
    assert errors[0].validation_code == "INVALID_BOOK"
    assert errors[0].severity == "ERROR"
    assert errors[0].field == "book"
    assert errors[0].current_value == "GAS_FORWARD"


def test_ignores_missing_or_blank_book():
    dataframe = pd.DataFrame(
        [
            {"closure_id": 1, "book": None},
            {"closure_id": 2, "book": float("nan")},
            {"closure_id": 3, "book": ""},
            {"closure_id": 4, "book": "   "},
        ]
    )

    errors = BookValidator().validate(dataframe)

    assert errors == []


def test_comparison_is_case_sensitive_and_does_not_normalize_values():
    dataframe = pd.DataFrame(
        [
            {"closure_id": 1, "book": "gas_spot"},
            {"closure_id": 2, "book": "GAS_SPOT "},
        ]
    )

    errors = BookValidator().validate(dataframe)

    assert len(errors) == 2
    assert [error.current_value for error in errors] == ["gas_spot", "GAS_SPOT "]


def test_accepts_custom_valid_books():
    dataframe = pd.DataFrame(
        [
            {
                "closure_id": 1,
                "book": "CUSTOM_BOOK",
            }
        ]
    )

    errors = BookValidator(["CUSTOM_BOOK"]).validate(dataframe)

    assert errors == []
