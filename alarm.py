import datetime
import threading
import asyncio

time1 = '1:18:50'
time2 = '4:17:30'
time3 = '5:18:50'

async def checkTime(ctx):
  while True:
    now = datetime.datetime.now()

    current_time = now.strftime("%w:%H:%M")
    if(current_time == time1 or current_time == time2 or current_time == time3):  # check if matches with the desired time
      await ctx.send("ENGLISH INCOMING! BRACE FOR IMPACT")
    await asyncio.sleep(60)

async def eng(ctx):
  now = datetime.datetime.now()

  current_time = now.strftime("%w:%H:%M")
  target_time = now
  dt = 0
  if(current_time <= time1):
    dt = int(time1[:1])-int(current_time[:1])
    target_time = target_time.replace(hour=int(time1[2:4]), 
    minute=int(time1[5:]))
  elif(current_time <= time2):
    dt = int(time2[:1])-int(current_time[:1])
    target_time = target_time.replace(hour=int(time2[2:4]), minute=int(time2[5:]))
  elif(current_time <= time3):
    dt = int(time3[:1])-int(current_time[:1])
    target_time = target_time.replace(hour=int(time3[2:4]), minute=int(time3[5:]))
  else:
    dt = int(time1[:1])-int(current_time[:1])+7
  dt = datetime.timedelta(dt)

  target_time = target_time + dt
  await ctx.send(str((target_time-now).days) + " days, " + str((target_time-now).seconds//3600) + " hours, " + str(((target_time-now).seconds//60)%60) + " minutes" + "\n" + str(int((target_time-now).total_seconds())) + " seconds remaining" + "\n" + str(int((target_time-now).total_seconds()/60)) + " minutes remaining" + "\n" + str(int((target_time-now).total_seconds()/60)/60) + " hours remaining" + "\n" + str(int((target_time-now).total_seconds()/60)/60/24) + " days remaining")


async def english(ctx):
  now = datetime.datetime.now()

  current_time = now.strftime("%w:%H:%M")
  target_time = now
  dt = 0
  if(current_time <= time1):
    dt = int(time1[:1])-int(current_time[:1])
    target_time = target_time.replace(hour=int(time1[2:4]), 
    minute=int(time1[5:]))
  elif(current_time <= time2):
    dt = int(time2[:1])-int(current_time[:1])
    target_time = target_time.replace(hour=int(time2[2:4]), minute=int(time2[5:]))
  elif(current_time <= time3):
    dt = int(time3[:1])-int(current_time[:1])
    target_time = target_time.replace(hour=int(time3[2:4]), minute=int(time3[5:]))
  else:
    dt = int(time1[:1])-int(current_time[:1])+7
  dt = datetime.timedelta(dt)

  target_time = target_time + dt
  await ctx.send(str(int((target_time-now).total_seconds()/60)) + " minutes remaining")