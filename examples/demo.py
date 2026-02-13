"""Examples demonstrating jlext usage."""

from jlext import julia, julia_eval, julia_exec, JuliaModule


# ============================================================
# 1. Basic: @julia decorator - write Julia in a Python function
# ============================================================

@julia
def add(x, y):
    """
    return x + y
    """

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

@julia
def matrix_multiply(A, B):
    """
    return A * B
    """


# ============================================================
# 2. julia_eval - quick one-liner evaluation
# ============================================================

def demo_eval():
    print("sqrt(2) =", julia_eval("sqrt(2.0)"))
    print("π =", julia_eval("π"))
    print("range sum =", julia_eval("sum(1:100)"))


# ============================================================
# 3. julia_exec + JuliaModule - use Julia packages
# ============================================================

def demo_linear_algebra():
    la = JuliaModule("LinearAlgebra")
    v = julia_eval("[1.0, 2.0, 3.0]")
    print("norm =", la.norm(v))
    print("dot =", la.dot(v, v))


# ============================================================
# 4. Complex Julia function with type annotations
# ============================================================

@julia(name="mandelbrot_pixel")
def mandelbrot(c_re, c_im, max_iter):
    """
    z_re, z_im = 0.0, 0.0
    for i in 1:max_iter
        if z_re*z_re + z_im*z_im > 4.0
            return i
        end
        z_re, z_im = z_re*z_re - z_im*z_im + c_re, 2.0*z_re*z_im + c_im
    end
    return max_iter
    """


if __name__ == "__main__":
    print("=== @julia decorator ===")
    print(f"add(3, 4) = {add(3, 4)}")
    print(f"fibonacci(10) = {fibonacci(10)}")

    print("\n=== julia_eval ===")
    demo_eval()

    print("\n=== JuliaModule ===")
    demo_linear_algebra()

    print("\n=== Mandelbrot ===")
    print(f"mandelbrot(0.0, 0.0, 100) = {mandelbrot(0.0, 0.0, 100)}")
    print(f"mandelbrot(0.5, 0.5, 100) = {mandelbrot(0.5, 0.5, 100)}")

    print("\n=== Batch .map() ===")
    results = fibonacci.map([(10,), (20,), (30,)])
    print(f"fibonacci.map([(10,), (20,), (30,)]) = {results}")
