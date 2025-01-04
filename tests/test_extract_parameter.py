import pytest
from apyscan import extract_parameter


def test_extract_parameter():
    url = "http://127.0.0.1:5000/api/v1/users?id=1&name=test"
    assert extract_parameter(url, "id") == "id"
    assert extract_parameter(url, "name") == "name"

    url = "http://127.0.0.1:5000/api/v1/users?id=1&name=test"
    assert extract_parameter(url, "") == "id"

    url = "http://127.0.0.1:5000/api/v1/users?param=value"
    assert extract_parameter(url, "param") == "param"

    url = "http://127.0.0.1:5000/api/v1/users"
    with pytest.raises(ValueError):
        extract_parameter(url, "id")

    url = "http://127.0.0.1:5000/api/v1/users?id=1"
    with pytest.raises(ValueError):
        extract_parameter(url, "name")
