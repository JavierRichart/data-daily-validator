from abc import ABC, abstractmethod

import pandas as pd

from src.models import ValidationResult


class BaseValidator(ABC):

    @abstractmethod
    def validate(self, dataframe: pd.DataFrame) -> list[ValidationResult]:
        """Ejecuta la validación y devuelve los errores encontrados."""
        raise NotImplementedError