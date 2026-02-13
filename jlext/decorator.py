"""Core decorator and utilities for jlext."""

import functools
from functools import lru_cache
from .runtime import runtime
from .transpiler import extract_julia_source, build_julia_function, get_param_names

# Global counter to avoid Julia namespace collisions for same-named functions
_name_counter: dict[str, int] = {}


def _unique_jl_name(base: str) -> str:
    """Generate a unique Julia function name to avoid global namespace collisions."""
    count = _name_counter.get(base, 0)
    _name_counter[base] = count + 1
    return f"_jlext_{base}_{count}" if count else f"_jlext_{base}"


class JuliaFunction:
    """A compiled Julia function callable from Python."""

    def __init__(self, py_func, julia_code: str, jl_func_name: str):
        self._py_func = py_func
        self.julia_code = julia_code
        self.jl_func_name = jl_func_name
        self._jl_fn = None
        self._jl_map_fn = None
        functools.update_wrapper(self, py_func)

    def _compile(self):
        runtime.exec(self.julia_code)
        self._jl_fn = runtime.seval(self.jl_func_name)
        # Generate a vectorized map wrapper for batch calls
        map_name = f"{self.jl_func_name}__map"
        runtime.exec(
            f"{map_name}(args_list) = [Base.invokelatest({self.jl_func_name}, a...) for a in args_list]"
        )
        self._jl_map_fn = runtime.seval(map_name)
        # Replace __call__ to skip future compile checks
        self.__call__ = self._call_compiled

    def _call_compiled(self, *args):
        return self._jl_fn(*args)

    def __call__(self, *args):
        self._compile()
        return self._jl_fn(*args)

    def map(self, args_list: list[tuple]) -> list:
        """Batch call: execute the Julia function for each args tuple in one cross-language round-trip.

        Example:
            results = fib.map([(10,), (20,), (30,)])
        """
        if self._jl_fn is None:
            self._compile()
        return list(self._jl_map_fn(args_list))

    def __repr__(self):
        return f"<JuliaFunction {self.jl_func_name}>"


def julia(func=None, *, name=None):
    """Decorator to define a Julia function using Python syntax.

    Usage:
        @julia
        def my_add(x, y):
            '''
            return x + y
            '''

        result = my_add(1, 2)  # Runs in Julia!
    """
    def decorator(fn):
        jl_name = name or _unique_jl_name(fn.__name__)
        params = get_param_names(fn)
        julia_body = extract_julia_source(fn)
        julia_code = build_julia_function(jl_name, params, julia_body)
        return JuliaFunction(fn, julia_code, jl_name)

    if func is not None:
        return decorator(func)
    return decorator


@lru_cache(maxsize=512)
def julia_eval(code: str):
    """Evaluate a Julia expression and return the result (cached).

    Example:
        julia_eval("sqrt(2.0)")
    """
    return runtime.seval(code)


def julia_exec(code: str):
    """Execute Julia statements.

    Example:
        julia_exec("using LinearAlgebra")
    """
    runtime.exec(code)


class JuliaModule:
    """Proxy to access Julia module members as attributes.

    Example:
        la = JuliaModule("LinearAlgebra")
        la.norm([1.0, 2.0, 3.0])
    """

    def __init__(self, module_name: str):
        runtime.exec(f"using {module_name}")
        self._name = module_name
        self._mod = runtime.seval(module_name)
        self._cache: dict[str, object] = {}

    def __getattr__(self, name: str):
        if name.startswith("_"):
            raise AttributeError(name)
        cached = self._cache.get(name)
        if cached is not None:
            return cached
        val = getattr(self._mod, name)
        self._cache[name] = val
        return val

    def __repr__(self):
        return f"<JuliaModule {self._name}>"
