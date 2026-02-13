"""jlext - Write Julia code in Python functions, like Numba but for Julia."""

from .decorator import julia, julia_eval, julia_exec, JuliaModule

__all__ = ["julia", "julia_eval", "julia_exec", "JuliaModule"]
