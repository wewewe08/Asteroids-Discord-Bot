import discord
import asyncio
import datetime

from discord.ext import commands

class Play(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("play is ready")

    @commands.command()
    #1 command running per user
    @commands.max_concurrency(number = 1, per=commands.BucketType.user, wait=False)
    async def play(self, ctx):
        #cog variables
        gameGrid = self.client.get_cog("Grid")
        user_input = self.client.get_cog("Movement")
        makeEmbed = self.client.get_cog("Embed")
        asteroid = self.client.get_cog("Asteroid")
        #gameboard aesthetics
        image_url = "https://cdn-icons-png.flaticon.com/512/1114/1114780.png"
        icon = ":black_large_square:"
        #grid variables
        grid_size = 7
        #losing condition
        game_over = False

        if gameGrid is not None and user_input is not None and makeEmbed is not None and asteroid is not None:
            #setting the array variables for the grids
            gameboard, arrAsteroid, arrRocket = await gameGrid.makeGrid(grid_size, icon)

            #send the gameboard to discord as an EMBED
            origGrid = await gameGrid.gridToString(stringVal= "", gameboard = gameboard)
            embed = await makeEmbed.makeEmbed(ctx, origGrid, image_url)
            message = await ctx.send(embed = embed)

            emojis = ["⬅️", "➡️", "💥"] #player input
            for e in emojis:
                await message.add_reaction(emoji = e)      

            #check if the user reacted to the message
            def checkReaction(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in emojis

            while not game_over:  
                #move asteroids (ARCHIVED)
                #generator = await asteroid.moveAsteroid(gameboard, arrAsteroid)
                #for item in generator:
                #    await message.edit(embed = resetEmbed(item))
                #    await asyncio.sleep(1)
                asteroidShot = False
                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout= 20.0, check = checkReaction)
                    if str(reaction.emoji) == '⬅️':
                        move = await user_input.moveLeft(gameboard, arrRocket)
                    elif str(reaction.emoji) == '➡️':
                        move = await user_input.moveRight(gameboard, arrRocket)
                    elif str(reaction.emoji) == '💥':
                        move = await asteroid.shootAsteroid(gameboard, arrRocket, arrAsteroid)
                        asteroidShot = True
                except asyncio.TimeoutError:
                    await ctx.send(f"> **{ctx.author.name}, you didn't react to the message so the game ended.**") #afk player
                    break
                else:
                    player = ctx.message.author
                    reset_embed = await makeEmbed.resetEmbed(ctx, move, image_url)
                    await message.edit(embed = reset_embed) #reset grid
                    move, arrAsteroid = await asteroid.resetBoard(gameboard, arrAsteroid, arrRocket, grid_size, icon, asteroidShot)
                    for e in emojis:
                        await message.remove_reaction(e, player)   
                        asteroidShot = False    

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send(f"> **{ctx.author.name},  you are already in a game!**") #player tried to run the play command more than once
def setup(client):
    client.add_cog(Play(client))
