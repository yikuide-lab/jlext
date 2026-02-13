"""Benchmark jlext performance."""
import time
from jlext import julia, julia_eval, JuliaModule


@julia
def fib(n):
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


# Warm up
fib(10)

N = 1_000

# --- Single calls ---
t0 = time.perf_counter()
for _ in range(N):
    fib(30)
t1 = time.perf_counter()
single_time = t1 - t0
print(f"@julia fib(30) x {N} single calls: {single_time:.3f}s  ({single_time/N*1e6:.1f} µs/call)")

# --- Batch .map() ---
args_list = [(30,)] * N
t0 = time.perf_counter()
results = fib.map(args_list)
t1 = time.perf_counter()
batch_time = t1 - t0
print(f"@julia fib(30) x {N} batch .map(): {batch_time:.3f}s  ({batch_time/N*1e6:.1f} µs/call)")
print(f"Speedup: {single_time/batch_time:.1f}x")

# --- julia_eval cache ---
julia_eval("sqrt(2.0)")
t0 = time.perf_counter()
for _ in range(10_000):
    julia_eval("sqrt(2.0)")
t1 = time.perf_counter()
print(f"\njulia_eval cached x 10000: {t1-t0:.4f}s  ({(t1-t0)/10_000*1e6:.2f} µs/call)")

# --- JuliaModule attr cache ---
la = JuliaModule("LinearAlgebra")
v = julia_eval("[1.0, 2.0, 3.0]")
la.norm(v)
t0 = time.perf_counter()
for _ in range(10_000):
    la.norm(v)
t1 = time.perf_counter()
print(f"JuliaModule.norm() x 10000: {t1-t0:.4f}s  ({(t1-t0)/10_000*1e6:.2f} µs/call)")

print(f"\nSelf-replacing __call__ active: {fib.__call__.__func__.__name__ == '_call_compiled'}")
