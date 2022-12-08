import discord
from discord.ext import commands
from discord.utils import get
import random
import time
import replit
import keep_alive
import asyncio
import rainPoem
import blockindexes
import os
import alarm
import commandStuff
import requests
import worlds
import terraingeneration
import define
from mutagen.mp3 import MP3
import search_google.api
from discord_slash import SlashCommand, SlashContext
import gtts

# variables
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='t/', intents=intents)
slash = SlashCommand(bot, sync_commands=True)
guild_ids = [555157545044672513]
# Set developer key and CSE ID
dev_key = os.getenv("GOOGLEKEY")
cse_id = os.getenv("GOOGLEID")

buildargs = {
    'serviceName': 'customsearch',
    'version': 'v1',
    'developerKey': dev_key
}

botspeed = ['','','','','','']
reactions = [
    '◀️', '🔼', '🔽', '▶️', '⬅️', '⬆️', '⬇️', '➡️', '↖️', '↗️', '⏹', '⏺'
]

# Setting up the array of blocks that will be used by the bot.
emotes = blockindexes.blockIndex
emotes.append("<:P0:766679476956168232>")  # player
emotes.append("<a:p0rout:809126203973828640>")  # going out right
emotes.append("<a:p0lin:809126204132687892>")  # coming in left
emotes.append("<a:p0uout:809126203587559455>")  # going out up
emotes.append("<a:p0din:809126203725971488>")  # coming in down
emotes.append("<a:p0lout:809126203981692928>")  # going out left
emotes.append("<a:p0rin:809126203969110016>")  # coming in right
emotes.append("<a:p0dout:809126203586773034>")  # going out down
emotes.append("<a:p0uin:809126204014985266>")  # coming in up

pindex = 47
"""selected = 1
px = 0
py = 0
pxpast = 0
pypast = 0
delayNum = 3
removereact = 0

columnCount = 8
rowCount = 8
cameraX = 0
cameraY = 0
mapmessage = None
selectmessage = None
dimension = "overworld"
"""


@bot.event
async def on_ready():
    replit.clear()
    os.system('clear')
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    bot.remove_command('help')
    englishChannel = bot.get_channel(742410232550129786)
    info = discord.Activity(name="Gage", type=3)
    await bot.change_presence(status=discord.Status.dnd, activity=info)
    #await alarm.checkTime(englishChannel)
    return


@bot.event
async def on_message(message):
  global botspeed
  if (message.author.bot and message.content == "vroom vroom"):
    botspeed.append(message.author.name)
    botspeed.pop(0)
  if (message.author == bot.user):
    return
  if message.content.startswith("heyoo"):
    await asyncio.sleep(5)
    await message.channel.send("hiya")
  elif "~race" in message.content:
      await message.channel.send("vroom vroom")
      await asyncio.sleep(1)
      for i in range(6):
        if botspeed[0] == "":
          botspeed.append("")
          botspeed.pop(0)
      await message.channel.send(f"```     LEADERBOARD     \n=====================\n🥇 {botspeed[0]}\n🥈 {botspeed[1]}\n🥉 {botspeed[2]}\n4. {botspeed[3]}\n5. {botspeed[4]}\n6. {botspeed[5]}\n=====================```")
      botspeed = ['','','','','','']
  elif "~mourne*" in message.content:
    await message.channel.send("F")
  elif "~consult" in message.content:
    await message.channel.send(random.choice(["Yes","No","Definitely","Perhaps not","Strongly against","Totally","Of course"]))
  elif "~movie" in message.content:
    await movie(await bot.get_context(message))
  elif (message.author.bot and message.content.startswith("~")):
    await asyncio.sleep(3)
    try:
      await message.channel.send(rainPoem.rain(message.content))
    except:
      await message.channel.send("The End")
  elif (message.author.bot and message.content.startswith("​")):
    await asyncio.sleep(3)
    await talk(await bot.get_context(message))

  if (not message.author.bot and message.content.__contains__("ngrok")):
    await mcserver(await bot.get_context(message), message.content)

  if(message.content.startswith("[h hack")):
    member = message.guild.get_member(840251081195651082)
    webhook = await message.channel.create_webhook(name=member.name)
    await webhook.send(
      "Hack successful, Gage is now hacked.", username=member.name, avatar_url=member.avatar_url)

    await webhook.delete()

  if(message.content.startswith("Join my coop game on Bloons TD 6!")):
    await message.channel.send(message.content[61:])
    await message.delete()
  await bot.process_commands(message)


@bot.command()
async def test(ctx):
    await ctx.send("Hi")

