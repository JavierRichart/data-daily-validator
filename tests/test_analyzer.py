import pandas as pd

from src.analyzer import run_validations
from src.validators.book import BookValidator
from src.validators.commodity_book import CommodityBookValidator
from src.validators.company_name import CompanyNameValidator
from src.validators.contract_date_range import ContractDateRangeValidator
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


def test_run_all_validators_returns_one_expected_error_per_invalid_row():
    valid_combinations = {
        "GAS": "GAS_SPOT",
        "POWER": "POWER_FORWARD",
    }
    valid_dates = {
        "contract_date": "2024-01-15",
        "contract_start_date": "2024-01-01",
        "contract_end_date": "2024-01-31",
    }

    def row(closure_id, **values):
        return {
            "closure_id": closure_id,
            "book": "GAS_SPOT",
            "commodity": "GAS",
            "company_name": "COMPANY_A",
            **valid_dates,
            **values,
        }

    dataframe = pd.DataFrame(
        [
            row(1),
            row(2, book=""),
            row(3, commodity="WATER"),
            row(4, book="UNKNOWN"),
            row(5, book="POWER_FORWARD"),
            row(6, company_name="COMPANY_C"),
            row(7, contract_date="2024-02-01"),
        ]
    )

    validators = [
        RequiredFieldsValidator(
            [
                "book",
                "commodity",
                "company_name",
                "contract_date",
                "contract_start_date",
                "contract_end_date",
            ]
        ),
        CommodityValidator(["GAS", "POWER"]),
        BookValidator(),
        CommodityBookValidator(valid_combinations),
        CompanyNameValidator(),
        ContractDateRangeValidator(),
    ]

    errors = run_validations(dataframe, validators)

    assert [error.validation_code for error in errors] == [
        "REQUIRED_FIELD",
        "INVALID_COMMODITY",
        "INVALID_BOOK",
        "INVALID_COMMODITY_BOOK",
        "INVALID_COMPANY_NAME",
        "CONTRACT_DATE_OUT_OF_RANGE",
    ]
    assert [error.closure_id for error in errors] == [2, 3, 4, 5, 6, 7]
