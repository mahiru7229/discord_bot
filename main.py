from discord.ext import commands, tasks
from dotenv import load_dotenv
import discord
import os
import sys
from commands.json.get_prefix import prefix
load_dotenv()

intents = discord.Intents.all()
intents.members = True

prefix = get_prefix.prefix()
client = commands.Bot(command_prefix=prefix,intents=intents)

@client.event
async def on_ready():
    print("Bot is logged in !!!")


@client.command(name="shiina")
async def ping(ctx):
    await ctx.reply("**{}** \n`(Ping: {}ms)`".format("Này, có gì không vậy ?",round(client.latency, 1)))


client.run(os.getenv("TOKEN"))