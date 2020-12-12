import json
import sys
import subprocess
import time
import logging

from .version import __version__
from .xmrig_api_client import XmrigClient

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

RESOLUTION_SEC = 5
MAXIMUM_PROFILE_TIMEOUT_SEC = 60
MINIMUM_PROFILE_TIMEOUT_SEC = 10
assert RESOLUTION_SEC < MINIMUM_PROFILE_TIMEOUT_SEC

activated = False
xmrig_http_client = XmrigClient('http://127.0.0.1:8810', 'foobar')
logger = logging.getLogger()


def run(command, timeout=None):
    return subprocess.run(
        command,
        shell=True,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        timeout=timeout,
    )


def has_dependency(program: str):
    res = run(f'which {program}')
    return res.returncode == 0


def get_idle_time_sec():
    res = run("xprintidle")
    idle_time_sec = int(res.stdout) / 1000
    return idle_time_sec


def is_active():
    return activated


def activate():
    global activated, xmrig_http_client
    with open('maximum-config.json') as max_json_file:
        max_config = json.load(max_json_file)
        xmrig_http_client.set_config(max_config)
    logger.info("activate")
    activated = True


def deactivate():
    global activated
    with open('minimum-config.json') as min_json_file:
        min_config = json.load(min_json_file)
        xmrig_http_client.set_config(min_config)
    logger.info("deactivate")
    activated = False


if __name__ == "__main__":
    if sys.platform == 'linux' and not has_dependency('xprintidle'):
        logger.info('you have to install xprintidle first')
        sys.exit(1)

    try:
        while True:
            idle_time_sec = get_idle_time_sec()
            logger.info(f"idle for {idle_time_sec} seconds")

            if idle_time_sec > MAXIMUM_PROFILE_TIMEOUT_SEC:
                if not is_active():
                    activate()

            if is_active():
                if idle_time_sec < MINIMUM_PROFILE_TIMEOUT_SEC:
                    deactivate()

            time.sleep(RESOLUTION_SEC)
    except KeyboardInterrupt:
        logger.info('program stopped by user')
