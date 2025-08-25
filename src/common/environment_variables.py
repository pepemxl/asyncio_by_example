from typing import Optional
import os
import yaml
if __name__  == '__main__':
    import sys
    package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.append(package_path)
from src.common.constants import CONFIG_FILE_PATH
from src.common.constants import DEFAULT_LOG_LEVEL
from src.common.logger import get_logger


log = get_logger(
    logger_name=__name__,
    logger_caller=__file__,
    level=DEFAULT_LOG_LEVEL,
    flag_stdout=True
)
FLAG_ENV_VARS_LOADED = False


def load_environment_variables_from_local_config():
    global FLAG_ENV_VARS_LOADED
    if os.path.isfile(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "r") as ptr_file:
            env_data = yaml.safe_load(ptr_file)
            config = env_data.get("data")
            os.environ.update(config)
            FLAG_ENV_VARS_LOADED = True
    else:
        log.error("Config file \"{0}\" was not found!".format(CONFIG_FILE_PATH))
        sys.exit(1)


def get_env_var(env_var_key: str, default: Optional[str]=None) -> Optional[str]:
    global FLAG_ENV_VARS_LOADED
    if not FLAG_ENV_VARS_LOADED:
        load_environment_variables_from_local_config()
    try:
        value = os.getenv(env_var_key)
    except Exception as e:
        log.exception("Exception with environment variable with key: {0} Exception:{1}".format(env_var_key, str(e)))
    if value is None:
        log.error("Environment variable with key: {0} was not found!".format(env_var_key))
        if default:
            return default
        return value
    return value


def test_logger():
    log.info("Llamada a modulo {0}".format(__file__))


if __name__ == '__main__':
    test_logger()