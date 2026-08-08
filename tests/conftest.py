import os
import pathlib
import sys

# Add the src directory to sys.path so that imports like 'src.app.main' work
src_path = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(src_path))
