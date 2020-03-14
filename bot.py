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
	name = member.name
	await member.send(botinfo.welcome(name))



token = botinfo.token
client.run(token)