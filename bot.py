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
        rules_mention = rules_channel.mention
        mention = member.mention
        await join_channel.send(botinfo.gatekeep(mention, rules_mention))

@client.event
async def on_message(message):
	if message.author == client.user: # No  R E C U R S I O N  allowed
		return
	
	channel = message.channel
	content = message.content
	
	member = message.author
	name = member.name
	mention = member.mention

	main_channel = client.get_channel(botinfo.main_channel_id)
	
	if 'would you kindly' in content.lower():
		if channel == client.get_channel(botinfo.join_channel_id):
			guild = client.get_guild(botinfo.guild_id)
			member_role = guild.get_role(botinfo.member_role_id)
			
			roles = member.roles
			if member_role not in roles:
				await member.add_roles(member_role)
				await main_channel.send(botinfo.welcome(mention))

token = botinfo.token
client.run(token)
