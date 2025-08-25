import os
if __name__  == '__main__':
    import sys
    package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.append(package_path)
from src.common.constants import PATH_STRUCTURE
from src.common.logger import get_logger


log = get_logger(__file__, "INFO")


def create_local_folder(path_structure = PATH_STRUCTURE):
    if path_structure is None:
        return False
    for item in path_structure:
        path = item.get('path', None)
        if path:
            if not os.path.isdir(path):
                log.info("Creating path: {0}".format(path))
                try:
                    os.mkdir(path)
                except Exception as e:
                    log.exception("Error creating path: {0} with exception: {1}".format(path, str(e)))
        children = item.get('children', None)
        if children:
            create_local_folder(children)


if __name__ == '__main__':
    create_local_folder()