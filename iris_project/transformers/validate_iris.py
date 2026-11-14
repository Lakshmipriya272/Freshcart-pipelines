if "transformer" not in globals():
    try:
        from mage_ai.data_preparation.decorators import test, transformer
    except ImportError:

        def transformer(f):
            return f

        def test(f):
            return f


@transformer
def transform(df, *args, **kwargs):
    missing = int(df.isna().sum().sum())
    classes = df["target"].nunique()
    print(f"validate_iris: missing values={missing}, classes={classes}")
    return df


@test
def test_clean_and_three_classes(output, *args) -> None:
    assert output.isna().sum().sum() == 0, "Iris data contains missing values"
    assert output["target"].nunique() == 3, "Iris data must have exactly 3 classes"