@bot.command()
async def botrace(ctx):
    await ctx.send(f"```     LEADERBOARD     \n=====================\n🥇 {botspeed[0]}\n🥈 {botspeed[1]}\n🥉 {botspeed[2]}\n4. {botspeed[3]}\n5. {botspeed[4]}\n=====================```")


@bot.command()
async def eng(ctx):
    await alarm.eng(ctx)

@bot.command()
async def english(ctx):
    await alarm.english(ctx)


@slash.slash(name="english",
             description="How much time until d̶e̶a̶t̶h̶  english?", guild_ids=guild_ids)
async def _english(ctx: SlashContext):
    await alarm.english(ctx)


@bot.command()
async def essay(ctx):
    await alarm.essay(ctx)


@bot.command()
async def delay(ctx, *arg: int):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    if (len(arg) > 0):
        delayNum = arg[0]
    else:
        delayNum = 3
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await ctx.message.delete()


@bot.command()
async def step(ctx, *arg: int):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    if (len(arg) > 0):
        if (arg[0] == 1):
            removereact = 1
        else:
            removereact = 0
    else:
        removereact = 0
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await ctx.message.delete()


@commands.has_permissions(kick_members=True)
@bot.command()
async def kick(ctx, user: discord.Member):
    if (ctx.author.id == 323504459835637761):
        await ctx.guild.kick(user)
        await ctx.send(f"{user.mention} has been kicked")
    else:
        await ctx.send(f"{ctx.author.mention} has been kicked")


@bot.command()
async def raining(ctx):
    await ctx.send("~There Will Come Soft Rains by Ray Bradbury")


@bot.command()
async def talk(ctx):
    await ctx.send("​" + ((await ctx.message.channel.history(
        limit=200).flatten())[-1].content).strip('​'))


@bot.command()
async def kill(ctx, *arg: str):
    if (len(arg) > 0):
        if (arg[0] == "@r"):
            player = random.choice(ctx.message.channel.members)
            while (str(player.status) != "online" or player.bot):
                player = random.choice(ctx.message.channel.members)
            await ctx.send(f"{player.mention} fell out of the world")
        elif (arg[0] == "@a"):
            allplayers = ""
            for player in ctx.message.channel.members:
                if (str(player.status) == "online" and not player.bot):
                    allplayers += f"{player.mention} fell out of the world\n"
            await ctx.send(allplayers)
        elif (arg[0] == "@e"):
            allplayers = ""
            for player in ctx.message.channel.members:
                if (str(player.status) == "online"):
                    allplayers += f"{player.mention} fell out of the world\n"
            await ctx.send(allplayers)
        else:
            await ctx.send(f"{arg[0]} fell out of the world")
            try:
                peep = ctx.guild.get_member_named(arg[0])
                await peep.move_to(ctx.guild.get_channel(779186887389872160))
            except:
                try:
                    peep = ctx.guild.get_member(int(arg[0][3:-1]))
                    await peep.move_to(
                        ctx.guild.get_channel(779186887389872160))
                except:
                    pass
    else:
        await ctx.send(f"{ctx.author.mention} fell out of the world")
        await ctx.author.move_to(ctx.guild.get_channel(779186887389872160))

@bot.command()
async def deport(ctx, name, channel):
  peep = ctx.guild.get_member_named(name)
  await peep.move_to(ctx.guild.get_channel(channel))

@slash.slash(name="smite",
             description="Smite a player", guild_ids=guild_ids
             )
async def smite(ctx: SlashContext, target):
    if (target == "@r"):
        player = random.choice(ctx.channel.members)
        while (str(player.status) != "online" or player.bot):
            player = random.choice(ctx.channel.members)
        await ctx.send(f"{player.mention} was struck by lightning")
    elif (target == "@a"):
        allplayers = ""
        for player in ctx.channel.members:
            if (str(player.status) == "online" and not player.bot):
                allplayers += f"{player.mention} was struck by lightning\n"
        await ctx.send(allplayers)
    elif (target == "@e"):
        allplayers = ""
        for player in ctx.channel.members:
            if (str(player.status) == "online"):
                allplayers += f"{player.mention} was struck by lightning\n"
        await ctx.send(allplayers)
    else:
        await ctx.send(f"{target} was struck by lightning")

@bot.command()
async def setsize(ctx, x, y):
    await terraingeneration.setsize(ctx, x, y)


@bot.command()
async def flat(ctx):
    await terraingeneration.flat(ctx)


@bot.command()
async def gen(ctx, seed=None):
    await terraingeneration.gen(ctx, seed)


