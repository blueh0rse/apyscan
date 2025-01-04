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
