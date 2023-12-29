import os
from distutils.util import strtobool
import supervisely as sly
from dotenv import load_dotenv

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api: sly.Api = sly.Api.from_env()

WORKSPACE_ID = sly.env.workspace_id()

ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ABSOLUTE_PATH)
sly.logger.debug(f"Absolute path: {ABSOLUTE_PATH}, parent dir: {PARENT_DIR}")

TEMP_DIR = os.path.join(PARENT_DIR, "temp")
sly.fs.mkdir(TEMP_DIR, remove_content_if_exists=True)
sly.logger.debug(f"App starting... TEMP dir: {TEMP_DIR}")

IS_DEFAULT_SETTINGS = bool(strtobool(os.getenv("modal.state.defaultSettings")))
DEFAULT_GROUP_NAME = "multiview"
GROUP_TAG_NAME = os.environ.get("modal.state.groupTagName", "")
SYNC_IMAGES = bool(strtobool(os.getenv("modal.state.syncImages")))
