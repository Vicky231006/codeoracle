"""
Test suite for main module.
"""

import unittest
from main import main
from utils import calculate_sum, format_output


class TestMain(unittest.TestCase):
    """Test cases for main module."""
    
    def test_calculate_sum(self):
        """Test the calculate_sum function."""
        numbers = [1, 2, 3, 4, 5]
        result = calculate_sum(numbers)
        self.assertEqual(result, 15)
    
    def test_format_output_small(self):
        """Test format_output with small value."""
        result = format_output(5)
        self.assertIn("Small value", result)
    
    def test_format_output_medium(self):
        """Test format_output with medium value."""
        result = format_output(50)
        self.assertIn("Medium value", result)
    
    def test_format_output_large(self):
        """Test format_output with large value."""
        result = format_output(150)
        self.assertIn("Large value", result)


if __name__ == "__main__":
    unittest.main()

# Made with Bob
