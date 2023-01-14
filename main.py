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

intents = discord.Intents.all()
intents.members = True

prefix = get_prefix.prefix()
client = commands.Bot(command_prefix=prefix,intents=intents)

@client.event
async def on_ready():
    print("Bot is logged in !!!")
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    logging.basicConfig(filename=os.path.join("code","log","log.txt"),
 level=logging.DEBUG,format="{} %(message)s".format(time_for_log()),encoding='utf-8')
    logging.debug("{}#{}({})|{}|{}({})|{}".format(message.author.name,message.author.discriminator,message.author.id, message.guild.name,message.channel.name,message.channel.id,message.content))
    await client.process_commands(message)
@client.event
async def on_message_edit(bf,af):
    logging.basicConfig(filename=os.path.join("code","log","log.txt"),level=logging.DEBUG,format="{} %(message)s".format(time_for_log()),encoding='utf-8')
    logging.debug("{}#{}({}) (EDITED)|{}|{}({})|{} (edited)--> {}".format(bf.author.name,bf.author.discriminator,bf.author.id, bf.guild.name,bf.channel.name,bf.channel.id,bf.content,af.content))

@client.event
async def on_message_delete(message):
    snipe = await get_snipe()
    snipe["author"] = "{}#{}".format(message.author.name, message.author.discriminator)
    snipe["message_content"] = message.content
    snipe["message_id"] = message.id
    snipe["author_id"] = message.author.id
    with open(os.path.join("code","snipe","snipe.json"),"w") as f:
        json.dump(snipe,f,indent=4)

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

@client.command()
async def coin(ctx):
    print(ctx.message.attachments[0].url)
    await ctx.send("work")

@client.command(name="snipe")
async def snipe(ctx):
    snipe_ = await get_snipe()
    user_pfp = await client.fetch_user(snipe_["author_id"])
    embed = discord.Embed(color=discord.Color.from_rgb(12, 225, 232))
    embed.set_author(name="Người gửi: {}".format(snipe_["author"]), icon_url=user_pfp.avatar)
    embed.add_field(name="Content: ", value=snipe_["message_content"])
    embed.set_footer(text="Message ID: {} | Author ID: {}".format(snipe_["message_id"], snipe_["author_id"]))
    await ctx.send(embed=embed)
@client.command(name="kick")
@commands.has_permissions(kick_members= True)
async def kick(ctx, userName: discord.User,*,reason):
    await ctx.guild.kick(userName)
    try: 
        embed = discord.Embed(title="Bạn đã kick {}".format(userName),color=discord.Color.from_rgb(12, 225, 232))
        embed.add_field(name="Lý do:", value=reason)
        embed.set_footer(text=await get_time())
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title="Bạn đã kick {}".format(userName),color=discord.Color.from_rgb(12, 225, 232))
        embed.add_field(name="Lý do:", value="")
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
async def get_snipe():
    with open(os.path.join("code","snipe","snipe.json"),"r") as f:
        return json.loads(f.read())

client.run(os.getenv("TOKEN"))