"""Transpiler: extract Julia code from Python function source and build callable Julia functions."""

import ast
import inspect
import textwrap
import re


def extract_julia_source(func) -> str:
    """Extract the Julia code string from a decorated function.

    Supports two styles:
    1. Docstring-style: the function body is a single docstring containing Julia code
    2. String-return-style: the function returns a string literal containing Julia code
    """
    source = textwrap.dedent(inspect.getsource(func))
    tree = ast.parse(source)
    funcdef = tree.body[0]
    assert isinstance(funcdef, (ast.FunctionDef, ast.AsyncFunctionDef))

    body = funcdef.body

    # Style 1: docstring body (single Expr(Constant(str)))
    if (len(body) == 1
            and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)):
        return textwrap.dedent(body[0].value.value).strip()

    # Style 2: docstring + pass, or return string
    # Check for docstring as first element
    start = 0
    if (isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)):
        julia_code = textwrap.dedent(body[0].value.value).strip()
        start = 1

        # Remaining should be just `pass` or nothing
        remaining = body[start:]
        if not remaining or (len(remaining) == 1 and isinstance(remaining[0], ast.Pass)):
            return julia_code

    # Style 3: return "..." at the end
    if isinstance(body[-1], ast.Return) and isinstance(body[-1].value, ast.Constant) and isinstance(body[-1].value.value, str):
        return textwrap.dedent(body[-1].value.value).strip()

    raise SyntaxError(
        f"Cannot extract Julia code from function '{func.__name__}'. "
        "Use a docstring body or return a Julia code string."
    )


def build_julia_function(func_name: str, param_names: list[str], julia_body: str) -> str:
    """Build a complete Julia function definition string."""
    params = ", ".join(param_names)
    # If the body already defines a function, use it as-is
    if re.match(r'^\s*function\s', julia_body) or re.match(r'^\s*\w+\(.*\)\s*=', julia_body):
        return julia_body

    indented = textwrap.indent(julia_body, "    ")
    return f"function {func_name}({params})\n{indented}\nend"


def get_param_names(func) -> list[str]:
    """Get parameter names from a Python function."""
    sig = inspect.signature(func)
    return [p.name for p in sig.parameters.values()]
