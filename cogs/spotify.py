import discord
import json
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from database import Database
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random


class SpotifyAPI():
    '''
    Implements the features which require to interface with the Spotify API
    '''
    def __init__(self, sp):
        self.sp = sp

    def get_recommendations_for_artist(self, artist):
        '''
        Get recommendations for a particular artist
        '''
        print(artist)
        artist_info = self.sp.search(artist, limit=1)
        artist_uri = artist_info['tracks']['items'][0]['album']['artists'][0]['id']
        print(artist_uri)
        results = self.sp.recommendations(seed_artists=[artist_uri])
        rand_album = random.choice(results["tracks"])
        rand_track = rand_album['external_urls']['spotify']
        print(rand_track)
        return rand_track

class SpotifyCommands(commands.Cog):
    '''
    Implements the discord commands for Spotify Commands
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def afa(self, ctx):
        '''
        Add favourite artist function
        '''
        await ctx.send('Enter your favourite artists comma seperated')

        def check(msg):
            return msg.author.id == ctx.author.id

        msg = await self.bot.wait_for("message", check=check)#, timeout=30)
        print(msg.content)
        print(ctx.author)
        artists = msg.content.split(",")
        data = {
            "discord_id" : str(ctx.author),
            "artists": artists
        }
        Database.add_data(data)
        await ctx.send(f"You can now get recommendations for {msg.content}")


    @commands.command()
    async def show(self, ctx):
        '''
        show/list all artists
        '''
        avail_data = Database.get_data(str(ctx.author))
        if avail_data != None:
            i = 1
            msg = "Here are your favourite artists:\n"
            
            for x in avail_data:
                appnd = f"{i}) {x}\n"
                msg = msg + appnd
                i += 1
            await ctx.send(f"{msg}")

    @commands.command()
    async def rec(self, ctx):
        '''
        Get recs for an artist querying the DB for the user's artists list
        '''
        avail_data = Database.get_data(str(ctx.author))
        print(avail_data)
        # print(ctx.author)
        if avail_data != None:
            # artist = spot.get_artist(random.choice(avail_data))
            artist = random.choice(avail_data)
            if artist:
                msg = spot.get_recommendations_for_artist(artist)
                await ctx.send(f"Recommendation for **{artist}**\n{msg}")
            else:
                print(artist)
                print("Can't find that artist!")
    
    @commands.command()
    async def remove(self, ctx):
        '''
        remove a selected artist
        '''
        avail_data = Database.get_data(str(ctx.author))
        if avail_data != None:
            i = 1
            msg = "Here are your favourite artists, select their numbers to delete from list:\n"
            
            for x in avail_data:
                appnd = f"{i}) {x}\n"
                msg = msg + appnd
                i += 1
            await ctx.send(f"{msg}")

            def check(msg):
                return msg.author.id == ctx.author.id
            try:
                resp = await self.bot.wait_for("message", check=check, timeout=15)
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond!")
                return

            try:
                val = [int(x)-1 for x in resp.content.split(',')]
                data = {
                            'discord_id': str(ctx.author),
                            'value': []
                        }
                for each in val:
                    if each >= 0 and each < len(avail_data):
                        data['value'].append(avail_data[each])
                        ret = Database.del_data(data)
                        if ret != None:
                            await ctx.send("Delete successful!")
                        else:
                            await ctx.send("Delete failed!")
            except ValueError or TypeError:
                await ctx.send("Hey! That wasn't valid! Restart the command again.")
        else:
            await ctx.send("You have no favourite artists :(")
                

with open("config.json", "r") as f:
    spot_config = json.load(f)


client_credentials_manager = SpotifyClientCredentials(client_id=spot_config['spotify_client'], client_secret=spot_config['spotify_secret'])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
spot = SpotifyAPI(sp)


def setup(bot):
    bot.add_cog(SpotifyCommands(bot))