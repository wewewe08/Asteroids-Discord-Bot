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
        #gameboard aesthetics
        image_url = "https://cdn-icons-png.flaticon.com/512/1114/1114780.png"
        icon = ":black_large_square:"
        #grid variables
        grid_size = 7
        #losing condition
        game_over = False

        if gameGrid is not None and user_input is not None and makeEmbed is not None:
            gameboard, arrAsteroid, arrRocket = await gameGrid.makeGrid(grid_size, icon)

            def gridToString(stringVal, gameboard): #take data from the array and convert it into a String
                for row in gameboard:
                    for col in row:
                        for string in col:   
                            stringVal += string
                        stringVal += "\n"
                return stringVal

            #send the gameboard to discord as an EMBED
            origGrid = gridToString(stringVal= "", gameboard = gameboard)
            embed = await makeEmbed.makeEmbed(ctx, origGrid, image_url)
            message = await ctx.send(embed = embed)

            emojis = ["⬅️", "➡️", "💥"] #player input
            for e in emojis:
                await message.add_reaction(emoji = e)      

            #check if the user reacted to the message
            def checkReaction(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in emojis

            def resetEmbed(moveGrid): #update the grid embed once the player reacts
                newGrid = gridToString(stringVal= "", gameboard = moveGrid)
                new_embed = discord.Embed(
                    title = "ASTEROIDS",
                )
                new_embed.timestamp = datetime.datetime.utcnow()
                new_embed.add_field(name = "HOW TO PLAY", value = "react to the messages to move/shoot", inline = False)
                new_embed.add_field(name = "warning:", value = "DO NOT react too fast - if the rocket gets stuck, just react again", inline = False)
                new_embed.add_field(name = "destroy the asteroids to get points", value = newGrid, inline = True)
                new_embed.set_footer(text= f"{ctx.author.name}'s game",icon_url=image_url)
                edited_message = new_embed
                return edited_message

            while not game_over:  
                #spawn asteroids
                moveAsteroid = await user_input.moveAsteroid(gameboard, arrAsteroid)
                await message.edit(embed = resetEmbed(moveAsteroid))
                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout= 20.0, check = checkReaction)
                    if str(reaction.emoji) == '⬅️':
                        move = await user_input.moveLeft(gameboard, arrRocket)
                    elif str(reaction.emoji) == '➡️':
                        move = await user_input.moveRight(gameboard, arrRocket)
                    elif str(reaction.emoji) == '💥':
                        move = await user_input.shootAsteroid(gameboard, arrRocket, arrAsteroid)
                except asyncio.TimeoutError:
                    await ctx.send(f"> **{ctx.author.name}, you didn't react to the message so the game ended.**")
                    break
                else:
                    player = ctx.message.author
                    await message.edit(embed = resetEmbed(move))
                    move = await user_input.resetBoard(gameboard, arrAsteroid)
                    for e in emojis:
                        await message.remove_reaction(e, player)       

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send(f"> **{ctx.author.name},  you are already in a game!**")
def setup(client):
    client.add_cog(Play(client))