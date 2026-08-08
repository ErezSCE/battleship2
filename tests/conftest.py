import sys
from pathlib import Path
# Add the src directory to sys.path so that imports like 'src.app.main' work
src_path = Path(__file__).resolve().parents[1]
sys.path.append(str(src_path))
