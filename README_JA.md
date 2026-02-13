# jlext

[中文](https://github.com/yikuide-lab/jlext/blob/main/README.md) | [English](https://github.com/yikuide-lab/jlext/blob/main/README_EN.md) | [한국어](https://github.com/yikuide-lab/jlext/blob/main/README_KO.md)

Numbaのように、Python関数内でJuliaコードを直接記述・実行できます。

## インストール

```bash
pip install jlext
```

GitHubから最新版をインストール：

```bash
pip install git+https://github.com/yikuide-lab/jlext.git
```

事前に [Julia](https://julialang.org/downloads/) のインストールが必要です。

## クイックスタート

### @julia デコレータ

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

fibonacci(10)  # → 55、Juliaで実行
```

### バッチ呼び出し（24倍高速化）

```python
results = fibonacci.map([(10,), (20,), (30,)])
# → [55, 6765, 832040]
```

### クイック評価

```python
from jlext import julia_eval, julia_exec

julia_eval("sum(1:100)")     # → 5050
julia_exec("using Statistics")
```

### Juliaパッケージの利用

```python
from jlext import JuliaModule

la = JuliaModule("LinearAlgebra")
la.norm([1.0, 2.0, 3.0])  # → 3.7416...
```

## API

| API | 用途 |
|-----|------|
| `@julia` | デコレータ — docstringにJuliaコードを記述 |
| `func.map(args_list)` | バッチ呼び出し、言語間オーバーヘッドを削減 |
| `julia_eval(expr)` | Julia式を評価（結果は自動キャッシュ） |
| `julia_exec(code)` | Julia文を実行 |
| `JuliaModule(name)` | Juliaモジュールをインポートしメンバーにアクセス |

## License

MIT
