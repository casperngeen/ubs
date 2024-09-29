import json
import logging
import math
import re
import operator
from functools import reduce

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/lisp-parser', methods=['POST'])
def evaluate_parser():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    expressions = data.get('expressions')
    logs = []
    variables = {}
    for i, expression in enumerate(expressions):
        tokenized_expression = tokenize(expression)
        ast = parse(tokenized_expression)
        try:
            evaluate_ast(ast, variables, logs)
        except Exception as e:
            logs.append(f"ERROR at line {i+1}")
            break
    return json.dumps({"output": logs})
    

def is_valid_string(str: str):
    return str.endswith('"') and str.startswith('"')

def tokenize(expression):
    # Tokenize input string using regex to capture parentheses and words
    token_pattern = re.compile(r'[\(\)]|"(?:[^"\\]|\\.)*"|[^\s\(\)]+')
    tokens = token_pattern.findall(expression)
    return [token.strip() for token in tokens]

def parse(tokens):
    # Tokens should be an iterator
    tokens = iter(tokens)
    return parse_tokens(tokens)

def parse_tokens(tokens):
    expression = []
    
    for token in tokens:
        if token == '(':
            # Recursively parse inner expressions
            expression.append(parse_tokens(tokens))
        elif token == ')':
            # End the current list when encountering a closing parenthesis
            return expression
        else:
            # Add individual tokens (int, float, strings, etc.)
            expression.append(parse_token(token))
    
    # If we're parsing the outermost level and there's only one expression, return it directly
    return expression if len(expression) > 1 else expression[0]

def parse_token(token):
    # Handle literals and symbols
    if token.startswith('-') and token[1:].replace('.', '', 1).isdigit():
        if '.' in token:
            return float(token)  # Convert to float if it has a decimal point
        else:
            return int(token)
    elif token.replace('.', '', 1).isdigit():  # Check for both integers and floats
        return float(token) if '.' in token else int(token)
    elif token.startswith('"') and token.endswith('"'):
        return token[1:-1]  # Strip quotes from strings
    elif token in ('true', 'false'):
        return token == 'true'  # Convert 'true'/'false' to boolean
    elif token == 'null':
        return None  # Handle null
    else:
        return token  # For symbols or function names
    
def evaluate_ast(ast, variables, logs):
    if isinstance(ast, list):
        # The first item is the function name
        func = ast[0]
        if func == 'puts':
            str1 = evaluate_ast(ast[1], variables, logs)
            if not isinstance(str1, str):
                raise Exception()
            logs.append(str1)
            return None
        elif func == 'set':
            name = ast[1]
            if name in variables:
                raise Exception()
            value = evaluate_ast(ast[2], variables, logs)
            variables[name] = value
            print(variables)
            return None
        elif func == 'concat':
            str1 = evaluate_ast(ast[1], variables, logs)
            str2 = evaluate_ast(ast[2], variables, logs)
            if not isinstance(str1, str) or not isinstance(str2, str):
                raise Exception()
            return "".join([str1, str2])
        elif func == 'lowercase':
            str1 = evaluate_ast(ast[1], variables, logs)
            if not isinstance(str1, str):
                raise Exception()
            return str1.lower()
        elif func == 'uppercase':
            str1 = evaluate_ast(ast[1], variables, logs)
            if not isinstance(str1, str):
                raise Exception()
            return str1.upper()
        elif func == 'replace':
            str1 = evaluate_ast(ast[1], variables, logs)
            str2 = evaluate_ast(ast[2], variables, logs)
            str3 = evaluate_ast(ast[3], variables, logs)
            if not isinstance(str1, str) or not isinstance(str2, str) or not isinstance(str3, str):
                raise Exception()
            return str1.replace(str2, str3)
        elif func == 'substring':
            str1 = evaluate_ast(ast[1], variables, logs)
            start = evaluate_ast(ast[2], variables, logs)
            stop = evaluate_ast(ast[3], variables, logs)
            if not isinstance(str1, str) or not isinstance(start, int) or not isinstance(stop, int):
                raise Exception()
            if 0 > start or start >= len(str1) or 0 > stop or stop > len(str1) or stop < start:
                raise Exception()
            return str1[start:stop]
        elif func == 'add':
            evaluated_args = [evaluate_ast(arg, variables, logs) for arg in ast[1:]]
            if len(evaluated_args) >= 2 and all(isinstance(arg, (int, float)) for arg in evaluated_args):
                return round(reduce(operator.add, evaluated_args), 4)
            else:
                raise Exception()
        elif func == 'subtract':
            num1 = evaluate_ast(ast[1], variables, logs)
            num2 = evaluate_ast(ast[2], variables, logs)
            if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
                raise Exception()
            return round(num1-num2,4)
        elif func == 'multiply':
            evaluated_args = [evaluate_ast(arg, variables, logs) for arg in ast[1:]]
            if len(evaluated_args) >= 2 and all(isinstance(arg, (int, float)) for arg in evaluated_args):
                return round(reduce(operator.mul, evaluated_args, 1), 4)
            else:
                raise Exception()
        elif func == 'divide':
            num1 = evaluate_ast(ast[1], variables, logs)
            num2 = evaluate_ast(ast[2], variables, logs)
            if num2 == 0 or not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
                raise Exception()
            if isinstance(num1, int) and isinstance(num2, int):
                return math.trunc(num1/num2)
            else:
                return round(num1/num2, 4)
        elif func == 'abs':
            num = evaluate_ast(ast[1], variables, logs)
            if not isinstance(num, (int, float)):
                raise Exception()
            return abs(num)
        elif func == 'max':
            if len(ast) < 2:
                raise Exception()
            evaluated_args = [evaluate_ast(arg, variables, logs) for arg in ast[1:]]
            if all(isinstance(arg, (int, float)) for arg in evaluated_args):
                return max(evaluated_args)
            else:
               raise Exception()
        elif func == 'min':
            if len(ast) < 2:
                raise Exception()
            evaluated_args = [evaluate_ast(arg, variables, logs) for arg in ast[1:]]
            if all(isinstance(arg, (int, float)) for arg in evaluated_args):
                return min(evaluated_args)
            else:
                raise Exception()
        elif func == 'gt':
            if len(ast) == 1:
                raise Exception()
            num1 = evaluate_ast(ast[1], variables, logs)
            num2 = evaluate_ast(ast[2], variables, logs)
            if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
                raise Exception()
            return num1 > num2
        elif func == 'lt':
            if len(ast) == 1:
                raise Exception()
            num1 = evaluate_ast(ast[1], variables, logs)
            num2 = evaluate_ast(ast[2], variables, logs)
            if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
                raise Exception()
            return num1 < num2
        elif func == 'equal':
            op1 = evaluate_ast(ast[1], variables, logs)
            op2 = evaluate_ast(ast[2], variables, logs)
            return op1 == op2
        elif func == 'not_equal':
            op1 = evaluate_ast(ast[1], variables, logs)
            op2 = evaluate_ast(ast[2], variables, logs)
            return op1 != op2
        elif func == 'str':
            op = evaluate_ast(ast[1], variables, logs)
            if op is None:
                return 'null'
            elif op is True:
                return 'true'
            elif op is False:
                return 'false'
            else:
                return str(op)
        else:
            raise NameError(f"Unknown function: {func}")
    else:
        if isinstance(ast, str):
            if ast in variables:
                return variables[ast]  # Variable lookup
            else:
                return ast  # Assume it's a string literal or unquoted string
        else:
            return ast 