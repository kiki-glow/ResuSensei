"""json_safe.py

Helpers to ensure data structures are JSON-serializable.

This project stores several Python dict/list payloads into SQLAlchemy JSON columns.
Some computed values come from NumPy (e.g. np.float64), which may not be JSON-serializable
by database drivers. This module converts NumPy scalar types into native Python types.
"""

from __future__ import annotations

from typing import Any


def json_safe(value: Any) -> Any:
    """Recursively convert a value into something JSON-serializable.

    - Converts NumPy scalar types (np.generic) into native Python scalars.
    - Recursively converts dicts/lists/tuples.
    - Leaves other types unchanged.
    """

    # NumPy scalars
    try:
        import numpy as np  # type: ignore

        if isinstance(value, np.generic):
            return value.item()
    except Exception:
        # If numpy isn't available or type detection fails, just continue.
        pass

    # Containers
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}

    if isinstance(value, list):
        return [json_safe(v) for v in value]

    if isinstance(value, tuple):
        return [json_safe(v) for v in value]

    # Primitive types / everything else
    return value

