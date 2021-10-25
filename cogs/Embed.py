import discord
import datetime
from discord.ext import commands

class Embed(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("embed is ready")
    
    async def makeEmbed(self,ctx, grid, url, points, missles):
        embed = discord.Embed(
            title = "ASTEROIDS :rocket: ",
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(name = ":game_die: HOW TO PLAY :game_die: ", value = "1. react to the messages to move/shoot (⬅️, ➡️, 💥) \n2. move the rocket after you shoot an asteroid to respawn them :rock:\n3. shoot the care packages to replenish ammo! ( 📦 )\n4. care packages have a random chance of spawning after shooting a rock.\n5. reach 10 points to win! :medal: ", inline = False)
        embed.add_field(name = "WARNING⚠️", value = "DO NOT react too fast - make sure that the last reaction has reset before reacting again.", inline = False)
        embed.add_field(name = f"🥉POINTS: {points}    📦MISSLES: {missles}", value = grid, inline = True)
        embed.set_footer(text= f"{ctx.author.name}'s game",icon_url=url)
        return embed

    async def resetEmbed(self, ctx, moveGrid, image_url, points, missles): #update the grid embed once the player reacts
        gameGrid = self.client.get_cog("Grid")
        if gameGrid is not None:
            newGrid = await gameGrid.gridToString(stringVal= "", gameboard = moveGrid)
            new_embed = discord.Embed(
                title = "ASTEROIDS :rocket:  ",
            )
            new_embed.timestamp = datetime.datetime.utcnow()
            new_embed.add_field(name = ":game_die: HOW TO PLAY :game_die: ", value = "1. react to the messages to move/shoot (⬅️, ➡️, 💥) \n2. move the rocket after you shoot an asteroid to respawn them :rock:\n3. shoot the care packages to replenish ammo! ( 📦 )\n4. care packages have a random chance of spawning after shooting a rock.\n5. reach 10 points to win! :medal: ", inline = False)
            new_embed.add_field(name = "WARNING⚠️", value = "DO NOT react too fast - make sure that the last reaction has reset before reacting again.", inline = False)
            if points >= 10:
                new_embed.add_field(name = f"🥇POINTS: {points}    📦MISSLES: {missles}", value = newGrid, inline = True) #
            elif points >=  5 and points < 10:
                new_embed.add_field(name = f"🥈POINTS: {points}    📦MISSLES: {missles}", value = newGrid, inline = True)
            else:
                new_embed.add_field(name = f"🥉POINTS: {points}    📦MISSLES: {missles} ", value = newGrid, inline = True)
            new_embed.set_footer(text= f"{ctx.author.name}'s game",icon_url=image_url)
            edited_message = new_embed
            return edited_message

def setup(client):
    client.add_cog(Embed(client))
