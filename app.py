from pathlib import Path

from src.analyzer import run_validations
from src.loader import load_file
from src.models import ValidationResult
from src.validators.base import BaseValidator
from src.validators.book import BookValidator
from src.validators.commodity import CommodityValidator
from src.validators.commodity_book import CommodityBookValidator
from src.validators.company_name import CompanyNameValidator
from src.validators.contract_date_range import ContractDateRangeValidator
from src.validators.required_fields import RequiredFieldsValidator


def build_validators() -> list[BaseValidator]:
    return [
        RequiredFieldsValidator(
            [
                "closure_id",
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
        CommodityBookValidator(
            {
                "GAS": "GAS_SPOT",
                "POWER": "POWER_FORWARD",
            }
        ),
        CompanyNameValidator(),
        ContractDateRangeValidator(),
    ]


def main(file_path: str | Path = "data/closures.csv") -> list[ValidationResult]:
    dataframe = load_file(file_path)
    errors = run_validations(dataframe, build_validators())

    if not errors:
        print("No se encontraron errores de validación.")
        return errors

    print("Errores de validación:")
    for error in errors:
        print(
            f"[{error.severity}] {error.validation_code} - "
            f"closure_id={error.closure_id}, campo={error.field}: {error.message}"
        )

    return errors


if __name__ == "__main__":
    main()
