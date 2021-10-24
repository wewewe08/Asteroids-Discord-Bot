import discord
import datetime

from discord.ext import commands

class Embed(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("embed is ready")
    
    async def makeEmbed(self,ctx, grid, url):
        embed = discord.Embed(
            title = "ASTEROIDS",
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(name = "HOW TO PLAY", value = "1. react to the messages to move/shoot\n2. move the rocket after you shoot an asteroid to respawn them.", inline = False)
        embed.add_field(name = "warning:", value = "DO NOT react too fast - if the rocket gets stuck, just react again", inline = False)
        embed.add_field(name = "destroy the asteroids to get points", value = grid, inline = True)
        embed.set_footer(text= f"{ctx.author.name}'s game",icon_url=url)
        return embed

def setup(client):
    client.add_cog(Embed(client))
