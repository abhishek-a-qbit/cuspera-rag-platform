"""Top-level shim for `src.vector_store` used by tests.
"""
try:
    from src.vector_store import *  # noqa: F401,F403
except Exception:
    from importlib import import_module
    _mod = import_module("src.vector_store")
    globals().update({k: getattr(_mod, k) for k in dir(_mod) if not k.startswith("_")})
