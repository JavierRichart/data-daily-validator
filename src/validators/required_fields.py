import pandas as pd

from src.models import ValidationResult
from src.validators.base import BaseValidator

class RequiredFieldsValidator(BaseValidator):

    def __init__(self, required_fields: list[str]):
        self.required_fields = required_fields

    def validate(self, dataframe: pd.DataFrame) -> list[ValidationResult]:
        errors = []

        for _, row in dataframe.iterrows():
            for field in self.required_fields:
                if pd.isna(row[field]) or row[field]=="":
                    errors.append(
                        ValidationResult(
                            closure_id=row["closure_id"],
                            validation_code="REQUIRED_FIELD",
                            validation_name="Campo obligatorio vacío",
                            severity="ERROR",
                            field=field,
                            current_value=row[field],
                            expected_value="Valor obligatorio",
                            message=f"El campo '{field}' está vacío.",
                        )
                    )
        return errors
