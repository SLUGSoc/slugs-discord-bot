#!/usr/bin/env python3

import discord
import botinfo
import sqlite3
import time
import os

start_time = time.localtime()
print(os.getcwd())
print(time.asctime(start_time))

client = discord.Client()

@client.event
async def on_ready():
    print("Ready.")

@client.event
async def on_member_join(member):
    join_channel = client.get_channel(botinfo.join_channel_id)
    rules_channel = client.get_channel(botinfo.rules_channel_id)
    await join_channel.send(botinfo.gatekeep(member.mention, rules_channel.mention))

@client.event
async def on_message(message):
    if message.author == client.user: # No  R E C U R S I O N  allowed
        return

    channel = message.channel
    content = message.content

    member = message.author
    name = member.name

    main_channel = client.get_channel(botinfo.main_channel_id)

    if 'would you kindly' in content.lower():
        if channel == client.get_channel(botinfo.join_channel_id):
            guild = client.get_guild(botinfo.guild_id)
            member_role = guild.get_role(botinfo.member_role_id)

            roles = member.roles
            if member_role not in roles:
                await member.add_roles(member_role)
                await main_channel.send(botinfo.welcome(member.mention))

# Logging Channel
@client.event
async def on_raw_message_delete(payload):
    logging_channel = client.get_channel(botinfo.logging_channel_id)
    
    message = payload.cached_message.replace("@","*@*") # Stops logged messages mentioning people
    channel = client.get_channel(payload.channel_id)

    if message is None:
        delete_string = ">>> ```css\n[MESSAGE DELETED] [Message ID:] {0}```A message was deleted from {1}, but this message was not found in the message cache.\n".format(payload.message_id, channel.mention)
    else:
        delete_string = ">>> ```css\n[MESSAGE DELETED] [Message ID:] {0} [User ID:] {1}```The following message from **{2}** was deleted from {3}:\n*{4}*".format(message.id, message.author.id, str(message.author), channel.mention, message.content)
    await logging_channel.send(delete_string)

@client.event
async def on_message_edit(before, after):
    logging_channel = client.get_channel(botinfo.logging_channel_id)
    message_bef = before.content.replace("@","*@*")
    message_aft = after.content.replace("@","*@*")

    channel = after.channel
    if before.content == after.content:
        return # Edit detects many subtle changes to the message object, but we only care about the actual words being changed
    edit_string = '>>> ```css\n"MESSAGE EDITED" "Message ID:" {0}```The following message by **{1}** was edited in {2}:\n\n**Before:**\n*{3}*\n\n**After:**\n*{4}*\n'.format(after.id, (after.author), channel.mention, message_bef, message_aft)
    await logging_channel.send(edit_string)

@client.event
async def on_member_remove(member):
    logging_channel = client.get_channel(botinfo.logging_channel_id)
    leave_string = ">>> ```ini\n[USER LEFT] [User ID:] {1}```{0} has left the server.".format(member.mention, member.id)
    await logging_channel.send(leave_string)

token = botinfo.token
client.run(token)
