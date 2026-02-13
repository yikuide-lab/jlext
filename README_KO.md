# jlext

[中文](README.md) | [English](README_EN.md) | [日本語](README_JA.md)

Numba처럼 Python 함수 안에서 Julia 코드를 직접 작성하고 실행할 수 있습니다.

## 설치

```bash
pip install jlext
```

GitHub에서 최신 버전 설치:

```bash
pip install git+https://github.com/yikuide-lab/jlext.git
```

[Julia](https://julialang.org/downloads/)가 사전에 설치되어 있어야 합니다.

## 빠른 시작

### @julia 데코레이터

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

fibonacci(10)  # → 55, Julia에서 실행
```

### 배치 호출 (24배 속도 향상)

```python
results = fibonacci.map([(10,), (20,), (30,)])
# → [55, 6765, 832040]
```

### 빠른 평가

```python
from jlext import julia_eval, julia_exec

julia_eval("sum(1:100)")     # → 5050
julia_exec("using Statistics")
```

### Julia 패키지 사용

```python
from jlext import JuliaModule

la = JuliaModule("LinearAlgebra")
la.norm([1.0, 2.0, 3.0])  # → 3.7416...
```

## API

| API | 용도 |
|-----|------|
| `@julia` | 데코레이터 — docstring에 Julia 코드 작성 |
| `func.map(args_list)` | 배치 호출, 언어 간 오버헤드 감소 |
| `julia_eval(expr)` | Julia 표현식 평가 (결과 자동 캐시) |
| `julia_exec(code)` | Julia 문 실행 |
| `JuliaModule(name)` | Julia 모듈을 가져와 멤버에 접근 |

## License

MIT
