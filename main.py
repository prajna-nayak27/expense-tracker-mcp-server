from fastmcp import FastMCP
import random
import json

# fastmcp server instance
mcp = FastMCP("CalculatorServer", "A simple calculator server using FastMCP")

# Tool: Add two numbers
@mcp.tool()
def add(a: float, b: float) -> float:
    """ Add two numbers and return the result. 

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of the two numbers.
    """
    return a + b

# Tool: Subtract two numbers
@mcp.tool()
def subtract(a: float, b: float) -> float:
    """ Subtract the second number from the first and return the result. 

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The result of the subtraction.
    """
    return a - b

# Tool: Multiply numbers
@mcp.tool()
def multiply(numbers: list[float]) -> float:
    """ Multiply multiple numbers and return the result. 

    Args:
        numbers (list[float]): A list of numbers to multiply.

    Returns:
        float: The product of all the numbers.
    """
    result = 1
    for num in numbers:
        result *= num
    return result


# Tool: Generate a random number within a range
@mcp.tool()
def random_number(min_value: int=1, max_value: int=100) -> int:
    """ Generate a random integer between min_value and max_value. 
    Args:
        min_value (int): The minimum value of the range.
        max_value (int): The maximum value of the range.
    Returns:
        int: A random integer within the specified range.
    """
    return random.randint(min_value, max_value)


# Tool: Server information
@mcp.resource("info://server")
def server_info() -> str:
    """ Provide information about the calculator server.

    Returns:
        str: A JSON string containing server information.
    """
    info = {
        "name": "CalculatorServer",
        "version": "1.0",
        "description": "A simple calculator server using FastMCP",
        "tools": ["add", "subtract", "multiply", "random_number"],
        "author": "Pnayak"
    }
    return json.dumps(info, indent=4)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
