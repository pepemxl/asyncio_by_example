import os
import sys
import setproctitle



api_root_path = os.path.abspath(os.path.dirname(__file__))
project_root_path = os.path.abspath(os.path.join(api_root_path, '..'))
if project_root_path not in sys.path:
    sys.path = [project_root_path]+[path for path in sys.path if path not in {'', '.', api_root_path, project_root_path}]

print(sys.meta_path)