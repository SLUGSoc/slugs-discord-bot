import os
import yaml

import discord
from discord import Client, Guild, Role, TextChannel

from src.constants import CONFIG_DIR, ROOT_DIR
from src.logger import logger

token_path = os.path.join(ROOT_DIR, "token.yaml")
with open(token_path, "r") as token_file:
    token = yaml.safe_load(token_file).get("token")

class ServerConfig:
    @staticmethod
    def load_configs(client: Client):
        server_configs: dict[int: ServerConfig] = {}

        config_files = os.listdir(CONFIG_DIR)
        for cfg_filename in config_files:
            if cfg_filename == "config_template.yaml":
                continue

            cfg_filepath = os.path.join(CONFIG_DIR, cfg_filename)
            try:
                cfg = ServerConfig(cfg_filepath, client)
                server_configs[cfg.guild.id] = cfg
            except (discord.ClientException, RuntimeError) as err:
                logger.error(
                    f"Failed to load server config {cfg_filename}: {err}"
                )
        return server_configs

    def __init__(self, config_filepath: str, client: Client):
        with open(config_filepath, "r") as cfg_file:
            cfg_yaml: dict[str, str | int | dict] = yaml.safe_load(cfg_file)

        self.challenge_response: str = cfg_yaml["info"]["challenge"]

        self.guild: Guild = client.get_guild(cfg_yaml["info"]["guild"])
        if not self.guild:
            raise RuntimeError(
                f"Could not get details for guild with ID: {cfg_yaml["info"]["guild"]}. " +
                f"Has the bot been invited to this server?"
            )

        self.audit_channel: TextChannel = client.get_channel(cfg_yaml["channels"]["audit"])
        self.challenge_channel: TextChannel = client.get_channel(cfg_yaml["channels"]["challenge"])
        self.intro_channel: TextChannel = client.get_channel(cfg_yaml["channels"]["intro"])
        self.rules_channel: TextChannel = client.get_channel(cfg_yaml["channels"]["rules"])

        self.privileged_role: Role = self.guild.get_role(cfg_yaml["roles"]["privileged"])
        self.member_role: Role = self.guild.get_role(cfg_yaml["roles"]["member"])

        self.auth_secrets = cfg_yaml["google_auth"]
