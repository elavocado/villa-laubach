"""Compatibility entry point. Prefer python scripts/build.py."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).parent / "scripts" / "build.py"), run_name="__main__")