@bot.command()
async def show(ctx):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    mapmessage = discord.utils.get(
        bot.cached_messages,
        id=mapmessageid) if not (mapmessageid == None) else None
    selectmessage = discord.utils.get(
        bot.cached_messages,
        id=selectmessageid) if not (selectmessageid == None) else None
    terrain = worlds.load(str(ctx.guild.id), dimension)
    result = ""
    for i in range(cameraY, cameraY + 8):
        for j in range(cameraX, cameraX + 8):
            result += emotes[terrain[i][j]]
        result += "\n"
    mapmessage = await ctx.send(result)
    selectmessage = await ctx.send("Selected: " + emotes[selected])
    react_message = discord.utils.get(bot.cached_messages, id=mapmessage.id)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    for reaction in reactions:
        await mapmessage.add_reaction(reaction)
    await asyncio.sleep(5)
    while (mapmessageid == react_message.id):
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
            str(ctx.guild.id))
        mapmessage = discord.utils.get(
            bot.cached_messages,
            id=mapmessageid) if not (mapmessageid == None) else None
        selectmessage = discord.utils.get(
            bot.cached_messages,
            id=selectmessageid) if not (selectmessageid == None) else None
        react_message = discord.utils.get(bot.cached_messages,
                                          id=react_message.id)
        tally = {
            reaction.emoji: reaction.count
            for reaction in react_message.reactions
        }
        maxvote = 1
        action = ''
        for index in reactions:
            if (tally[index] > maxvote):
                maxvote = tally[index]
                action = index
        if (action == '◀️'):
            await minel(ctx)
        elif (action == '🔼'):
            await mineu(ctx)
        elif (action == '🔽'):
            await mined(ctx)
        elif (action == '▶️'):
            await miner(ctx)
        elif (action == '⬅️'):
            await movel(ctx)
        elif (action == '⬆️'):
            await moveuplace(ctx)
        elif (action == '⬇️'):
            await moved(ctx, 1)
        elif (action == '➡️'):
            await mover(ctx)
        elif (action == '↖️'):
            await moveul(ctx)
        elif (action == '↗️'):
            await moveur(ctx)
        elif (action == '⏹'):
            selected += 1
            if (selected >= pindex):
                selected = 0
            worlds.savesetting(str(ctx.guild.id), [
                selected, px, py, pxpast, pypast, delayNum, removereact,
                columnCount, rowCount, cameraX, cameraY, mapmessageid,
                selectmessageid, dimension
            ])
            await selectmessage.edit(content=("Selected: " + emotes[selected]))
        elif (action == '⏺'):
            selected += 5
            if (selected >= pindex):
                selected = 0
            worlds.savesetting(str(ctx.guild.id), [
                selected, px, py, pxpast, pypast, delayNum, removereact,
                columnCount, rowCount, cameraX, cameraY, mapmessageid,
                selectmessageid, dimension
            ])
            await selectmessage.edit(content=("Selected: " + emotes[selected]))
        if (removereact == 1):
            for reaction in react_message.reactions:
                users = await reaction.users().flatten()
                for user in users:
                    if user.id != bot.user.id:
                        await reaction.remove(user)
        await asyncio.sleep(delayNum)
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
            str(ctx.guild.id))
        react_message = discord.utils.get(bot.cached_messages,
                                          id=mapmessage.id)
    print("Bye")


async def showedit(ctx):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    mapmessage = discord.utils.get(
        bot.cached_messages,
        id=mapmessageid) if not (mapmessageid == None) else None
    selectmessage = discord.utils.get(
        bot.cached_messages,
        id=selectmessageid) if not (selectmessageid == None) else None
    terrain = worlds.load(str(ctx.guild.id), dimension)
    result = ""
    for i in range(cameraY, cameraY + 8):
        for j in range(cameraX, cameraX + 8):
            result += emotes[terrain[i][j]]
        result += "\n"
    worlds.save(str(ctx.guild.id), terrain, dimension)
    try:
        await mapmessage.edit(content=result)
    except:
        mapmessage = await ctx.send(result)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])


@bot.command()
async def miner(ctx):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    mapmessage = discord.utils.get(
        bot.cached_messages,
        id=mapmessageid) if not (mapmessageid == None) else None
    selectmessage = discord.utils.get(
        bot.cached_messages,
        id=selectmessageid) if not (selectmessageid == None) else None
    terrain = worlds.load(str(ctx.guild.id), dimension)
    if (px < columnCount - 1):
        if (terrain[py][px + 1] == 0):
            await terraingeneration.setblock2(ctx, px + 1, py, selected)
        else:
            terrain[py][px + 1] = 0
            worlds.save(str(ctx.guild.id), terrain, dimension)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)


