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