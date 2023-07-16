"""
SNPE Environment Setup and Sanity Checks for needed dependencies versions.
"""

from logging import raiseExceptions
import re
import subprocess
import sys, os
from icecream import ic
from packaging import version

from .exec_utils import exec_shell_cmd, get_host_type
from .logger_config import logger


def get_env_var(env_var_name):
    env_var = os.environ.get(env_var_name)
    if not env_var:
        # logger.error(f"\n{env_var_name} is not set ...\n")
        env_var = input(f"\nEnter path for {env_var_name}: \n")
        if not os.path.isdir(env_var):
            get_env_var()

    return env_var


def get_onnx_dir():
    try:
        import onnx
        return str(onnx.__file__).replace("/__init__.py", "")
    except ImportError as ie:
        logger.critical(f"Not able to import ONNX : {ie}")
        logger.critical("Press CTRL + C to exit and install ONNX or \n")
        return get_env_var("ONNX_DIR")


def get_snpe_version() -> str:
    try:
        output = subprocess.check_output(["snpe-net-run", "--version"], universal_newlines=True, env=os.environ)
        snpe_version = output.strip().split()[1] # eg: ['SNPE', 'v2.7.0.4264']
        return snpe_version
    except Exception as e:
        logger.error("Not able to get SNPE version using cmd : 'snpe-net-run --version' ")
        logger.info("Please run <SNPE_ROOT>/bin/envsetup.sh script")


def check_adb_version() -> bool:
    try:
        output = subprocess.check_output(["adb", "version"], universal_newlines=True)
        match = re.search(r'version (\d+\.\d+\.\d+)', output) # eg: Android Debug Bridge version 1.0.41
        if match:
            adb_version = match.group(1)
            logger.debug(f"ADB version = {adb_version}")
        else:
            raise RuntimeError('Could not extract ADB version')
    
        if version.parse(adb_version) >= version.parse("1.0.39"):
            return True
        else:
            raise RuntimeError('Please install ADB with version >= 1.0.39')

    except Exception as e:
        raise RuntimeError("Not able to get ADB version using cmd : 'adb version' ")


def check_python_version():
    python_version = sys.version_info
    snpe_version = get_snpe_version()

    if version.parse(snpe_version) <= version.parse("v2.10"):
        if not (python_version[0] == 3 and python_version[1] == 6):
            logger.warning('SNPE Converters : unsupported Python version: {}'.format(python_version), 
                            'till SNPE-2.10, expected Python version == 3.6')

    elif version.parse(snpe_version) >= version.parse("v2.11"):
        if not (python_version[0] == 3 and python_version[1] == 8):
            logger.warning('SNPE Converters : unsupported Python version: {}'.format(python_version), 
                            'SNPE-2.11 and higher expects Python version == 3.8')

def setup_snpe_env():
    SNPE_ROOT = get_env_var("SNPE_ROOT")
    ic(SNPE_ROOT)
    ONNX_DIR = get_onnx_dir()
    ic(ONNX_DIR)

    setup_cmd = f"source {SNPE_ROOT}/bin/envsetup.sh -o {ONNX_DIR}"
    
    if exec_shell_cmd(setup_cmd) == 0:
    
        #=====> Add the new path to PYTHONPATH
        current_pythonpath = os.environ.get('PYTHONPATH', '')
        new_pythonpath = f"{SNPE_ROOT}/lib/python"
        updated_pythonpath = f"{current_pythonpath}:{new_pythonpath}" if current_pythonpath else new_pythonpath
        ic(updated_pythonpath)

        # Update the value of PYTHONPATH
        os.environ['PYTHONPATH'] = updated_pythonpath
        sys.path.append(f"{SNPE_ROOT}/lib/python")

        #=====> Add the new path to PATH
        current_path = os.environ.get('PATH', '')
        new_path = f"{SNPE_ROOT}/bin/{get_host_type().value}"
        updated_path = f"{current_path}:{new_path}" if current_path else new_path
        ic(updated_path)

        # Update the value of PATH
        os.environ['PATH'] = updated_path

        #=====> Add the new path to LD_LIBRARY_PATH
        ld_lib_path = os.environ.get('LD_LIBRARY_PATH', '')
        new_lb_lib_path = f"{SNPE_ROOT}/lib/{get_host_type().value}"
        updated_ld_lib_path = f"{ld_lib_path}:{new_lb_lib_path}" if ld_lib_path else new_lb_lib_path
        ic(updated_ld_lib_path)

        # Update the value of PATH
        os.environ['LD_LIBRARY_PATH'] = updated_ld_lib_path

        return SNPE_ROOT
    else:
        raise RuntimeError(f"Not able to set SNPE ENV. Please run this cmd manually:\n {setup_cmd}")


class SnpeEnv:
    _SNPE_ROOT = setup_snpe_env()

    @property
    def SNPE_ROOT(self):
        return self._SNPE_ROOT

    @SNPE_ROOT.setter
    def SNPE_ROOT(self, value):
        if self._SNPE_ROOT is None:
            self._SNPE_ROOT = value
        else:
            raise ValueError("Cannot reassign the value of SNPE_ROOT")

    def __init__(self):
        do_sanity_checks()
        set_sanity_checks_passed()
        # if sanity_checks_passed():
        #     if SnpeEnv._SNPE_ROOT is None:
        #         SnpeEnv._SNPE_ROOT = setup_snpe_env
        # else:
        #     do_sanity_checks()
        #     set_sanity_checks_passed()
        #     SnpeEnv._SNPE_ROOT = setup_snpe_env


def do_sanity_checks():
    # Perform sanity checks
    check_python_version()


def sanity_checks_passed():
    return hasattr(SnpeEnv, '_sanity_checks_passed') and SnpeEnv._sanity_checks_passed


def set_sanity_checks_passed():
    SnpeEnv._sanity_checks_passed = True

