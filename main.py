import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from keep_alive import keep_alive

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description="OSAC Music Bot (Beta): Search and Plays music from ytube or a provided custom url",
    intents=intents
)

# async def load_extensions():

@bot.event
async def on_ready():
    print("Logged in as {0} ({0.id})".format(bot.user))
    # loads all the cogs inside the cogs folder on startup
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py")  and filename != "__init__.py":
            await bot.load_extension(f"cogs.{filename[:-3]}")
    print("------")

@bot.command()
async def load(ctx, cname):
    author = str(ctx.message.author.id)
    if author == OWNER_ID:
        bot.load_extension(f"cogs.{cname}")
        await ctx.send(f"Successfully loaded {cname}")
    else:
        await ctx.send("Only the bot owner can use this command.")


@bot.command()
async def unload(ctx, cname):
    author = str(ctx.message.author.id)
    if author == OWNER_ID:
        bot.unload_extension(f"cogs.{cname}")
    else:
        await ctx.send("Only the bot owner can use this command!")


@bot.command()
async def reload(ctx, cname):
    author = str(ctx.message.author.id)
    if author == OWNER_ID:
        bot.unload_extension(f"cogs.{cname}")
        bot.load_extension(f"cogs.{cname}")
        await ctx.send(f"Successfully reloaded {cname}.")
    else:
        await ctx.send("Only the bot owner can use this command!")



bot.run(TOKEN)
