from sklearn.datasets import load_iris as sk_load_iris

if "data_loader" not in globals():
    try:
        from mage_ai.data_preparation.decorators import data_loader, test
    except ImportError:

        def data_loader(f):
            return f

        def test(f):
            return f


@data_loader
def load_data(*args, **kwargs):
    return sk_load_iris(as_frame=True).frame


@test
def test_shape(output, *args) -> None:
    assert output.shape == (150, 5), f"Expected (150, 5), got {output.shape}"
