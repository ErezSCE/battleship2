import sys
import os
# Add the src directory to sys.path so that imports like 'src.app.main' work
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(src_path)
