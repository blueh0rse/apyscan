from apyscan import validate_argument
import pytest


def test_validate_argument_url_valid():
    assert validate_argument("url", "http://127.0.0.1:5000") == "http://127.0.0.1:5000"
    assert validate_argument("url", "https://example.com") == "https://example.com"
    assert (
        validate_argument("url", "https://sub.domain.co:8080/path/to/resource")
        == "https://sub.domain.co:8080/path/to/resource"
    )


def test_validate_argument_url_invalid():
    with pytest.raises(SystemExit):
        validate_argument("url", "http//example")
    with pytest.raises(SystemExit):
        validate_argument("url", "ftp://example.com")
    with pytest.raises(SystemExit):
        validate_argument("url", "https://example.com/ space")


def test_validate_argument_wordlist_valid():
    assert validate_argument("wordlist", "wordlist.txt") == "wordlist.txt"
    assert (
        validate_argument("wordlist", "C:/path/to/file/wordlist.txt")
        == "C:/path/to/file/wordlist.txt"
    )
    assert (
        validate_argument("wordlist", "./relative/path/to/wordlist.txt")
        == "./relative/path/to/wordlist.txt"
    )


def test_validate_argument_wordlist_invalid():
    with pytest.raises(SystemExit):
        validate_argument("wordlist", "wordlist")
    with pytest.raises(SystemExit):
        validate_argument("wordlist", "/path/to/dir/")
    with pytest.raises(SystemExit):
        validate_argument("wordlist", "file with space.txt")


def test_validate_argument_codes_valid():
    assert validate_argument("codes", "200") == [200]
    assert validate_argument("codes", "200,201,301") == [200, 201, 301]


def test_validate_argument_codes_invalid():
    with pytest.raises(SystemExit):
        validate_argument("codes", "abc")
    with pytest.raises(SystemExit):
        validate_argument("codes", "200,abc")
    with pytest.raises(SystemExit):
        validate_argument("codes", "200,201,")


def test_validate_argument_codes_default():
    assert validate_argument("codes", None) == [200, 201, 301]


def test_validate_argument_param_valid():
    assert validate_argument("param", "id") == "id"
    assert validate_argument("param", "user_id") == "user_id"
    assert validate_argument("param", "param-1") == "param-1"
    assert validate_argument("param", "") == ""


def test_validate_argument_param_invalid():
    with pytest.raises(SystemExit):
        validate_argument("param", "id&name")
    with pytest.raises(SystemExit):
        validate_argument("param", "name@123")
    with pytest.raises(SystemExit):
        validate_argument("param", "key value")


def test_validate_argument_limit_valid():
    valid_limits = [1, 100, 999999, 1000000]
    for limit in valid_limits:
        result = validate_argument("limit", limit)
        assert result == limit, f"Expected {limit}, got {result}"


def test_validate_argument_limit_invalid():
    invalid_limits = [0, -1, 1000001, "abc", 1.5, [], {}]
    for limit in invalid_limits:
        with pytest.raises(SystemExit):
            validate_argument("limit", limit)
