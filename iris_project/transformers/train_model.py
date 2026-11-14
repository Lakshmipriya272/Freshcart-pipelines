from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

if "transformer" not in globals():
    try:
        from mage_ai.data_preparation.decorators import test, transformer
    except ImportError:

        def transformer(f):
            return f

        def test(f):
            return f

FEATURES = ["sepal length (cm)", "sepal width (cm)", "petal length (cm)", "petal width (cm)"]
MIN_ACCURACY = 0.90


@transformer
def transform(df, *args, **kwargs):
    max_depth = int(kwargs.get("max_depth", 3))
    train = df[df["split"] == "train"]
    test_rows = df[df["split"] == "test"]

    model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    model.fit(train[FEATURES], train["target"])

    out = test_rows.copy()
    out["prediction"] = model.predict(test_rows[FEATURES])
    out["max_depth"] = max_depth
    accuracy = accuracy_score(out["target"], out["prediction"])
    out["test_accuracy"] = accuracy
    print(f"train_model: max_depth={max_depth}, test_accuracy={accuracy:.4f}")
    return out


@test
def test_accuracy(output, *args) -> None:
    accuracy = output["test_accuracy"].iloc[0]
    assert accuracy >= MIN_ACCURACY, f"Accuracy {accuracy:.4f} is below {MIN_ACCURACY}"
