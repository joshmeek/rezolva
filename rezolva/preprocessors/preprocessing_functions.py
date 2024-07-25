"""
Collection of preprocessing functions for use with SimplePreprocessor

These functions can be passed to SimplePreprocessor to create a custom preprocessing pipeline.
Each function takes a single value as input and returns the processed value.
"""

import re
import unicodedata
from datetime import datetime
from typing import Any, Dict

from ..core.base import Entity


# Basic string operations
def lowercase(value: Any) -> Any:
    return value.lower() if isinstance(value, str) else value


def uppercase(value: Any) -> Any:
    return value.upper() if isinstance(value, str) else value


def strip_whitespace(value: Any) -> Any:
    return value.strip() if isinstance(value, str) else value


def remove_punctuation(value: Any) -> Any:
    if isinstance(value, str):
        return "".join(char for char in value if char.isalnum() or char.isspace())
    return value


# Advanced string operations
def remove_accents(value: Any) -> Any:
    if isinstance(value, str):
        return "".join(c for c in unicodedata.normalize("NFD", value) if unicodedata.category(c) != "Mn")
    return value


def replace_special_characters(value: Any, replacement: str = "") -> Any:
    if isinstance(value, str):
        return re.sub(r"[^a-zA-Z0-9\s]", replacement, value)
    return value


def truncate(value: Any, max_length: int) -> Any:
    if isinstance(value, str) and len(value) > max_length:
        return value[:max_length]
    return value


# Name-specific operations
def normalize_name(value: Any) -> Any:
    if isinstance(value, str):
        # Remove titles, suffixes, etc.
        name_parts = value.lower().replace(".", "").split()
        name_parts = [part for part in name_parts if part not in {"mr", "mrs", "ms", "dr", "prof", "jr", "sr"}]
        return " ".join(name_parts)
    return value


def sort_name_parts(value: Any) -> Any:
    if isinstance(value, str):
        return " ".join(sorted(value.split()))
    return value


# Number operations
def normalize_phone(value: Any) -> Any:
    if isinstance(value, str):
        return "".join(char for char in value if char.isdigit())
    return value


def format_phone(value: Any, format: str = "(###) ###-####") -> Any:
    if isinstance(value, str):
        digits = "".join(char for char in value if char.isdigit())
        if len(digits) == 10:
            for digit in digits:
                format = format.replace("#", digit, 1)
            return format
    return value


# Date operations
def parse_date(value: Any, input_format: str = "%Y-%m-%d") -> Any:
    if isinstance(value, str):
        try:
            return datetime.strptime(value, input_format)
        except ValueError:
            pass
    return value


def format_date(value: Any, output_format: str = "%Y-%m-%d") -> Any:
    if isinstance(value, datetime):
        return value.strftime(output_format)
    return value


# Address operations
def normalize_address(value: Any) -> Any:
    if isinstance(value, str):
        # Replace common abbreviations
        replacements = {
            "street": "st",
            "road": "rd",
            "avenue": "ave",
            "drive": "dr",
            "lane": "ln",
            "boulevard": "blvd",
            "circle": "cir",
            "north": "n",
            "south": "s",
            "east": "e",
            "west": "w",
        }
        normalized = value.lower()
        for full, abbr in replacements.items():
            normalized = re.sub(rf"\b{full}\b", abbr, normalized)
            normalized = re.sub(rf"\b{full}\.?\b", abbr, normalized)
        return normalized
    return value


# Email operations
def normalize_email(value: Any) -> Any:
    if isinstance(value, str):
        return value.lower().strip()
    return value


# Advanced operations
def extract_initials(value: Any) -> Any:
    if isinstance(value, str):
        return "".join(word[0].upper() for word in value.split() if word)
    return value


def remove_stopwords(value: Any, stopwords: set) -> Any:
    if isinstance(value, str):
        return " ".join(word for word in value.split() if word.lower() not in stopwords)
    return value


# Entity-level operations
def merge_fields(entity: Entity, fields: list, new_field: str, separator: str = " ") -> Entity:
    merged_value = separator.join(str(entity.attributes.get(field, "")) for field in fields)
    new_attributes = {**entity.attributes, new_field: merged_value}
    return Entity(entity.id, new_attributes)


def split_field(entity: Entity, field: str, new_fields: list, separator: str = " ") -> Entity:
    if field in entity.attributes:
        parts = entity.attributes[field].split(separator)
        new_attributes = {**entity.attributes}
        for i, new_field in enumerate(new_fields):
            if i < len(parts):
                new_attributes[new_field] = parts[i]
            else:
                new_attributes[new_field] = ""
        return Entity(entity.id, new_attributes)
    return entity


# Conditional operations
def apply_if(value: Any, condition: callable, function: callable) -> Any:
    if condition(value):
        return function(value)
    return value


# Type conversion
def to_string(value: Any) -> str:
    return str(value)


def to_int(value: Any) -> Any:
    try:
        return int(value)
    except (ValueError, TypeError):
        return value


def to_float(value: Any) -> Any:
    try:
        return float(value)
    except (ValueError, TypeError):
        return value


# Custom field mapping
def map_values(value: Any, mapping: Dict[Any, Any]) -> Any:
    return mapping.get(value, value)


# Regex-based operations
def extract_pattern(value: Any, pattern: str) -> Any:
    if isinstance(value, str):
        match = re.search(pattern, value)
        if match:
            return match.group()
    return value


def replace_pattern(value: Any, pattern: str, replacement: str) -> Any:
    if isinstance(value, str):
        return re.sub(pattern, replacement, value)
    return value
