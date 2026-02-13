# jlext

[中文](README.md) | [日本語](README_JA.md) | [한국어](README_KO.md)

Write and run Julia code directly inside Python functions, just like Numba.

## Installation

```bash
pip install jlext
```

Or install the latest version from GitHub:

```bash
pip install git+https://github.com/yikuide-lab/jlext.git
```

[Julia](https://julialang.org/downloads/) must be installed beforehand.

## Quick Start

### @julia Decorator

```python
from jlext import julia

@julia
def fibonacci(n):
    """
    if n <= 1
        return n
    end
    a, b = 0, 1
    for _ in 2:n
        a, b = b, a + b
    end
    return b
    """

fibonacci(10)  # → 55, executed in Julia
```

### Batch Calls (24x Speedup)

```python
results = fibonacci.map([(10,), (20,), (30,)])
# → [55, 6765, 832040]
```

### Quick Evaluation

```python
from jlext import julia_eval, julia_exec

julia_eval("sum(1:100)")     # → 5050
julia_exec("using Statistics")
```

### Using Julia Packages

```python
from jlext import JuliaModule

la = JuliaModule("LinearAlgebra")
la.norm([1.0, 2.0, 3.0])  # → 3.7416...
```

## API

| API | Description |
|-----|-------------|
| `@julia` | Decorator — write Julia code in the function docstring |
| `func.map(args_list)` | Batch calls, reducing cross-language overhead |
| `julia_eval(expr)` | Evaluate a Julia expression (results are cached) |
| `julia_exec(code)` | Execute Julia statements |
| `JuliaModule(name)` | Import a Julia module and access its members |

## License

MIT
