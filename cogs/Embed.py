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

    async def resetEmbed(self, ctx, moveGrid, image_url): #update the grid embed once the player reacts
        gameGrid = self.client.get_cog("Grid")
        if gameGrid is not None:
            newGrid = await gameGrid.gridToString(stringVal= "", gameboard = moveGrid)
            new_embed = discord.Embed(
                title = "ASTEROIDS",
            )
            new_embed.timestamp = datetime.datetime.utcnow()
            new_embed.add_field(name = "HOW TO PLAY", value = "1. react to the messages to move/shoot\n2. move the rocket after you shoot an asteroid to respawn them.", inline = False)
            new_embed.add_field(name = "warning:", value = "DO NOT react too fast - if the rocket gets stuck, just react again", inline = False)
            new_embed.add_field(name = "destroy the asteroids to get points", value = newGrid, inline = True)
            new_embed.set_footer(text= f"{ctx.author.name}'s game",icon_url=image_url)
            edited_message = new_embed
            return edited_message

def setup(client):
    client.add_cog(Embed(client))
