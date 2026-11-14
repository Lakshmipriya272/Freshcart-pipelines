from pathlib import Path

if "data_exporter" not in globals():
    try:
        from mage_ai.data_preparation.decorators import data_exporter, test
    except ImportError:

        def data_exporter(f):
            return f

        def test(f):
            return f

OUTPUT_FILE = "iris_predictions.csv"


@data_exporter
def export_data(df, *args, **kwargs):
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"save_results: wrote {len(df)} rows to {OUTPUT_FILE}")


@test
def test_file_written(*args) -> None:
    assert Path(OUTPUT_FILE).exists(), f"{OUTPUT_FILE} was not created"
