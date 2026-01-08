"""Top-level shim for `src.data_loader` used by tests.
"""
try:
    from src.data_loader import *  # noqa: F401,F403
except Exception:  # fallback for direct import when running outside package
    from importlib import import_module
    _mod = import_module("src.data_loader")
    globals().update({k: getattr(_mod, k) for k in dir(_mod) if not k.startswith("_")})
