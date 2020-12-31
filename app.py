import os
import discord
from discord.ext import commands
import random,requests,json
import asyncio

bot = commands.Bot(command_prefix="!",description="ThunderbirdBot")

@bot.event
async def on_ready():
    print(f"You're logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game("Type !helpme"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith("hello"):
        await message.channel.send(f"{message.author.mention} Hello!")
    elif message.content == "!social":
        embed = discord.Embed(title="Social Medias", description="Social Media Links", color=0x00ff00)
        embed.add_field(name="Twitter",value="https://twitter.com/0gulcancicek")
        embed.add_field(name="Github",value="https://github.com/ogulcancicek")
        embed.add_field(name="Twitch",value="https://www.twitch.tv/thunderbirdss")
        embed.set_thumbnail(url="https://pluralsight.imgix.net/paths/python-7be70baaac.png")
        await message.channel.send(embed=embed)
    else:
        await bot.process_commands(message)

@bot.command()
async def x(message):
    chance = random.randint(1,7)
    if chance % 2 == 0:
        await message.channel.send(f"You passed,mate! {message.author.mention}")
    else:
        await message.channel.send(f"You are 100% son of a bitch!,{message.author.mention}")

@bot.command()
async def whatabout(ctx):
    if "@" in ctx.message.content:
        randint = random.randint(0,2)
        tagged_user = ctx.message.content.split()[1]
        if randint == 0:
            rsp = requests.get("https://api.datamuse.com/words?rel_jjb=person")
            adjectives = rsp.json()
            adj = random.choice(adjectives)
            await ctx.channel.send(f"{tagged_user} is a {adj['word']} person")
        else:
            await ctx.channel.send(f"{tagged_user} is my ortaam.")
    else:
        await ctx.channel.send(f"{ctx.guild.mention} please tag someone after !whatabout command!!")

@bot.command(pass_context=True)
async def notification(ctx):
    mgs = []
    with open("notifications.txt") as file: 
        for line in file:
            try:
                wrds = line.split(",")
                mgs.append((wrds[0],wrds[1].strip("\n")))
            except:
                continue
    channel = bot.get_channel(141618596462854145)
    while True:
        msg,role_name = random.choice(mgs)
        if "@" not in role_name:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            await channel.send(f"> {role.mention} {msg}")
        else:
            await channel.send(f"> {role_name} {msg}")
        await asyncio.sleep(600)

@commands.has_permissions(administrator=True)
@bot.command(pass_context=True)
async def clear(ctx,amount):
    if int(amount) > 50:
        amount = 50
    await ctx.channel.purge(limit=int(amount))

@commands.has_permissions(administrator=True)
@bot.command()
async def slowmode(ctx,delay:int):
    await ctx.channel.edit(slowmode_delay=delay)
    await ctx.channel.send(f"Set the slowmode delay in this channel to {delay} seconds!")

@commands.has_permissions(administrator=True)
@bot.command()
async def add_notification(ctx,*args):
    msg = " ".join(args[:-1])
    mention = args[-1]
    with open("notifications.txt","a") as file:
        file.write(f"{msg},{mention}\n")
    await ctx.channel.send(f"> {msg} has been added.")

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx,member:discord.Member,reason=None):
    bot_id = 788870059073732638
    if member == bot.get_user(id=bot_id):
        await ctx.channel.send(f"> {ctx.message.author.mention} siktir lan kıvrak. You can not kick me!")
    else:
        await member.kick(reason=reason)
        await ctx.channel.send(f"> {member.display_name} has been kicked.")

@bot.command()
async def year2020(ctx):
    await ctx.channel.send(f"> 2020 yılının anasını sikim. {ctx.author.mention} Sana bi' şey olmasın ortaam. ")

@bot.command()
async def helpme(ctx):
    embed = discord.Embed(Title="Commands",description="Bot commands:",color=0xfc3903)
    embed.add_field(name="!x",value="Try your chance against us!\n",inline=False)
    embed.add_field(name="!whatabout @mention",value="Learn something about your friends\n",inline=False)
    embed.add_field(name="!notification",value="Show notification every 240 seconds\n",inline=False)
    embed.add_field(name="!add_notification",value="Add some new notifications to our list\n",inline=False)
    embed.add_field(name="!clear x",value="Remove x messages from chat!\n",inline=False)
    embed.add_field(name="!slowmode x",value="Set slowmode of channel to x seconds\n",inline=False)
    embed.add_field(name="!social",value="Show the creator's social media address.\n",inline=False)
    await ctx.channel.send(embed=embed)
    
bot.run(os.environ["DISCORD_TOKEN"])
