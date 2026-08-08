import sys
import pathlib
# Add the src directory to sys.path so that imports like 'src.app.main' work
src_path = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(src_path))
