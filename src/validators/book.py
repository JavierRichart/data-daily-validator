import pandas as pd

from src.models import ValidationResult
from src.validators.base import BaseValidator


DEFAULT_VALID_BOOKS = ["GAS_SPOT", "POWER_FORWARD"]


class BookValidator(BaseValidator):

    def __init__(self, valid_books: list[str] | None = None):
        self.valid_books = list(
            DEFAULT_VALID_BOOKS if valid_books is None else valid_books
        )

    def validate(self, dataframe: pd.DataFrame) -> list[ValidationResult]:
        errors = []

        for _, row in dataframe.iterrows():
            book = row["book"]

            if pd.isna(book) or (isinstance(book, str) and book.strip() == ""):
                continue

            if book not in self.valid_books:
                errors.append(
                    ValidationResult(
                        closure_id=row["closure_id"],
                        validation_code="INVALID_BOOK",
                        validation_name="Book no válido",
                        severity="ERROR",
                        field="book",
                        current_value=book,
                        expected_value=self.valid_books,
                        message=f"Book no válido: {book}",
                    )
                )

        return errors
