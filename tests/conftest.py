"""Pytest configuration.

Ensures the project root is on sys.path so test modules can import the `scripts` package
without requiring the user to install the package.
"""

import os
import sys
from pathlib import Path

# Add the repository root to sys.path for test imports.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
