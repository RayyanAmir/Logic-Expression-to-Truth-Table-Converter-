# Logical Expression to Truth Table Converter

This Python project is designed to parse logical expressions and generate truth tables, which are crucial for understanding and verifying logical operations in discrete mathematics. The converter supports various logical operations, including NOT, AND, OR, XOR, IMPLIES, and IFF, and can handle complex nested expressions.

## Features

1. **Supports Multiple Logical Operations**
   - Includes NOT, AND, OR, XOR, IMPLIES, and IFF.

2. **Variable Detection**
   - Automatically detects variables in the expression.

3. **Intermediate Expression Evaluation**
   - Evaluates and displays intermediate expressions in the truth table.

4. **User-Friendly Input**
   - Accepts logical expressions in a user-friendly format.

## Files

- **logic_converter.py**
  - Main script containing the logic for parsing expressions, evaluating them, and generating the truth table.

## Getting Started

### Prerequisites

- Python 3.x installed on your system.
- `pyparsing` library installed. You can install it using pip:
  ```sh
  pip install pyparsing
##Enter a logical expression when prompted:
Enter a logical expression: A AND B -> C

##Expression Parsing
The script uses pyparsing to define the grammar and parse logical expressions. The following classes represent different types of logical operations:

-BoolOperand: Represents a variable in the expression.
-BoolBinOp: Base class for binary operations.
-BoolNot: Represents the NOT operation.
-BoolAnd: Represents the AND operation.
-BoolOr: Represents the OR operation.
-BoolXor: Represents the XOR operation.
-BoolImplies: Represents the IMPLIES operation.
-BoolIff: Represents the IFF operation.

##Usage
Input Expression: The user is prompted to enter a logical expression.
Generate Truth Table: The script parses the expression, evaluates it for all possible combinations of variable values, and prints the truth table along with intermediate expression evaluations.

##Contribution
-Feel free to contribute to the project by submitting issues and pull requests. Follow the standard GitHub contribution guidelines.

##License
-This project is licensed under the MIT License - see the LICENSE file for details.
