import pandas as pd

from src.models import ValidationResult
from src.validators.base import BaseValidator

class RequiredFieldsValidator(BaseValidator):

    def __init__(self, required_fields: list[str]):
        self.required_fields = required_fields

    def validate(self, dataframe: pd.DataFrame) -> list[ValidationResult]:
        return[]