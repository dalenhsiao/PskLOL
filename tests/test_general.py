import PskLOL as lol


def test_category_search():
    lol.category_search(
        institutions=["carnegie mellon university"],
        category=["engineering"],
    )
    assert True
