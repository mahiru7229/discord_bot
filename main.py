from discord.ext import commands, tasks
from dotenv import load_dotenv
import discord
import os
import time
import sys
import logging
import json
import get_prefix
load_dotenv()

def time_for_log():
    return time.strftime("[%H:%M:%S|%m-%d-%Y]")
logging.basicConfig(filename=os.path.join("code","log","log.txt"),
 level=logging.DEBUG,format="{} %(message)s".format(time_for_log()),encoding='utf-8')
intents = discord.Intents.all()
intents.members = True

prefix = get_prefix.prefix()
client = commands.Bot(command_prefix=prefix,intents=intents)

@client.event
async def on_ready():
    print("Bot is logged in !!!")
@client.event
async def on_message(message):
    logging.debug("[DISCORD]{}#{}({})|{}|{}({})|{}".format(message.author.name,message.author.discriminator,message.author.id, message.guild.name,message.channel.name,message.channel.id,message.content))

@client.command(name="shiina")
async def ping(ctx):
    await ctx.reply("**{}** \n`(Ping: {}ms)`".format("Này, có gì không vậy ?",round(client.latency, 1)))

@client.command(name="cash")
async def cash(ctx):
    await isUserExist(str(ctx.author.id))
    log = await openBank()
    
    await ctx.send("{} | Bạn hiện đang có **{:,d}** :banana: ".format(ctx.author.mention,log[str(ctx.author.id)]["money"]))


@client.command(name="about")
async def about(ctx):
    with open(os.path.join("code","about","inf.json"),"r",encoding="utf8") as f:
        inf = json.loads(f.read())
    embed = discord.Embed(title="About the Bot", description="{}".format(inf["description"]),color =discord.Color.green())
    embed.set_author(name="{}".format(inf["authors"]["github"]))
    embed.add_field(name="Version",value=inf["version"])
    embed.add_field(name="Date created: ",value="{}".format(inf["date"]))
    embed.set_footer(text=await get_time())
    await ctx.send(embed=embed)

@client.command(name="give")
async def give(ctx, mention, amount):
    log_1 = mention
    log_1 = log_1.replace("<","")
    log_1 = log_1.replace(">","")
    log_1 = log_1.replace("@","")
    await isUserExist(str(ctx.author.id))
    await isUserExist(str(log_1))
    log = await openBank()
    log[str(ctx.author.id)]["money"] -= int(amount)
    a = log[str(ctx.author.id)]["money"]
    log[str(log_1)]["money"] += int(amount)
    await saveData(log)
    embed = discord.Embed(title="Gửi thành công !", color= discord.Color.from_rgb(255,255,255))
    embed.add_field(name="Số tiền gửi: ", value="{} :banana:".format(int(amount)))
    embed.add_field(name="Số tiền còn lại: ", value="{} :banana:".format(a))
    embed.set_footer(text = await get_time())
async def openBank():
    """Đọc thông tin túi tiền"""
    with open(os.path.join("code","economy","money.json"),"r") as f:
        inf_money = json.loads(f.read())
    return inf_money

async def isUserExist(user_id):
    """Check xem thằng dùng lệnh có tài khoản chưa"""
    log = await openBank()
    if str(user_id) not in log:
        print(user_id)
        log[str(user_id)] = {}
        log[str(user_id)]["money"]= 0
    await saveData(log)



async def saveData(data):
    """Lưu lại số tiền sau khi giao dịch"""
    with open(os.path.join("code","economy","money.json"),"w") as f:
        json.dump(data,f,indent=4)

async def get_time():
    return time.strftime("%a, %b %d, %Y | %H:%M:%S")


client.run(os.getenv("TOKEN"))