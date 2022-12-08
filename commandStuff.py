import random

execPlayer = None
channel = None
allowed = [323504459835637761, 318958842123780096, 229727740952051715, 541321819039203338]

async def cmdexecute(ctx, userinput):
  global execPlayer
  global channel
  execPlayer = None
  channel = None
  userinput = userinput.split(' ', 1)
  check = userinput[0]
  command = userinput[1]
  await method2[check](ctx, command)

async def cmdas(ctx, userinput):
  userinput = userinput.split(' ', 2)
  arg = userinput[0]
  check = userinput[1]
  command = userinput[2]
  global execPlayer
  if(arg == "@r"):
    execPlayer = random.choice(ctx.message.channel.members)
    while (str(execPlayer.status) != "online" or execPlayer.bot):
      execPlayer = random.choice(ctx.message.channel.members).id
  elif(arg == "@a"):
    await ctx.send("Sorry, targeting >1 person is disabled.")
    return
  elif(arg == "@e"):
    await ctx.send("Sorry, targeting >1 person is disabled. Specify a single person by using @e[name=<Insert player name>]")
    return
  elif(arg[0:3]=="@e["):
    arg = arg[3:len(arg)-1]
    nbt = arg.split(",")
    for part in nbt:
      part = part.strip()
      partarg = part.split("=")
      if(partarg[0] == "name"):
        execPlayer = ctx.guild.get_member_named(partarg[1])
        if(execPlayer != None):
          execPlayer = execPlayer.id
        else:
          execPlayer = ctx.guild.get_member(partarg[1])
          if(execPlayer != None):
            execPlayer = execPlayer.id
          else:
            execPlayer = None
  else:
    execPlayer = ctx.guild.get_member_named(arg)
    if(execPlayer != None):
      execPlayer = execPlayer.id
    else:
      execPlayer = ctx.guild.get_member(int(arg))
      if(execPlayer != None):
        execPlayer = execPlayer.id
      else:
        execPlayer = None
  await method2[check](ctx, command)

async def cmdpositioned(ctx, userinput):
  userinput = userinput.split(' ', 2)
  arg = userinput[0]
  check = userinput[1]
  command = userinput[2]
  global channel
  channel = ctx.guild.get_channel(int(arg))
  await method2[check](ctx, command)

async def cmdrun(ctx, userinput):
  userinput = userinput.split(' ', 1)
  check = userinput[0]
  command = userinput[1]
  await method1[check](ctx, command)

async def cmdsay(ctx, message=None):
  global channel
  global execPlayer
  if(ctx.author.id in allowed):
    if(execPlayer != None):
      member = ctx.guild.get_member(execPlayer)
      if(channel != None):
        webhook = await channel.create_webhook(name=member.name)
      else:
        webhook = await ctx.channel.create_webhook(name=member.name)
      await webhook.send(
        str(message), username=member.name, avatar_url=member.avatar_url)

      await webhook.delete()
    else:
      if(channel != None):
        await channel.send(message)
      else:
        await ctx.send(message)
  else:
    await ctx.send("You do not have permission to use this command.")

method1 = {"execute":cmdexecute, "say":cmdsay}
method2 = {"as":cmdas, "positioned":cmdpositioned, "in":cmdpositioned, "run":cmdrun}


"""
@bot.command()
async def execute(ctx, asword : str, member: discord.Member, runword : str, sayword : str, *, message=None):
  if(ctx.author.id == 323504459835637761):
    webhook = await ctx.channel.create_webhook(name=member.name)
    await webhook.send(
      str(message), username=member.name, avatar_url=member.avatar_url)

    webhooks = await ctx.channel.webhooks()
    for webhook in webhooks:
      await webhook.delete()
"""