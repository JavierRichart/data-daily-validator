from dataclasses import dataclass

@dataclass
class ValidationResult:
    closure_id: int
    validation_code: str
    validation_name: str
    severity: str
    field: str
    current_value: object
    expected_value: object
    message: str