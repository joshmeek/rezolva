import unittest
from datetime import datetime

from rezolva.preprocessors.preprocessing_functions import (
    extract_initials, format_date, format_phone, lowercase, normalize_address,
    normalize_email, normalize_name, normalize_phone, parse_date,
    remove_accents, remove_punctuation, remove_stopwords,
    replace_special_characters, sort_name_parts, strip_whitespace, truncate,
    uppercase)


class TestPreprocessingFunctions(unittest.TestCase):
    def test_lowercase(self):
        self.assertEqual(lowercase("HELLO"), "hello")
        self.assertEqual(lowercase(123), 123)

    def test_uppercase(self):
        self.assertEqual(uppercase("hello"), "HELLO")
        self.assertEqual(uppercase(123), 123)

    def test_strip_whitespace(self):
        self.assertEqual(strip_whitespace("  hello  "), "hello")
        self.assertEqual(strip_whitespace(123), 123)

    def test_remove_punctuation(self):
        self.assertEqual(remove_punctuation("hello, world!"), "hello world")
        self.assertEqual(remove_punctuation(123), 123)

    def test_remove_accents(self):
        self.assertEqual(remove_accents("café"), "cafe")
        self.assertEqual(remove_accents(123), 123)

    def test_replace_special_characters(self):
        self.assertEqual(replace_special_characters("hello@world", "_"), "hello_world")
        self.assertEqual(replace_special_characters(123), 123)

    def test_truncate(self):
        self.assertEqual(truncate("hello world", 5), "hello")
        self.assertEqual(truncate(123, 5), 123)

    def test_normalize_name(self):
        self.assertEqual(normalize_name("Mr. John Doe Jr."), "john doe")
        self.assertEqual(normalize_name(123), 123)

    def test_sort_name_parts(self):
        self.assertEqual(sort_name_parts("John Doe"), "Doe John")
        self.assertEqual(sort_name_parts(123), 123)

    def test_normalize_phone(self):
        self.assertEqual(normalize_phone("(123) 456-7890"), "1234567890")
        self.assertEqual(normalize_phone(123), 123)

    def test_format_phone(self):
        self.assertEqual(format_phone("1234567890"), "(123) 456-7890")
        self.assertEqual(format_phone("12345"), "12345")
        self.assertEqual(format_phone(123), 123)

    def test_parse_date(self):
        self.assertEqual(parse_date("2021-01-01"), datetime(2021, 1, 1))
        self.assertEqual(parse_date("invalid"), "invalid")
        self.assertEqual(parse_date(123), 123)

    def test_format_date(self):
        self.assertEqual(format_date(datetime(2021, 1, 1)), "2021-01-01")
        self.assertEqual(format_date("2021-01-01"), "2021-01-01")
        self.assertEqual(format_date(123), 123)

    def test_normalize_address(self):
        self.assertEqual(normalize_address("123 Main Street"), "123 main st")
        self.assertEqual(normalize_address(123), 123)

    def test_normalize_email(self):
        self.assertEqual(normalize_email("John.Doe@Example.com"), "john.doe@example.com")
        self.assertEqual(normalize_email(123), 123)

    def test_extract_initials(self):
        self.assertEqual(extract_initials("John Doe"), "JD")
        self.assertEqual(extract_initials(123), 123)

    def test_remove_stopwords(self):
        stopwords = {"the", "is", "a"}
        self.assertEqual(remove_stopwords("this is a test", stopwords), "this test")
        self.assertEqual(remove_stopwords(123, stopwords), 123)


if __name__ == "__main__":
    unittest.main()
