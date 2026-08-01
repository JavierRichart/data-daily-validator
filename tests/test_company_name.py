import pandas as pd

from src.validators.company_name import CompanyNameValidator


def test_accepts_default_valid_company_names():
    dataframe = pd.DataFrame(
        [
            {"closure_id": 1, "company_name": "COMPANY_A"},
            {"closure_id": 2, "company_name": "COMPANY_B"},
        ]
    )

    errors = CompanyNameValidator().validate(dataframe)

    assert errors == []


def test_detects_invalid_company_name():
    dataframe = pd.DataFrame(
        [{"closure_id": 1, "company_name": "COMPANY_C"}]
    )

    errors = CompanyNameValidator().validate(dataframe)

    assert len(errors) == 1
    assert errors[0].validation_code == "INVALID_COMPANY_NAME"
    assert errors[0].validation_name == "Company name no válido"
    assert errors[0].severity == "ERROR"
    assert errors[0].field == "company_name"
    assert errors[0].current_value == "COMPANY_C"
    assert errors[0].expected_value == ["COMPANY_A", "COMPANY_B"]
    assert errors[0].closure_id == 1
    assert errors[0].message == "Company name no válido: COMPANY_C"


def test_ignores_empty_company_names():
    dataframe = pd.DataFrame(
        [
            {"closure_id": 1, "company_name": None},
            {"closure_id": 2, "company_name": float("nan")},
            {"closure_id": 3, "company_name": ""},
            {"closure_id": 4, "company_name": "   "},
        ]
    )

    errors = CompanyNameValidator().validate(dataframe)

    assert errors == []


def test_comparison_is_case_sensitive_and_does_not_normalize_values():
    dataframe = pd.DataFrame(
        [
            {"closure_id": 1, "company_name": "company_a"},
            {"closure_id": 2, "company_name": "COMPANY_A "},
        ]
    )

    errors = CompanyNameValidator().validate(dataframe)

    assert len(errors) == 2
    assert [error.current_value for error in errors] == [
        "company_a",
        "COMPANY_A ",
    ]


def test_uses_custom_valid_company_names():
    dataframe = pd.DataFrame(
        [
            {"closure_id": 1, "company_name": "CUSTOM_COMPANY"},
            {"closure_id": 2, "company_name": "COMPANY_A"},
        ]
    )

    errors = CompanyNameValidator(["CUSTOM_COMPANY"]).validate(dataframe)

    assert len(errors) == 1
    assert errors[0].closure_id == 2
    assert errors[0].current_value == "COMPANY_A"
    assert errors[0].expected_value == ["CUSTOM_COMPANY"]


def test_does_not_modify_dataframe():
    dataframe = pd.DataFrame(
        [{"closure_id": 1, "company_name": "COMPANY_C"}]
    )
    original = dataframe.copy(deep=True)

    CompanyNameValidator().validate(dataframe)

    pd.testing.assert_frame_equal(dataframe, original)
