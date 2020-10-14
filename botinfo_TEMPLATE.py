#!/usr/bin/env python3

token = "" # str, secret token associated with application
guild_id = 0 # int, id of operating server
join_channel_id = 0 # int, id of channel where gatekeep challenge is issued
intro_channel_id = 0 # int, id of channel where users are introduced after correct response
bot_channel_id = 0 # int, id of channel where bot should interact with users (does nothing atm)
rules_channel_id = 0 # int, id of channel that users are guided to in the challenge
logging_channel_id = 0 # int, id of channel where all logging messages are sent
member_role_id = 0 # int, id of server role that is given to users who successfully respond to the challenge

def welcome(user): # Message sent in intro channel after a successful response from user
        return "Welcome to this server, {0}".format(user)

def gatekeep(user, rules): # Message sent in join channel to user upon joining
        return "Hi {0}. Go to {1} for server rules, the respond with **'open sesame'** or whatever, this is just an example.".format(user,rules)

challenge_response = 'open sesame'
