from sklearn.model_selection import train_test_split

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
    train_idx, test_idx = train_test_split(
        df.index, test_size=0.3, random_state=42, stratify=df["target"]
    )
    out = df.copy()
    out["split"] = "train"
    out.loc[test_idx, "split"] = "test"
    return out


@test
def test_split_column(output, *args) -> None:
    assert set(output["split"]) == {"train", "test"}
    assert (output["split"] == "test").sum() == 30
