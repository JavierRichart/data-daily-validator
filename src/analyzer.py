import pandas as pd

from src.models import ValidationResult
from src.validators.base import BaseValidator


def run_validations(
        dataframe: pd.DataFrame,
        validators: list[BaseValidator],
) -> list[ValidationResult]:
    errors = []

    for validator in validators:
        errors.extend(validator.validate(dataframe))

    return errors