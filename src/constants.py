from os import path

APP_NAME = "slugsnet"

ROOT_DIR = path.dirname(  # slugs-discord-bot
    path.dirname(  # slugs-discord-bot\src
        __file__  # slugs-discord-bot\src\constants.py
    )
)

CONFIG_DIR = path.join(ROOT_DIR, "server_configs")
LOG_DIR = path.join(ROOT_DIR, "logs")
TEMPLATE_DIR = path.join(ROOT_DIR, "config_templates")
