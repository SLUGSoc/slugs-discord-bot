from os import makedirs, path
from shutil import copy

from src.constants import CONFIG_DIR, ROOT_DIR, TEMPLATE_DIR
from src.logger import logger

makedirs(CONFIG_DIR, exist_ok=True)

setup_required = False

token_filepath = path.join(ROOT_DIR, "token.yaml")
if path.isfile(token_filepath):
    token_template = path.join(TEMPLATE_DIR, "token_template.yaml")
    copy(token_template, token_filepath)

    setup_required = True
    logger.info("Generated /token.yaml file. Please populate token field and restart the application.")

if len(CONFIG_DIR) == 0:
    config_template = path.join(TEMPLATE_DIR, "config_template.yaml")
    config_dst = path.join(CONFIG_DIR, "config0.yaml")
    copy(config_template, config_dst)

    setup_required = True
    logger.info(
        "No server configs were detected, so a new one has been created in /server_configs. Please populate " +
        "the fields within and restart the application."
    )
