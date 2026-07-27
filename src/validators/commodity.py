import pandas as pd

from src.models import ValidationResult
from src.validators.base import BaseValidator


class CommodityValidator(BaseValidator):

    def __init__(self, valid_commodities: list[str]):
        self.valid_commodities = valid_commodities

    def validate(self, dataframe: pd.DataFrame) -> list[ValidationResult]:
        errors = []

        for _, row in dataframe.iterrows():
            if row["commodity"] not in self.valid_commodities:
                errors.append(
                    ValidationResult(
                        closure_id=row["closure_id"],
                        validation_code='INVALID_COMMODITY',
                        validation_name="Commodity no válida",
                        severity="ERROR",
                        field="commodity",
                        current_value=row["commodity"],
                        expected_value=self.valid_commodities,
                        message=f"Commodity no válida: {row['commodity']}",
                    )
                )
        return errors