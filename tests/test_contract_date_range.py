import pandas as pd

from src.validators.contract_date_range import ContractDateRangeValidator


def _row(**values):
    return {"closure_id": 1, **values}


def test_accepts_contract_date_inside_range_including_boundaries():
    dataframe = pd.DataFrame(
        [
            _row(
                contract_date="2024-01-01",
                contract_start_date="2024-01-01",
                contract_end_date="2024-01-31",
            ),
            _row(
                closure_id=2,
                contract_date="2024-01-31",
                contract_start_date="2024-01-01",
                contract_end_date="2024-01-31",
            ),
        ]
    )

    assert ContractDateRangeValidator().validate(dataframe) == []


def test_detects_contract_date_outside_range():
    dataframe = pd.DataFrame(
        [_row(
            contract_date="2024-02-01",
            contract_start_date="2024-01-01",
            contract_end_date="2024-01-31",
        )]
    )

    errors = ContractDateRangeValidator().validate(dataframe)

    assert len(errors) == 1
    assert errors[0].validation_code == "CONTRACT_DATE_OUT_OF_RANGE"
    assert errors[0].field == "contract_date"


def test_detects_inverted_contract_date_range():
    dataframe = pd.DataFrame(
        [_row(
            contract_date="2024-01-15",
            contract_start_date="2024-02-01",
            contract_end_date="2024-01-01",
        )]
    )

    errors = ContractDateRangeValidator().validate(dataframe)

    assert len(errors) == 1
    assert errors[0].validation_code == "INVALID_CONTRACT_DATE_RANGE"
    assert errors[0].field == "contract_start_date"


def test_detects_invalid_format_or_calendar_date_for_each_field():
    dataframe = pd.DataFrame(
        [_row(
            contract_date="2024/01/01",
            contract_start_date="2024-02-30",
            contract_end_date="2024-01-31 00:00:00",
        )]
    )

    errors = ContractDateRangeValidator().validate(dataframe)

    assert [error.validation_code for error in errors] == [
        "INVALID_CONTRACT_DATE_FORMAT",
        "INVALID_CONTRACT_DATE_FORMAT",
        "INVALID_CONTRACT_DATE_FORMAT",
    ]
    assert [error.field for error in errors] == [
        "contract_date",
        "contract_start_date",
        "contract_end_date",
    ]


def test_rejects_date_with_surrounding_spaces():
    dataframe = pd.DataFrame(
        [_row(
            contract_date=" 2024-01-01 ",
            contract_start_date="2024-01-01",
            contract_end_date="2024-01-31",
        )]
    )

    errors = ContractDateRangeValidator().validate(dataframe)

    assert len(errors) == 1
    assert errors[0].validation_code == "INVALID_CONTRACT_DATE_FORMAT"
    assert errors[0].field == "contract_date"


def test_ignores_null_empty_and_blank_values():
    dataframe = pd.DataFrame(
        [_row(contract_date=None, contract_start_date="", contract_end_date="   ")]
    )

    assert ContractDateRangeValidator().validate(dataframe) == []


def test_does_not_modify_dataframe():
    dataframe = pd.DataFrame(
        [_row(
            contract_date="2024-01-15",
            contract_start_date="2024-01-01",
            contract_end_date="2024-01-31",
        )]
    )
    original = dataframe.copy(deep=True)

    ContractDateRangeValidator().validate(dataframe)

    pd.testing.assert_frame_equal(dataframe, original)