@bot.command()
async def minel(ctx):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    mapmessage = discord.utils.get(
        bot.cached_messages,
        id=mapmessageid) if not (mapmessageid == None) else None
    selectmessage = discord.utils.get(
        bot.cached_messages,
        id=selectmessageid) if not (selectmessageid == None) else None
    terrain = worlds.load(str(ctx.guild.id), dimension)
    if (px > 0):
        if (terrain[py][px - 1] == 0):
            await terraingeneration.setblock2(ctx, px - 1, py, selected)
        else:
            terrain[py][px - 1] = 0
            worlds.save(str(ctx.guild.id), terrain, dimension)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)


@bot.command()
async def mineu(ctx):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    mapmessage = discord.utils.get(
        bot.cached_messages,
        id=mapmessageid) if not (mapmessageid == None) else None
    selectmessage = discord.utils.get(
        bot.cached_messages,
        id=selectmessageid) if not (selectmessageid == None) else None
    terrain = worlds.load(str(ctx.guild.id), dimension)
    if (py > 0):
        if (terrain[py - 1][px] == 0):
            await terraingeneration.setblock2(ctx, px, py - 1, selected)
        else:
            terrain[py - 1][px] = 0
            worlds.save(str(ctx.guild.id), terrain, dimension)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)


@bot.command()
async def mined(ctx):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    mapmessage = discord.utils.get(
        bot.cached_messages,
        id=mapmessageid) if not (mapmessageid == None) else None
    selectmessage = discord.utils.get(
        bot.cached_messages,
        id=selectmessageid) if not (selectmessageid == None) else None
    terrain = worlds.load(str(ctx.guild.id), dimension)
    if (py < rowCount - 1):
        if (terrain[py + 1][px] == 0):
            await moveuplace(ctx)
            await terraingeneration.setblock2(ctx, px, py + 1, selected)
        else:
            terrain[py + 1][px] = 0
            worlds.save(str(ctx.guild.id), terrain, dimension)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)
    if (py != rowCount - 1 and terrain[py + 1][px] == 0):
        await moved(ctx)


@bot.command()
async def panr(ctx, *arg: int):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    mapmessage = discord.utils.get(
        bot.cached_messages,
        id=mapmessageid) if not (mapmessageid == None) else None
    selectmessage = discord.utils.get(
        bot.cached_messages,
        id=selectmessageid) if not (selectmessageid == None) else None
    if (len(arg) > 0):
        for _ in range(arg[0]):
            cameraX = min(cameraX + 1, columnCount - 8)
    else:
        cameraX = min(cameraX + 1, columnCount - 8)
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)


@bot.command()
async def panl(ctx, *arg: int):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    mapmessage = discord.utils.get(
        bot.cached_messages,
        id=mapmessageid) if not (mapmessageid == None) else None
    selectmessage = discord.utils.get(
        bot.cached_messages,
        id=selectmessageid) if not (selectmessageid == None) else None
    if (len(arg) > 0):
        for _ in range(arg[0]):
            cameraX = max(cameraX - 1, 0)
    else:
        cameraX = max(cameraX - 1, 0)
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)


@bot.command()
async def panu(ctx, *arg: int):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    mapmessage = discord.utils.get(
        bot.cached_messages,
        id=mapmessageid) if not (mapmessageid == None) else None
    selectmessage = discord.utils.get(
        bot.cached_messages,
        id=selectmessageid) if not (selectmessageid == None) else None
    if (len(arg) > 0):
        for _ in range(arg[0]):
            cameraY = max(cameraY - 1, 0)
    else:
        cameraY = max(cameraY - 1, 0)
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)


@bot.command()
async def pand(ctx, *arg: int):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    mapmessage = discord.utils.get(
        bot.cached_messages,
        id=mapmessageid) if not (mapmessageid == None) else None
    selectmessage = discord.utils.get(
        bot.cached_messages,
        id=selectmessageid) if not (selectmessageid == None) else None
    if (len(arg) > 0):
        for _ in range(arg[0]):
            cameraY = min(cameraY + 1, rowCount - 8)
    else:
        cameraY = min(cameraY + 1, rowCount - 8)
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)


