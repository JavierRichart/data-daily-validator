from src.loader import load_file

def test_load_csv():
    df = load_file("data/closures.csv")

    assert len(df) == 3
    assert "commodity" in df.columns
    assert df.iloc[0]["closure_id"] == 1