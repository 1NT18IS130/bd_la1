import os
import json
# import database
import discord
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Bot
from database import Database
import mongoengine
from spotipy.oauth2 import SpotifyClientCredentials
import cogs.spotify
import spotipy


with open("config.json", "r") as f:
    config = json.load(f)

# start the discord client
client = discord.Client()

# bot prefix, for eg h!hello
bot = commands.Bot(command_prefix=config['prefix'])

client = mongoengine.connect(host="mongodb://127.0.0.1:27017/bdproj")
Database(client)


for filename in os.listdir("cogs"):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(config['discord_token'])