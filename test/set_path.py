import sys
import os

def set_path_to_root():
    # Get the absolute path of the parent directory
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # Add the parent directory to sys.path
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)