@bot.command()
async def mover(ctx, *arg: int):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    mapmessage = discord.utils.get(
        bot.cached_messages,
        id=mapmessageid) if not (mapmessageid == None) else None
    selectmessage = discord.utils.get(
        bot.cached_messages,
        id=selectmessageid) if not (selectmessageid == None) else None
    terrain = worlds.load(str(ctx.guild.id), dimension)
    terrain[py][px] = 0
    if (terrain[pypast][pxpast] >= pindex):
        terrain[pypast][pxpast] = 0
    if (len(arg) > 0):
        for _ in range(arg[0]):
            if (terrain[py][min(px + 1, columnCount - 1)] == 0):
                px = min(px + 1, columnCount - 1)
    else:
        cblock = terrain[py][min(px + 1, columnCount - 1)]
        if (cblock == 0):
            pxpast = px
            pypast = py
            terrain[py][px] = pindex + 1
            px = min(px + 1, columnCount - 1)
        elif (cblock == 6 or cblock == 7):
            if (terrain[py][min(px + 2, columnCount - 1)] == 0):
                pxpast = px
                pypast = py
                terrain[py][px] = pindex + 1
                px = min(px + 2, columnCount - 1)
        elif (cblock == 43):
            if (dimension == "nether"):
                await switch(ctx, "overworld")
            else:
                await switch(ctx, "nether")
            selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
                str(ctx.guild.id))
            terrain = worlds.load(str(ctx.guild.id), dimension)
        elif (cblock == 34):
            if (terrain[py][min(px + 2, columnCount - 1)] == 43):
                if (dimension == "nether"):
                    await switch(ctx, "overworld")
                else:
                    await switch(ctx, "nether")
                selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
                    str(ctx.guild.id))
                terrain = worlds.load(str(ctx.guild.id), dimension)
    if terrain[py][px] != pindex:
        terrain[py][px] = pindex + 2
    worlds.save(str(ctx.guild.id), terrain, dimension)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)
    try:
        await ctx.message.delete()
    except:
        pass
    await asyncio.sleep(0.5)
    if (terrain[pypast][pxpast] >= pindex):
        terrain[pypast][pxpast] = 0
    terrain[py][px] = pindex
    worlds.save(str(ctx.guild.id), terrain, dimension)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)
    if (px > cameraX + 6):
        await panr(ctx, px - cameraX - 6)
    if (py != rowCount - 1 and terrain[py + 1][px] == 0):
        await moved(ctx)


@bot.command()
async def movel(ctx, *arg: int):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    mapmessage = discord.utils.get(
        bot.cached_messages,
        id=mapmessageid) if not (mapmessageid == None) else None
    selectmessage = discord.utils.get(
        bot.cached_messages,
        id=selectmessageid) if not (selectmessageid == None) else None
    terrain = worlds.load(str(ctx.guild.id), dimension)
    terrain[py][px] = 0
    if (terrain[pypast][pxpast] >= pindex):
        terrain[pypast][pxpast] = 0
    if (len(arg) > 0):
        for _ in range(arg[0]):
            if (terrain[py][max(px - 1, 0)] == 0):
                px = max(px - 1, 0)
    else:
        cblock = terrain[py][max(px - 1, 0)]
        if (cblock == 0):
            pxpast = px
            pypast = py
            terrain[py][px] = pindex + 5
            px = max(px - 1, 0)
        elif (cblock == 6 or cblock == 7):
            if (terrain[py][max(px - 2, 0)] == 0):
                pxpast = px
                pypast = py
                terrain[py][px] = pindex + 5
                px = max(px - 2, 0)
        elif (cblock == 43):
            if (dimension == "nether"):
                await switch(ctx, "overworld")
            else:
                await switch(ctx, "nether")
            selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
                str(ctx.guild.id))
            terrain = worlds.load(str(ctx.guild.id), dimension)
        elif (cblock == 34):
            if (terrain[py][max(px - 2, 0)] == 43):
                if (dimension == "nether"):
                    await switch(ctx, "overworld")
                else:
                    await switch(ctx, "nether")
                selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
                    str(ctx.guild.id))
                terrain = worlds.load(str(ctx.guild.id), dimension)
    if terrain[py][px] != pindex:
        terrain[py][px] = pindex + 6
    worlds.save(str(ctx.guild.id), terrain, dimension)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)
    try:
        await ctx.message.delete()
    except:
        pass
    await asyncio.sleep(0.5)
    if (terrain[pypast][pxpast] >= pindex):
        terrain[pypast][pxpast] = 0
    terrain[py][px] = pindex
    worlds.save(str(ctx.guild.id), terrain, dimension)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)
    if (px < cameraX + 1):
        await panl(ctx, cameraX + 1 - px)
    if (py != rowCount - 1 and terrain[py + 1][px] == 0):
        await moved(ctx)


