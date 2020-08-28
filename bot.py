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
async def on_raw_message_delete(payload):
    logging_channel = client.get_channel(botinfo.logging_channel_id)
    
    message = payload.cached_message
    message_id = payload.message_id
    channel = client.get_channel(channel_id)

    if type(message) == None:
        delete_string = ">>> ```css\n> [MESSAGE DELETED]\n> A message was deleted from {0}, but this message was not found in the message cache.\n> - Message ID: {1}```".format(channel.mention, message_id)
    else:
        delete_string = ">>> ```css\n>[MESSAGE DELETED]\n> The following message was deleted from {0}:\n> {1}\n> [Message ID:] {2}```".format(channel.mention, message, message_id)
    await logging_channel.send(delete_string)

async def on_message_edit(before, after):
    logging_channel = client.get_channel(botinfo.logging_channel_id)
    if before.content == after.content:
        return # Edit detects many subtle changes to the message object, but we only care about the actual words being changed
    edit_string = '>>> ```bash\n> "MESSAGE EDITED"\n> The following message was edited in {0}:\n> "Before:" {1}\n> "After:" {2}\n> "Message ID:" {3}'.format(channel.mention, before.content, after.content, after_id)
    await logging_channel.send(edit_string)

async def on_member_remove(member):
    logging_channel = client.get_channel(botinfo.logging_channel_id)
    leave_string = ">>> ```ini\n> [USER LEFT]\n> {0} has left the server.\n> [User ID:] {1}".format(member.mention, member.id)
    await logging_channel.send(leave_string)

token = botinfo.token
client.run(token)
