#!/usr/bin/env python3

import discord
import botinfo # Info file containing sensitive info and customized settings
import sqlite3
import time
import os
import gauth
from discord.ext import commands

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

    if botinfo.challenge_response in content.lower(): # I couldn't resist
        if channel == client.get_channel(botinfo.join_channel_id):
            guild = client.get_guild(botinfo.guild_id)
            member_role = guild.get_role(botinfo.member_role_id)

            roles = member.roles
            if member_role not in roles:
                intro_channel = client.get_channel(botinfo.intro_channel_id)
                
                await member.add_roles(member_role)
                await intro_channel.send(botinfo.welcome(member.mention))

# Logging Channel
@client.event
async def on_raw_message_delete(payload):
    logging_channel = client.get_channel(botinfo.logging_channel_id)
    
    message = payload.cached_message
    channel = client.get_channel(payload.channel_id)

    if message is None: # Occurs when message cannot be retrieved message cache
        delete_string = ">>> ```css\n[MESSAGE DELETED] [Message ID:] {0}```A message was deleted from {1}, but this message was not found in the message cache.\n".format(payload.message_id, channel.mention)
    else:
        noment_message = message.content.replace("@","*@*") # Stops logged messages mentioning users
        delete_string = ">>> ```css\n[MESSAGE DELETED] [Message ID:] {0} [User ID:] {1}```The following message from **{2}** was deleted from {3}:\n*{4}*".format(message.id, message.author.id, str(message.author), channel.mention, noment_message)
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

bot = commands.Bot(command_prefix='%')

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def auth(context, arg):
    logging_channel = client.get_channel(botinfo.logging_channel_id)
    member = context.author
    data = gauth.get_database()
    options = list()
    names = list()
    for d in data:
        options.append(str(len(options)))
        names.append(d[0])

    if arg.lower() == "list":
        options_list = list()
        for o in options:
            option = "**{})** {}".format(o, names[int(o)])
            options_list.append(option)
        options_string = '\n'.join(options_list)
        await logging_channel.send(options_string)

    elif arg.lower() in options:
        code = gauth.generate_codes(arg)

    else:
        await logging_channel.send("Invalid argument. Please select a number from `RON! auth list`.")

token = botinfo.token
client.run(token)
