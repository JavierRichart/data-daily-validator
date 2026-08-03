from datetime import date, datetime
import re

import pandas as pd

from src.models import ValidationResult
from src.validators.base import BaseValidator


class ContractDateRangeValidator(BaseValidator):
    """Valida que contract_date esté dentro del rango contractual."""

    DATE_FIELDS = (
        "contract_date",
        "contract_start_date",
        "contract_end_date",
    )
    DATE_FORMAT = "%Y-%m-%d"
    DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}\Z")

    def validate(self, dataframe: pd.DataFrame) -> list[ValidationResult]:
        errors = []

        for _, row in dataframe.iterrows():
            parsed_dates = {}
            for field in self.DATE_FIELDS:
                value = row[field]

                if self._is_empty(value):
                    continue

                parsed_date = self._parse_date(value)
                if parsed_date is None:
                    errors.append(
                        ValidationResult(
                            closure_id=row["closure_id"],
                            validation_code="INVALID_CONTRACT_DATE_FORMAT",
                            validation_name="Formato de fecha contractual no válido",
                            severity="ERROR",
                            field=field,
                            current_value=value,
                            expected_value="YYYY-MM-DD",
                            message=(
                                f"El campo '{field}' debe tener el formato YYYY-MM-DD."
                            ),
                        )
                    )
                else:
                    parsed_dates[field] = parsed_date

            start_date = parsed_dates.get("contract_start_date")
            end_date = parsed_dates.get("contract_end_date")
            contract_date = parsed_dates.get("contract_date")

            if start_date is not None and end_date is not None and start_date > end_date:
                errors.append(
                    ValidationResult(
                        closure_id=row["closure_id"],
                        validation_code="INVALID_CONTRACT_DATE_RANGE",
                        validation_name="Rango de fechas contractuales no válido",
                        severity="ERROR",
                        field="contract_start_date",
                        current_value=(row["contract_start_date"], row["contract_end_date"]),
                        expected_value="contract_start_date <= contract_end_date",
                        message="La fecha inicial del contrato es posterior a la fecha final.",
                    )
                )
            elif (
                contract_date is not None
                and start_date is not None
                and end_date is not None
                and not start_date <= contract_date <= end_date
            ):
                errors.append(
                    ValidationResult(
                        closure_id=row["closure_id"],
                        validation_code="CONTRACT_DATE_OUT_OF_RANGE",
                        validation_name="Fecha contractual fuera de rango",
                        severity="ERROR",
                        field="contract_date",
                        current_value=row["contract_date"],
                        expected_value=(
                            row["contract_start_date"],
                            row["contract_end_date"],
                        ),
                        message="contract_date está fuera del rango contractual.",
                    )
                )

        return errors

    @staticmethod
    def _is_empty(value: object) -> bool:
        return pd.isna(value) or (isinstance(value, str) and value.strip() == "")

    @classmethod
    def _parse_date(cls, value: object) -> date | None:
        if not isinstance(value, str) or not cls.DATE_PATTERN.fullmatch(value):
            return None

        try:
            return datetime.strptime(value, cls.DATE_FORMAT).date()
        except ValueError:
            return None
