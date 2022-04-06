
# ULTIMATE discord bot 
# GOALS:
#       Detect when chavez joins a voice chat and post fuck chavez in the general chat DONE
#       Greet people when they join DONE
#       Give access to certain chats through DM
#           example: I want to join DND chat, DM bot !Join DND, then bot adds me to DND role
#       Play rock paper scissors
#       Play higher/lower
#       User requested insults, !insult, bot responds with a random insult DONE
#       User targetted insults, !insultThem $User, bot insults specified user DONE

# By Myles Becker
# Last updated: 4/6/22

# Requires discord.py and python-dotenv
from typing import List
from dotenv import load_dotenv
import os
import discord 
import random

# Loading secrets
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAVEZ_ID_STR = os.getenv("CHAVEZ_ID")
GENERAL_CHANNEL_ID_STR = os.getenv("GENERAL_CHANNEL_ID")
VOICE_CHANNEL_ID_STR = os.getenv("VOICE_CHANNEL_ID")
# type conversions for integer secrets
CHAVEZ_ID = int(CHAVEZ_ID_STR)
GENERAL_CHANNEL_ID = int(GENERAL_CHANNEL_ID_STR)


print("secret loaded!")

# setting up client
client = discord.Client()

# insult list
insults = ["USER has a goldfish brain!", "USER sucks!", "USER has a tiny pp.", "USER is short.", "USER sucks almost as much as Chavez.", "If I were USER, I'd have depression too."]

# client events
# verify connection
@client.event
async def on_ready():
    print(f'{client.user} has connected.')

# fuck chavez setup
@client.event
async def on_voice_state_update(member, before, after):
    # check is it chavez
    if not before.channel and after.channel and member.id == CHAVEZ_ID:
        # pick the right channel
        channel = client.get_channel(GENERAL_CHANNEL_ID)
        # send the payload bois
        await channel.send("Fuck Chavez!")

# insults
@client.event
async def on_message(message):
    # make sure it doesnt respond to itself
    if message.author == client.user:
        return
    # make sure it's the command
    if message.content.startswith("!insult") or message.content.startswith("!Insult"):
        # common commands->
        # select insult
        user_insult = random.choice(insults)
        # determine what channel it was sent to
        channel_in = client.get_channel(message.channel.id)
        if message.content.startswith("!insultThem"):
            # grab targets name
            target_name = str(message.content)
            # remove command from name
            target_name = target_name.replace("!insultThem ", "")
            # replace USER with target
            user_insult = user_insult.replace("USER", target_name)
            # send the payload bois
            await channel_in.send(user_insult)
        else:
            # grab user's name
            user_name = str(message.author)
            # drop the tag
            user_name = user_name[:-5]
            # replace USER with username in insult
            user_insult = user_insult.replace("USER", user_name)
            # send the payload bois
            await channel_in.send(user_insult)

# welcome new members
@client.event
async def on_member_join(member):
    # set channel to general
    channel = client.get_channel(GENERAL_CHANNEL_ID)
    # send greeting
    await channel.send(f'Hi {member.name}, welcome to Squeebs!')

# run with token
client.run(TOKEN)