@bot.command()
async def moveu(ctx, *arg: int):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    mapmessage = discord.utils.get(
        bot.cached_messages,
        id=mapmessageid) if not (mapmessageid == None) else None
    selectmessage = discord.utils.get(
        bot.cached_messages,
        id=selectmessageid) if not (selectmessageid == None) else None
    terrain = worlds.load(str(ctx.guild.id), dimension)
    terrain[py][px] = 0
    if (terrain[pypast][pxpast] >= pindex):
        terrain[pypast][pxpast] = 0
    if (len(arg) > 0):
        for _ in range(arg[0]):
            if (terrain[max(py - 1, 0)][px] == 0):
                py = max(py - 1, 0)
    else:
        if (terrain[max(py - 1, 0)][px] == 0):
            pxpast = px
            pypast = py
            terrain[py][px] = pindex + 3
            py = max(py - 1, 0)
    if terrain[py][px] != pindex:
        terrain[py][px] = pindex + 4
    worlds.save(str(ctx.guild.id), terrain, dimension)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)
    try:
        await ctx.message.delete()
    except:
        pass
    await asyncio.sleep(0.5)
    if (terrain[pypast][pxpast] >= pindex):
        terrain[pypast][pxpast] = 0
    terrain[py][px] = pindex
    worlds.save(str(ctx.guild.id), terrain, dimension)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)
    if (py < cameraY + 1):
        await panu(ctx, cameraY + 1 - py)
    if (py != rowCount - 1 and terrain[py + 1][px] == 0):
        await moved(ctx)


@bot.command()
async def moveuplace(ctx):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    mapmessage = discord.utils.get(
        bot.cached_messages,
        id=mapmessageid) if not (mapmessageid == None) else None
    selectmessage = discord.utils.get(
        bot.cached_messages,
        id=selectmessageid) if not (selectmessageid == None) else None
    terrain = worlds.load(str(ctx.guild.id), dimension)
    terrain[py][px] = 0
    if (terrain[pypast][pxpast] >= pindex):
        terrain[pypast][pxpast] = 0
    if (terrain[max(py - 1, 0)][px] == 0):
        pxpast = px
        pypast = py
        terrain[py][px] = pindex + 3
        py = max(py - 1, 0)
    elif (terrain[max(py - 1, 0)][px] == 20):
        pxpast = px
        pypast = py
        terrain[py][px] = pindex + 3
        checkint = 1
        while (py - checkint > 0 and terrain[max(py - checkint, 0)][px] == 20):
            checkint += 1
            if (terrain[max(py - checkint, 0)][px] == 0):
                py = max(py - checkint, 0)
    if terrain[py][px] != pindex:
        terrain[py][px] = pindex + 4
    worlds.save(str(ctx.guild.id), terrain, dimension)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)
    await asyncio.sleep(0.5)
    if (terrain[pypast][pxpast] >= pindex):
        terrain[pypast][pxpast] = 0
    terrain[py][px] = pindex
    await showedit(ctx)
    if (py + 1 < rowCount):
        terrain[py + 1][px] = selected
    worlds.save(str(ctx.guild.id), terrain, dimension)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)
    if (py < cameraY + 1):
        await panu(ctx, cameraY + 1 - py)
    if (py != rowCount - 1 and terrain[py + 1][px] == 0):
        await moved(ctx)


@bot.command()
async def moveur(ctx, *arg: int):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    mapmessage = discord.utils.get(
        bot.cached_messages,
        id=mapmessageid) if not (mapmessageid == None) else None
    selectmessage = discord.utils.get(
        bot.cached_messages,
        id=selectmessageid) if not (selectmessageid == None) else None
    terrain = worlds.load(str(ctx.guild.id), dimension)
    terrain[py][px] = 0
    if (terrain[pypast][pxpast] >= pindex):
        terrain[pypast][pxpast] = 0
    if (len(arg) > 0):
        for _ in range(arg[0]):
            if (terrain[max(py - 1, 0)][px] == 0):
                py = max(py - 1, 0)
    else:
        if (terrain[max(py - 1, 0)][px] == 0):
            pxpast = px
            pypast = py
            terrain[py][px] = pindex + 3
            py = max(py - 1, 0)
    if terrain[py][px] != pindex:
        terrain[py][px] = pindex + 4
    worlds.save(str(ctx.guild.id), terrain, dimension)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)
    try:
        await ctx.message.delete()
    except:
        pass
    await asyncio.sleep(0.5)
    if (terrain[pypast][pxpast] >= pindex):
        terrain[pypast][pxpast] = 0
    terrain[py][px] = pindex
    worlds.save(str(ctx.guild.id), terrain, dimension)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)
    if (py < cameraY + 1):
        await panu(ctx, cameraY + 1 - py)
    await mover(ctx)


