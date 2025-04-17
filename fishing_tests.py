import math
from fishing import get_production_need


def test_get_production_need():
    data = {
        "population": {"AMP": {1961: 10000}},
        "consumption": {"AMP": {1961: 10}}
    }
    assert math.isclose(
        get_production_need(data, "AMP", 1961), 100.0
    )
    assert get_production_need(data, "AMP", 1960) is None


if __name__ == "__main__":
    test_get_production_need()
    print("All tests passed!")
