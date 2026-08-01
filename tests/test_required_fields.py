import pandas as pd

from  src.validators.required_fields import RequiredFieldsValidator


def test_detects_empty_required_field():
    dataframe = pd.DataFrame(
        [
            {
                "closure_id": 1,
                "book": "",
                "commodity": "GAS",
            }
        ]
    )

    validator = RequiredFieldsValidator(["book", "commodity"])
    errors = validator.validate(dataframe)

    assert len(errors) == 1
    assert errors[0].field == "book"
    assert errors[0].closure_id == 1


def test_detects_required_field_with_only_spaces():
    dataframe = pd.DataFrame(
        [
            {
                "closure_id": 1,
                "book": "   ",
                "commodity": "GAS",
            }
        ]
    )

    errors = RequiredFieldsValidator(["book"]).validate(dataframe)

    assert len(errors) == 1
    assert errors[0].validation_code == "REQUIRED_FIELD"
    assert errors[0].field == "book"
    assert errors[0].current_value == "   "


def test_does_not_consider_zero_or_false_empty():
    dataframe = pd.DataFrame(
        [
            {
                "closure_id": 1,
                "book": 0,
                "commodity": False,
            }
        ]
    )

    errors = RequiredFieldsValidator(["book", "commodity"]).validate(dataframe)

    assert errors == []
