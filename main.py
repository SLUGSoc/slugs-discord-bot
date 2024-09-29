import discord
from discord.ext import commands

from src.logger import logger

client = commands.Bot(command_prefix='%', intents=discord.Intents.default())

if __name__ == "__main__":
    logger.info("Starting slugsnet...")
    client.run(token="", log_handler=None)
