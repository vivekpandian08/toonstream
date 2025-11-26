"""
Comprehensive unit tests for toonlib.
Tests all primitive types, nested structures, and edge cases.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import toonlib
from toonlib import encode, decode, ToonEncodeError, ToonDecodeError


class TestPrimitiveTypes(unittest.TestCase):
    """Test encoding and decoding of primitive types."""
    
    def test_null(self):
        """Test null value."""
        self.assertEqual(encode(None, indent=0), "null")
        self.assertIsNone(decode("null"))
    
    def test_boolean_true(self):
        """Test true boolean."""
        self.assertEqual(encode(True, indent=0), "true")
        self.assertTrue(decode("true"))
    
    def test_boolean_false(self):
        """Test false boolean."""
        self.assertEqual(encode(False, indent=0), "false")
        self.assertFalse(decode("false"))
    
    def test_integer_positive(self):
        """Test positive integer."""
        self.assertEqual(encode(42, indent=0), "42")
        self.assertEqual(decode("42"), 42)
    
    def test_integer_negative(self):
        """Test negative integer."""
        self.assertEqual(encode(-42, indent=0), "-42")
        self.assertEqual(decode("-42"), -42)
    
    def test_integer_zero(self):
        """Test zero."""
        self.assertEqual(encode(0, indent=0), "0")
        self.assertEqual(decode("0"), 0)
    
    def test_float_positive(self):
        """Test positive float."""
        self.assertEqual(encode(3.14, indent=0), "3.14")
        self.assertEqual(decode("3.14"), 3.14)
    
    def test_float_negative(self):
        """Test negative float."""
        self.assertEqual(encode(-3.14, indent=0), "-3.14")
        self.assertEqual(decode("-3.14"), -3.14)
    
    def test_float_with_exponent(self):
        """Test float with scientific notation."""
        result = encode(1.23e10, indent=0)
        # Python may or may not use scientific notation depending on the number
        decoded = decode(result)
        self.assertAlmostEqual(decoded, 1.23e10, places=5)
    
    def test_string_simple(self):
        """Test simple string."""
        self.assertEqual(encode("hello", indent=0), '"hello"')
        self.assertEqual(decode('"hello"'), "hello")
    
    def test_string_empty(self):
        """Test empty string."""
        self.assertEqual(encode("", indent=0), '""')
        self.assertEqual(decode('""'), "")
    
    def test_string_with_spaces(self):
        """Test string with spaces."""
        self.assertEqual(encode("hello world", indent=0), '"hello world"')
        self.assertEqual(decode('"hello world"'), "hello world")
    
    def test_string_with_special_chars(self):
        """Test string with special characters."""
        test_cases = [
            'hello\nworld',
            'hello\tworld',
            'hello"world',
            'hello\\world',
            'hello/world',
        ]
        for test_str in test_cases:
            with self.subTest(test_str=test_str):
                encoded = encode(test_str, indent=0)
                decoded = decode(encoded)
                self.assertEqual(decoded, test_str)
    
    def test_string_unicode(self):
        """Test unicode strings."""
        test_cases = [
            "Hello 世界",
            "🎉🎊",
            "Привет",
            "مرحبا",
        ]
        for test_str in test_cases:
            with self.subTest(test_str=test_str):
                encoded = encode(test_str, indent=0)
                decoded = decode(encoded)
                self.assertEqual(decoded, test_str)


class TestArrays(unittest.TestCase):
    """Test encoding and decoding of arrays."""
    
    def test_empty_array(self):
        """Test empty array."""
        self.assertEqual(encode([], indent=0), "[]")
        self.assertEqual(decode("[]"), [])
    
    def test_array_of_integers(self):
        """Test array of integers."""
        arr = [1, 2, 3, 4, 5]
        encoded = encode(arr, indent=0)
        self.assertEqual(encoded, "[1, 2, 3, 4, 5]")
        self.assertEqual(decode(encoded), arr)
    
    def test_array_of_strings(self):
        """Test array of strings."""
        arr = ["a", "b", "c"]
        encoded = encode(arr, indent=0)
        decoded = decode(encoded)
        self.assertEqual(decoded, arr)
    
    def test_array_mixed_types(self):
        """Test array with mixed types."""
        arr = [1, "hello", True, None, 3.14]
        encoded = encode(arr, indent=0)
        decoded = decode(encoded)
        self.assertEqual(decoded, arr)
    
    def test_nested_arrays(self):
        """Test nested arrays."""
        arr = [[1, 2], [3, 4], [5, 6]]
        encoded = encode(arr, indent=0)
        decoded = decode(encoded)
        self.assertEqual(decoded, arr)
    
    def test_deeply_nested_arrays(self):
        """Test deeply nested arrays."""
        arr = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
        encoded = encode(arr, indent=0)
        decoded = decode(encoded)
        self.assertEqual(decoded, arr)


class TestObjects(unittest.TestCase):
    """Test encoding and decoding of objects."""
    
    def test_empty_object(self):
        """Test empty object."""
        self.assertEqual(encode({}, indent=0), "{}")
        self.assertEqual(decode("{}"), {})
    
    def test_simple_object(self):
        """Test simple object."""
        obj = {"name": "John", "age": 30}
        encoded = encode(obj, indent=0)
        decoded = decode(encoded)
        self.assertEqual(decoded, obj)
    
    def test_object_with_various_types(self):
        """Test object with various value types."""
        obj = {
            "string": "hello",
            "number": 42,
            "float": 3.14,
            "boolean": True,
            "null": None,
        }
        encoded = encode(obj, indent=0)
        decoded = decode(encoded)
        self.assertEqual(decoded, obj)
    
    def test_nested_objects(self):
        """Test nested objects."""
        obj = {
            "person": {
                "name": "John",
                "age": 30,
                "address": {
                    "street": "123 Main St",
                    "city": "Boston"
                }
            }
        }
        encoded = encode(obj, indent=0)
        decoded = decode(encoded)
        self.assertEqual(decoded, obj)
    
    def test_object_with_array(self):
        """Test object containing arrays."""
        obj = {
            "name": "John",
            "hobbies": ["reading", "gaming", "coding"]
        }
        encoded = encode(obj, indent=0)
        decoded = decode(encoded)
        self.assertEqual(decoded, obj)
    
    def test_array_of_objects(self):
        """Test array containing objects."""
        arr = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25}
        ]
        encoded = encode(arr, indent=0)
        decoded = decode(encoded)
        self.assertEqual(decoded, arr)


class TestComplexStructures(unittest.TestCase):
    """Test encoding and decoding of complex nested structures."""
    
    def test_complex_nested_structure(self):
        """Test complex nested structure."""
        data = {
            "users": [
                {
                    "id": 1,
                    "name": "John Doe",
                    "email": "john@example.com",
                    "active": True,
                    "profile": {
                        "age": 30,
                        "location": "Boston",
                        "interests": ["coding", "reading"]
                    }
                },
                {
                    "id": 2,
                    "name": "Jane Smith",
                    "email": "jane@example.com",
                    "active": False,
                    "profile": None
                }
            ],
            "metadata": {
                "total": 2,
                "page": 1,
                "per_page": 10
            }
        }
        encoded = encode(data, indent=0)
        decoded = decode(encoded)
        self.assertEqual(decoded, data)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def test_empty_string_key(self):
        """Test object with empty string key."""
        obj = {"": "empty key"}
        encoded = encode(obj, indent=0)
        decoded = decode(encoded)
        self.assertEqual(decoded, obj)
    
    def test_special_characters_in_keys(self):
        """Test object keys with special characters."""
        obj = {
            "key with spaces": "value1",
            "key\nwith\nnewlines": "value2",
            "key\"with\"quotes": "value3"
        }
        encoded = encode(obj, indent=0)
        decoded = decode(encoded)
        self.assertEqual(decoded, obj)
    
    def test_large_numbers(self):
        """Test very large numbers."""
        large_int = 9007199254740991  # Max safe integer in JS
        self.assertEqual(decode(encode(large_int, indent=0)), large_int)
    
    def test_very_small_float(self):
        """Test very small float."""
        small_float = 1e-10
        encoded = encode(small_float, indent=0)
        decoded = decode(encoded)
        self.assertAlmostEqual(decoded, small_float, places=15)
    
    def test_whitespace_handling(self):
        """Test that decoder handles various whitespace."""
        test_cases = [
            '  [  1  ,  2  ,  3  ]  ',
            '[\n  1,\n  2,\n  3\n]',
            '{\t"key"\t:\t"value"\t}',
        ]
        for toon_str in test_cases:
            with self.subTest(toon_str=toon_str):
                result = decode(toon_str)
                self.assertIsNotNone(result)


class TestLosslessRoundTrip(unittest.TestCase):
    """Test that encoding and decoding is lossless."""
    
    def test_roundtrip_primitives(self):
        """Test roundtrip for all primitive types."""
        test_values = [
            None,
            True,
            False,
            0,
            42,
            -42,
            3.14,
            -3.14,
            "",
            "hello",
            "hello world",
        ]
        for value in test_values:
            with self.subTest(value=value):
                encoded = encode(value, indent=0)
                decoded = decode(encoded)
                self.assertEqual(decoded, value)
    
    def test_roundtrip_collections(self):
        """Test roundtrip for collections."""
        test_values = [
            [],
            [1, 2, 3],
            {},
            {"key": "value"},
            [[1, 2], [3, 4]],
            {"nested": {"key": "value"}},
        ]
        for value in test_values:
            with self.subTest(value=value):
                encoded = encode(value, indent=0)
                decoded = decode(encoded)
                self.assertEqual(decoded, value)
    
    def test_roundtrip_complex(self):
        """Test roundtrip for complex structure."""
        data = {
            "string": "test",
            "number": 42,
            "float": 3.14,
            "bool": True,
            "null": None,
            "array": [1, 2, 3],
            "object": {"nested": "value"},
            "mixed": [1, "two", {"three": 3}]
        }
        encoded = encode(data, indent=0)
        decoded = decode(encoded)
        self.assertEqual(decoded, data)


class TestFormatting(unittest.TestCase):
    """Test formatting options."""
    
    def test_compact_format(self):
        """Test compact format (indent=0)."""
        data = {"key": "value", "array": [1, 2, 3]}
        encoded = encode(data, indent=0)
        self.assertNotIn('\n', encoded)
    
    def test_pretty_format(self):
        """Test pretty format with indentation."""
        data = {"key": "value", "array": [1, 2, 3]}
        encoded = encode(data, indent=2)
        self.assertIn('\n', encoded)
        decoded = decode(encoded)
        self.assertEqual(decoded, data)
    
    def test_sort_keys(self):
        """Test sort_keys option."""
        data = {"z": 1, "a": 2, "m": 3}
        encoded = encode(data, indent=0, sort_keys=True)
        # Keys should appear in alphabetical order
        self.assertLess(encoded.index('"a"'), encoded.index('"m"'))
        self.assertLess(encoded.index('"m"'), encoded.index('"z"'))


class TestErrorHandling(unittest.TestCase):
    """Test error handling and validation."""
    
    def test_decode_invalid_json(self):
        """Test decoding invalid TOON."""
        invalid_cases = [
            "",
            "{invalid}",
            "[1, 2,]",
            '{"key": undefined}',
            "nul",
            "tru",
            "fals",
        ]
        for invalid in invalid_cases:
            with self.subTest(invalid=invalid):
                with self.assertRaises(ToonDecodeError):
                    decode(invalid)
    
    def test_decode_unterminated_string(self):
        """Test decoding unterminated string."""
        with self.assertRaises(ToonDecodeError):
            decode('"unterminated')
    
    def test_decode_invalid_number(self):
        """Test decoding invalid number."""
        with self.assertRaises(ToonDecodeError):
            decode('123.456.789')
    
    def test_encode_unsupported_type(self):
        """Test encoding unsupported type."""
        class CustomClass:
            pass
        
        with self.assertRaises(ToonEncodeError):
            encode(CustomClass())
    
    def test_encode_nan(self):
        """Test encoding NaN."""
        with self.assertRaises(ToonEncodeError):
            encode(float('nan'))
    
    def test_encode_infinity(self):
        """Test encoding infinity."""
        with self.assertRaises(ToonEncodeError):
            encode(float('inf'))
        with self.assertRaises(ToonEncodeError):
            encode(float('-inf'))
    
    def test_decode_trailing_characters(self):
        """Test decoding with trailing characters."""
        with self.assertRaises(ToonDecodeError):
            decode('123 extra')


if __name__ == '__main__':
    unittest.main()
