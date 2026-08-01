from collections.abc import Mapping

import pandas as pd

from src.models import ValidationResult
from src.validators.base import BaseValidator


class CommodityBookValidator(BaseValidator):
    """Valida que cada commodity use su book correspondiente."""

    def __init__(self, valid_combinations: Mapping[str, str]):
        self.valid_combinations = dict(valid_combinations)
        self.valid_books = set(self.valid_combinations.values())

    def validate(self, dataframe: pd.DataFrame) -> list[ValidationResult]:
        errors = []

        for _, row in dataframe.iterrows():
            commodity = row["commodity"]
            book = row["book"]

            if self._is_empty(commodity) or self._is_empty(book):
                continue

            if commodity not in self.valid_combinations or book not in self.valid_books:
                continue

            expected_book = self.valid_combinations[commodity]
            if book != expected_book:
                errors.append(
                    ValidationResult(
                        closure_id=row["closure_id"],
                        validation_code="INVALID_COMMODITY_BOOK",
                        validation_name="Combinación commodity-book no válida",
                        severity="ERROR",
                        field="book",
                        current_value=book,
                        expected_value=expected_book,
                        message=(
                            f"El commodity '{commodity}' no puede utilizar el book "
                            f"'{book}'. Se esperaba '{expected_book}'."
                        ),
                    )
                )

        return errors

    @staticmethod
    def _is_empty(value: object) -> bool:
        return pd.isna(value) or (isinstance(value, str) and value.strip() == "")
