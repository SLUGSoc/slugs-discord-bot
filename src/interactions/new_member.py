from discord import Member

from src.config import ServerConfig

def challenge_message(member: Member, server_config: ServerConfig) -> str:
    challenge_str = (
        f"Hello {member.mention}!\n" +
        f"Welcome to the official Discord server for **SLUGSoc**: " +
        f"the **S**heffie**L**d **U**niversity **G**aming **SOC**iety.\n" +
        f"Please read the server rules posted in {server_config.rules_channel}, then come back here and post the phrase " +
        f"**{server_config.challenge_response}** to gain access."
    )
    return challenge_str

def intro_message(member: Member) -> str:
    return f"Welcome, {member.mention}! Enjoy your stay!"