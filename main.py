from src.setup import setup_required
if setup_required:
    exit()

import discord
from discord import (
    Member, Message,
    RawMemberRemoveEvent, RawMessageDeleteEvent, RawMessageUpdateEvent
)
from discord.ext import commands

from src.config import ServerConfig, token
from src.constants import APP_NAME
from src.interactions.msg_audit import MessageTemplates
from src.interactions.new_member import challenge_message, intro_message
from src.logger import logger

intents = discord.Intents(
    guilds=True,
    members=True,
    messages=True,
    message_content=True,
)

client = commands.Bot(command_prefix='%', intents=intents)
server_configs: dict[int: ServerConfig]
@client.event
async def on_ready():
    global server_configs
    server_configs = ServerConfig.load_configs(client)
    logger.info(f"{APP_NAME} online. Listening...")


# --- Audit events ---
@client.event
async def on_message_edit(before: Message, after: Message):
    if before.content == after.content:
        """
        Per https://discordpy.readthedocs.io/en/stable/api.html#discord.on_message_edit, many events trigger this, 
        however we only care about changes to message content.
        """
        return
    server_config: ServerConfig = server_configs.get(after.guild.id)

    embed = MessageTemplates.edit(before, after)
    await server_config.audit_channel.send(embed=embed)

@client.event
async def on_raw_message_edit(payload: RawMessageUpdateEvent):
    server_config: ServerConfig = server_configs.get(payload.guild_id)

    if getattr(payload, "cached_message", None) is not None:
        return  # Editing a message in cache will trigger on_message_edit

    msg_channel = server_config.guild.get_channel(payload.channel_id)
    embed = MessageTemplates.edit_raw(payload.message_id, msg_channel)
    await server_config.audit_channel.send(embed=embed)

@client.event
async def on_message_delete(message: Message):
    if message.author == client.user:
        return

    server_config: ServerConfig = server_configs.get(message.guild.id)
    embed = MessageTemplates.delete(message)
    await server_config.audit_channel.send(embed=embed)

@client.event
async def on_raw_message_delete(payload: RawMessageDeleteEvent):
    server_config: ServerConfig = server_configs.get(payload.guild_id)

    if getattr(payload, "cached_message", None) is not None:
        return  # Deleting a message in cache will trigger on_message_delete

    msg_channel = server_config.guild.get_channel(payload.channel_id)
    embed = MessageTemplates.delete_raw(payload.message_id, msg_channel)
    await server_config.audit_channel.send(embed=embed)

@client.event
async def on_member_remove(member: Member):
    server_config: ServerConfig = server_configs.get(member.guild.id)
    embed = MessageTemplates.member_leave(member)
    await server_config.audit_channel.send(embed=embed)

@client.event
async def on_raw_member_remove(payload: RawMemberRemoveEvent):
    if getattr(payload, "user", None) is not None:
        return  # A cached user leaving will trigger on_member_remove

    server_config: ServerConfig = server_configs.get(payload.guild_id)
    embed = MessageTemplates.member_leave_raw()
    await server_config.audit_channel.send(embed=embed)


# --- Join challenge events ---
@client.event
async def on_member_join(member: Member):
    server_config: ServerConfig = server_configs.get(member.guild.id)
    await server_config.challenge_channel.send(challenge_message(member, server_config))

@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    server_config: ServerConfig = server_configs.get(message.guild.id)
    if (
            message.content.lower().strip() == server_config.challenge_response  # Correct challenge given
            and message.channel == server_config.challenge_channel  # In the challenge channel
            and server_config.member_role not in message.author.roles  # Not already a member
    ):
        await message.author.add_roles(server_config.member_role, reason="Passed new member challenge.")
        await server_config.intro_channel.send(intro_message(message.author))

    await client.process_commands(message)


# --- Google Auth Integration ---
@client.command()
async def auth(context: commands.Context):
    server_config: ServerConfig = server_configs.get(context.guild.id)
    if (
        context.message.channel != server_config.audit_channel or
        context.message.author.roles[-1] < server_config.privileged_role
    ):
        return

    await server_config.audit_channel.send(
        embed=MessageTemplates.auth_message(server_config.auth_secrets),
        delete_after=30
    )



if __name__ == "__main__":
    logger.info(f"Starting {APP_NAME}...")
    client.run(token=token, log_handler=None)
