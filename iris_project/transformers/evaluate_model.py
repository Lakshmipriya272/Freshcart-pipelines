import pandas as pd
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support

if "transformer" not in globals():
    try:
        from mage_ai.data_preparation.decorators import test, transformer
    except ImportError:

        def transformer(f):
            return f

        def test(f):
            return f

CLASS_NAMES = ["setosa", "versicolor", "virginica"]


@transformer
def transform(df, *args, **kwargs):
    cm = confusion_matrix(df["target"], df["prediction"], labels=[0, 1, 2])
    print("Confusion matrix (rows = actual, columns = predicted):")
    print(pd.DataFrame(cm, index=CLASS_NAMES, columns=CLASS_NAMES))

    precision, recall, f1, support = precision_recall_fscore_support(
        df["target"], df["prediction"], labels=[0, 1, 2], zero_division=0
    )
    metrics = pd.DataFrame(
        {"class": CLASS_NAMES, "precision": precision, "recall": recall, "f1": f1, "support": support}
    ).round(4)
    print(metrics.to_string(index=False))
    return metrics


@test
def test_metrics_cover_all_classes(output, *args) -> None:
    assert len(output) == 3
    assert output["support"].sum() == 30
