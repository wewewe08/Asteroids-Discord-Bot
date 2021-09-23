#importing
import discord
import logging
import os
from discord import widget

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv() #get env data
BOT_TOKEN = os.getenv("BOT_TOKEN")

#logging errors in the console
logging = logging.basicConfig(level = logging.INFO)

client = commands.Bot(command_prefix = ".")

#startup
@client.event
async def on_ready():
    print("Bot is running.")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.CheckFailure):
        await  ctx.send("> **you do not have permission to use this command.**")
        return

extensions = ["cogs.Play", "cogs.Grid", "cogs.Movement", "cogs.Embed"]
if __name__ == "__main__":
    for ext in extensions:
        client.load_extension(ext)

client.run(BOT_TOKEN)