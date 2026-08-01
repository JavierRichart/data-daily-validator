import pandas as pd

from src.models import ValidationResult
from src.validators.base import BaseValidator


DEFAULT_VALID_COMPANY_NAMES = ["COMPANY_A", "COMPANY_B"]


class CompanyNameValidator(BaseValidator):
    """Valida que el nombre de la compañía esté entre los valores permitidos."""

    def __init__(self, valid_company_names: list[str] | None = None):
        self.valid_company_names = list(
            DEFAULT_VALID_COMPANY_NAMES
            if valid_company_names is None
            else valid_company_names
        )

    def validate(self, dataframe: pd.DataFrame) -> list[ValidationResult]:
        errors = []

        for _, row in dataframe.iterrows():
            company_name = row["company_name"]

            if self._is_empty(company_name):
                continue

            if company_name not in self.valid_company_names:
                errors.append(
                    ValidationResult(
                        closure_id=row["closure_id"],
                        validation_code="INVALID_COMPANY_NAME",
                        validation_name="Company name no válido",
                        severity="ERROR",
                        field="company_name",
                        current_value=company_name,
                        expected_value=self.valid_company_names,
                        message=f"Company name no válido: {company_name}",
                    )
                )

        return errors

    @staticmethod
    def _is_empty(value: object) -> bool:
        return pd.isna(value) or (isinstance(value, str) and value.strip() == "")
