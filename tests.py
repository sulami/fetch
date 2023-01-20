import unittest

from fetch import *


def test_parse_url_root():
    assert parse_url("https://google.com") == "google.com.html"


def test_parse_url_trailing_slash():
    assert parse_url("https://google.com/") == "google.com.html"


def test_parse_url_path():
    assert parse_url("https://google.com/foo") == "google.com__foo.html"


def test_parse_url_path_trailing_slash():
    assert parse_url("https://google.com/foo/") == "google.com__foo.html"


def test_parse_url_path_with_extensions():
    assert parse_url("https://google.com/foo.gif") == "google.com__foo.gif"


if __name__ == "__main__":
    unittest.main()