@bot.command()
async def moveul(ctx, *arg: int):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    mapmessage = discord.utils.get(
        bot.cached_messages,
        id=mapmessageid) if not (mapmessageid == None) else None
    selectmessage = discord.utils.get(
        bot.cached_messages,
        id=selectmessageid) if not (selectmessageid == None) else None
    terrain = worlds.load(str(ctx.guild.id), dimension)
    terrain[py][px] = 0
    if (terrain[pypast][pxpast] >= pindex):
        terrain[pypast][pxpast] = 0
    if (len(arg) > 0):
        for _ in range(arg[0]):
            if (terrain[max(py - 1, 0)][px] == 0):
                py = max(py - 1, 0)
    else:
        if (terrain[max(py - 1, 0)][px] == 0):
            pxpast = px
            pypast = py
            terrain[py][px] = pindex + 3
            py = max(py - 1, 0)
    if terrain[py][px] != pindex:
        terrain[py][px] = pindex + 4
    worlds.save(str(ctx.guild.id), terrain, dimension)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)
    try:
        await ctx.message.delete()
    except:
        pass
    await asyncio.sleep(0.5)
    if (terrain[pypast][pxpast] >= pindex):
        terrain[pypast][pxpast] = 0
    terrain[py][px] = pindex
    worlds.save(str(ctx.guild.id), terrain, dimension)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)
    if (py < cameraY + 1):
        await panu(ctx, cameraY + 1 - py)
    await movel(ctx)


@bot.command()
async def moved(ctx, *arg: int):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    mapmessage = discord.utils.get(
        bot.cached_messages,
        id=mapmessageid) if not (mapmessageid == None) else None
    selectmessage = discord.utils.get(
        bot.cached_messages,
        id=selectmessageid) if not (selectmessageid == None) else None
    terrain = worlds.load(str(ctx.guild.id), dimension)
    terrain[py][px] = 0
    if (terrain[pypast][pxpast] >= pindex):
        terrain[pypast][pxpast] = 0
    if (len(arg) > 0):
        if (arg[0] == 1):
            if (terrain[min(py + 1, rowCount - 1)][px] == 20):
                pxpast = px
                pypast = py
                terrain[py][px] = pindex + 7
                checkint = 1
                while (py + checkint < rowCount - 1 and terrain[min(
                        py + checkint, rowCount - 1)][px] == 20):
                    checkint += 1
                    if (terrain[min(py + checkint, rowCount - 1)][px] == 0):
                        py = min(py + checkint, rowCount - 1)
            elif (terrain[min(py + 1, rowCount - 1)][px] == 44):
                await switch(ctx, "end")
                selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
                    str(ctx.guild.id))
                terrain = worlds.load(str(ctx.guild.id), dimension)
        else:
            for _ in range(arg[0]):
                if (terrain[min(py + 1, rowCount - 1)][px] == 0):
                    py = min(py + 1, rowCount - 1)
    else:
        if (terrain[min(py + 1, rowCount - 1)][px] == 0):
            pxpast = px
            pypast = py
            terrain[py][px] = pindex + 7
            py = min(py + 1, rowCount - 1)
    if terrain[py][px] != pindex:
        terrain[py][px] = pindex + 8
    else:
        terrain[py][px] = pindex
    worlds.save(str(ctx.guild.id), terrain, dimension)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)
    try:
        await ctx.message.delete()
    except:
        pass
    await asyncio.sleep(0.5)
    if (terrain[pypast][pxpast] >= pindex):
        terrain[pypast][pxpast] = 0
    terrain[py][px] = pindex
    worlds.save(str(ctx.guild.id), terrain, dimension)
    mapmessageid = mapmessage.id if not (mapmessage == None) else None
    selectmessageid = selectmessage.id if not (selectmessage == None) else None
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension
    ])
    await showedit(ctx)
    if (py > cameraY + 6):
        await pand(ctx, py - cameraY - 6)
    if (py != rowCount - 1 and terrain[py + 1][px] == 0):
        await moved(ctx)


@bot.command()
async def select(ctx, item: int):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    mapmessage = discord.utils.get(
        bot.cached_messages,
        id=mapmessageid) if not (mapmessageid == None) else None
    selectmessage = discord.utils.get(
        bot.cached_messages,
        id=selectmessageid) if not (selectmessageid == None) else None
    if (item >= 0 and item < 47):
        selected = item
        await selectmessage.edit(content=("Selected: " + emotes[selected]))
        worlds.savesetting(str(ctx.guild.id), [
            selected, px, py, pxpast, pypast, delayNum, removereact,
            columnCount, rowCount, cameraX, cameraY, mapmessageid,
            selectmessageid, dimension
        ])
    else:
        await selectmessage.edit(content="Not a valid block")
    await ctx.message.delete()


@bot.command()
async def index(ctx):
    indexInventory = blockindexes.indexList().split("\n")
    result = ""
    for items in range(0, 12):
        result += indexInventory[items] + "\n"
    await ctx.send(result + "`")
    result = "`=========================================================\n"
    for items in range(12, 25):
        result += indexInventory[items] + "\n"
    await ctx.send(result + "`")


@bot.command()
async def execute(ctx, *, command):
    await commandStuff.cmdexecute(ctx, command)


@bot.command()
async def setblock(ctx, x, y, blockid):
    await terraingeneration.setblock(ctx, x, y, blockid)
    await showedit(ctx)


