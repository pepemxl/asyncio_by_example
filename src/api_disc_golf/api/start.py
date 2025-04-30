import os
import sys
import setproctitle


API_ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
project_root_path = os.path.abspath(os.path.join(API_ROOT_PATH, '..'))
if project_root_path not in sys.path:
    sys.path = [project_root_path]+[path for path in sys.path if path not in {'', '.', API_ROOT_PATH, project_root_path}]

print(sys.meta_path)


