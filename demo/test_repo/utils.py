"""
Utility functions for the test application.
"""


def calculate_sum(numbers):
    """
    Calculate the sum of a list of numbers.
    
    Args:
        numbers: List of numbers to sum
        
    Returns:
        Sum of all numbers
    """
    total = 0
    for num in numbers:
        total += num
    return total


def format_output(value):
    """
    Format a value for output.
    
    Args:
        value: Value to format
        
    Returns:
        Formatted string
    """
    if value > 100:
        return f"Large value: {value}"
    elif value > 10:
        return f"Medium value: {value}"
    else:
        return f"Small value: {value}"


def helper_function():
    """A helper function that does something."""
    pass

# Made with Bob