@bot.command()
async def switch(ctx, dimensionselect: str):
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(
        str(ctx.guild.id))
    worlds.savesetting(str(ctx.guild.id), [
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount,
        rowCount, cameraX, cameraY, mapmessageid, selectmessageid,
        dimensionselect
    ])


@bot.command()
async def mcserver(ctx, ip: str):
    api = requests.get("https://api.mcsrvstat.us/2/%s" % ip)
    if (api.status_code == 200):
        apijson = api.json()
        if (apijson["online"]):
            embed = discord.Embed(title="%s Server Status" % ip,
                                  color=discord.Colour(0x00FF00))
            embed.add_field(name="Status:", value="🟢 Online")
            embed.add_field(name="Version:", value=apijson["version"])
            embed.add_field(name="Players:",
                            value=(str(apijson["players"]["online"]) + "/" +
                                   str(apijson["players"]["max"])))
            embed.set_image(url="https://api.mcsrvstat.us/icon/%s" % ip)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="%s Server Status" % ip,
                                  color=discord.Colour(0xFF0000))
            embed.add_field(name="Status:", value="🔴 Offline")
            await ctx.send(embed=embed)
    else:
        await ctx.send("Error reaching API")


@bot.command()
async def mcserverlistplayers(ctx, ip: str):
    api = requests.get("https://api.mcsrvstat.us/2/%s" % ip)
    if (api.status_code == 200):
        apijson = api.json()
        if (apijson["online"]):
            embed = discord.Embed(title="%s Server Status" % ip,
                                  color=discord.Colour(0x00FF00))
            embed.add_field(name="Status:", value="🟢 Online")
            embed.add_field(name="Version:", value=apijson["version"])
            embed.add_field(name="Players:",
                            value=("\n".join(apijson["players"]["list"])))
            embed.set_image(url="https://api.mcsrvstat.us/icon/%s" % ip)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="%s Server Status" % ip,
                                  color=discord.Colour(0xFF0000))
            embed.add_field(name="Status:", value="🔴 Offline")
            await ctx.send(embed=embed)
    else:
        await ctx.send("Error reaching API")


@bot.command()
async def ask(ctx, arg):
    await ctx.send("No.")


@bot.command()
async def d(ctx, arg):
    await define.define(ctx, arg)


@bot.command()
async def p(ctx, arg, dc=1):
  voice = await ctx.author.voice.channel.connect()
  voice.play(discord.FFmpegPCMAudio('./res/' + arg + '.mp3'))
  while voice.is_playing():
    await asyncio.sleep(1)
  if (dc == 2):
    await p2(ctx, arg, voice)
    return
  await voice.disconnect()
  if (dc == 0):
    await ctx.author.move_to(None)

async def p2(ctx, arg, voice):
  voice.play(discord.FFmpegPCMAudio('./res/' + arg + '.mp3'))
  while voice.is_playing():
    await asyncio.sleep(1)
  await p2(ctx, arg, voice)

@bot.command()
async def say(ctx, *, arg:str):
  tts = gtts.gTTS(arg)
  tts.save("./res/audio.mp3")
  voice = await ctx.author.voice.channel.connect()
  voice.play(discord.FFmpegPCMAudio('./res/audio.mp3'))
  while voice.is_playing():
      await asyncio.sleep(1)
  await voice.disconnect()

@bot.command()
async def s(ctx, *, arg):
    async with ctx.typing():
        # Define cseargs for search
        cseargs = {'q': arg, 'cx': cse_id, 'num': 3}

        # Create a results object
        results = search_google.api.results(buildargs, cseargs)

        items = results.metadata['items']
        itemlinks = results.links

        for i, kv in enumerate(items[:10]):
            if 'start' in cseargs:
                i += int(cseargs['start'])

            header = '\n[' + str(i) + '] ' + kv['displayLink']
            result = header + '\n'
            result += itemlinks[i] + '\n'
            result += ('=' * len(header)) + '\n'

            description = '\n' + kv['snippet']
            await ctx.send(result + description)

@bot.command()
async def bai(ctx):
  await ctx.author.edit(deafen=True, mute=True)

@bot.command()
async def hai(ctx):
  await ctx.author.edit(deafen=False, mute=False)

async def movie(ctx):
    """MOVIE TIME"""
    channel = ctx.author.voice.channel
    vc = ctx.voice_client
    if vc:
        if vc.channel.id == channel.id:
            return
        await vc.move_to(channel)
    else:
        await channel.connect()

keep_alive.keep_alive()
try:
    bot.run(os.getenv("TOKEN"))
except Exception as e:
    print(e)
    os.system("kill 1")

