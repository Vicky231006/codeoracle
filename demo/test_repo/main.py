"""
Main entry point for the test application.
"""

from utils import calculate_sum, format_output
from config import APP_NAME, VERSION


def main():
    """Main function that orchestrates the application."""
    print(f"{APP_NAME} v{VERSION}")
    
    numbers = [1, 2, 3, 4, 5]
    total = calculate_sum(numbers)
    
    result = format_output(total)
    print(result)
    
    return 0


if __name__ == "__main__":
    exit(main())

# Made with Bob
