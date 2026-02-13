# jlext

[English](https://github.com/yikuide-lab/jlext/blob/main/README_EN.md) | [日本語](https://github.com/yikuide-lab/jlext/blob/main/README_JA.md) | [한국어](https://github.com/yikuide-lab/jlext/blob/main/README_KO.md)

像 Numba 一样，在 Python 函数中直接编写和运行 Julia 代码。

## 安装

```bash
pip install jlext
```

也可以从 GitHub 安装最新版：

```bash
pip install git+https://github.com/yikuide-lab/jlext.git
```

需要预先安装 [Julia](https://julialang.org/downloads/)。

## 快速开始

### @julia 装饰器

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

fibonacci(10)  # → 55，在 Julia 中执行
```

### 批量调用（24x 加速）

```python
results = fibonacci.map([(10,), (20,), (30,)])
# → [55, 6765, 832040]
```

### 快速求值

```python
from jlext import julia_eval, julia_exec

julia_eval("sum(1:100)")     # → 5050
julia_exec("using Statistics")
```

### 使用 Julia 包

```python
from jlext import JuliaModule

la = JuliaModule("LinearAlgebra")
la.norm([1.0, 2.0, 3.0])  # → 3.7416...
```

## API

| API | 用途 |
|-----|------|
| `@julia` | 装饰器，函数体用 docstring 写 Julia 代码 |
| `func.map(args_list)` | 批量调用，减少跨语言开销 |
| `julia_eval(expr)` | 求值 Julia 表达式（结果自动缓存） |
| `julia_exec(code)` | 执行 Julia 语句 |
| `JuliaModule(name)` | 导入 Julia 模块并访问其成员 |

## License

MIT
