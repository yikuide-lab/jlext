"""Julia runtime bridge - lazy singleton managing the Julia process."""

import threading
from functools import lru_cache


class _JuliaRuntime:
    """Lazy singleton that initializes Julia on first use."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def _ensure_init(self):
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    from juliacall import Main, convert, newmodule
                    self._Main = Main
                    self._seval = Main.seval
                    self._convert = convert
                    self._newmodule = newmodule
                    self._initialized = True

    @property
    def Main(self):
        self._ensure_init()
        return self._Main

    @property
    def convert(self):
        self._ensure_init()
        return self._convert

    def newmodule(self, name):
        self._ensure_init()
        return self._newmodule(name)

    def seval(self, code: str):
        """Evaluate Julia expression via cached seval reference."""
        self._ensure_init()
        return self._seval(code)

    # Alias
    eval = seval

    def exec(self, code: str):
        """Execute Julia statements (no return value expected)."""
        self.seval(code)

    @lru_cache(maxsize=256)
    def _resolve_func(self, func_name: str):
        """Resolve and cache a Julia function object by name."""
        return self.seval(func_name)

    def call(self, func_name: str, *args):
        """Call a Julia function by name with Python arguments."""
        return self._resolve_func(func_name)(*args)


runtime = _JuliaRuntime()
