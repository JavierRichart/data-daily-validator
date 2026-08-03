import pandas as pd

from app import build_validators, main


def test_main_reports_no_errors_for_valid_sample(capsys):
    errors = main("data/closures.csv")

    captured = capsys.readouterr()

    assert errors == []
    assert "No se encontraron errores de validación." in captured.out


def test_build_validators_configures_all_validators():
    validators = build_validators()

    assert len(validators) == 6


def test_main_prints_validation_errors(tmp_path, capsys):
    dataframe = pd.read_csv("data/closures.csv")
    dataframe.loc[0, "commodity"] = "WATER"
    file_path = tmp_path / "invalid_closures.csv"
    dataframe.to_csv(file_path, index=False)

    errors = main(file_path)

    captured = capsys.readouterr()

    assert [error.validation_code for error in errors] == ["INVALID_COMMODITY"]
    assert "INVALID_COMMODITY" in captured.out
