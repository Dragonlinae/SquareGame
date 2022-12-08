import worlds
import asyncio
import random


async def setsize(ctx, x, y):
  selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessage, selectmessage, dimension = worlds.loadsetting(str(ctx.guild.id))
  columnCount = int(x)
  rowCount = int(y)
  cameraX = 0
  cameraY = int(rowCount / 2) - 4
  terrain = [[0] * columnCount for _ in range(rowCount)]
  worlds.save(str(ctx.guild.id), terrain, dimension)
  worlds.savesetting(str(ctx.guild.id),[selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessage, selectmessage, dimension])


async def flat(ctx):
  selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessage, selectmessage, dimension = worlds.loadsetting(str(ctx.guild.id))
  terrain = [[0] * columnCount for _ in range(rowCount)]
  px=0
  cameraX = 0
  pxpast = 0
  pypast = 0
  cameraY = int(rowCount / 2) - 4
  dimension = "overworld"
  for dimensiongen in ["overworld", "nether", "end"]:
    for i in range(rowCount):
      for j in range(columnCount):
        terrain[i][j] = 0
    tracking = int(rowCount / 2)
    worlds.save(str(ctx.guild.id), terrain, dimensiongen)
    worlds.savesetting(str(ctx.guild.id),[selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessage, selectmessage, dimension])
    for j in range(columnCount):
      if(j==0):
        py = rowCount-tracking-1
      await mappart(ctx, j, tracking, dimensiongen)
  terrain = worlds.load(str(ctx.guild.id), dimension)
  selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessage, selectmessage, dimension = worlds.loadsetting(str(ctx.guild.id))
  terrain[py][px] = 47
  worlds.save(str(ctx.guild.id), terrain, dimension)
  worlds.savesetting(str(ctx.guild.id),[selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessage, selectmessage, dimension])

async def gen(ctx, seed = None):
  selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessage, selectmessage, dimension = worlds.loadsetting(str(ctx.guild.id))
  px = 0
  cameraX = 0
  pxpast = 0
  pypast = 0
  cameraY = int(rowCount / 2) - 4
  dimension = "overworld"
  for dimensiongen in ["overworld", "nether", "end"]:
    terrain = [[0] * columnCount for _ in range(rowCount)]
    for i in range(rowCount):
      for j in range(columnCount):
        terrain[i][j] = 0
    worlds.save(str(ctx.guild.id), terrain, dimensiongen)
    worlds.savesetting(str(ctx.guild.id),[selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessage, selectmessage, dimension])
    if (seed != None):
      random.seed(seed)
    else:
      random.seed()
    terrainnums = int(random.random() * pow(10, columnCount))
    tracking = int(rowCount / 2)
    for j in range(columnCount):
      testing = terrainnums % 10
      if (testing == 0 and j != 0):
        tracking -= 4
      elif (testing == 9 and j != 0):
        tracking += 4
      elif (testing < 3):
        tracking -= 1
      elif (testing > 6):
        tracking += 1
      tracking = max(int(rowCount / 2) - 3, tracking)
      tracking = min(int(rowCount / 2) + 3, tracking)
      if(j==0 and dimensiongen == "overworld"):
        py = rowCount-tracking-1
        worlds.savesetting(str(ctx.guild.id),[selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessage, selectmessage, dimension])
      await mappart(ctx, j, tracking, dimensiongen)
      terrainnums = int(terrainnums / 10)
    if(dimensiongen=="overworld"):
      locatex = random.randint(max(5,columnCount-10),columnCount-4)
      await setblock3(ctx, 44, [locatex, rowCount-2, locatex+1, rowCount-2, locatex+2, rowCount-2])
  terrain = worlds.load(str(ctx.guild.id), "overworld")
  selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessage, selectmessage, dimension = worlds.loadsetting(str(ctx.guild.id))
  terrain[py][px] = 47
  worlds.save(str(ctx.guild.id), terrain, "overworld")
  worlds.savesetting(str(ctx.guild.id),[selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessage, selectmessage, dimension])
  
async def mappart(ctx, j, tracking, dimensiongen):
  selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessage, selectmessage, dimension = worlds.loadsetting(str(ctx.guild.id))
  terrain = worlds.load(str(ctx.guild.id), dimensiongen)
  if(dimensiongen == "overworld"):
    rngval = random.random()
    if (rngval < 0.1 and j > 3):
        worlds.save(str(ctx.guild.id), terrain, dimensiongen)
        worlds.savesetting(str(ctx.guild.id),[selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessage, selectmessage, dimension])
        await createtree(ctx, tracking, j)
        selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessage, selectmessage, dimension = worlds.loadsetting(str(ctx.guild.id))
        terrain = worlds.load(str(ctx.guild.id), dimensiongen)
    for i in range(max(0, tracking - 2)):
      rngval = random.random()
      if (rngval < 0.03):
        terrain[rowCount - 1 - i][j] = 28
      elif (rngval < 0.1):
        terrain[rowCount - 1 - i][j] = 26
      elif (rngval < 0.2):
        terrain[rowCount - 1 - i][j] = 27
      elif (rngval < 0.3):
        terrain[rowCount - 1 - i][j] = 29
      else:
        terrain[rowCount - 1 - i][j] = 1
    for i in range(max(0, tracking - 2), tracking - 1):
      terrain[rowCount - 1 - i][j] = 3
    terrain[rowCount - tracking][j] = 2
  elif(dimensiongen == "nether"):
    for i in range(max(0, tracking)):
      terrain[rowCount - 1 - i][j] = 46
    rngval = random.random()
    if (rngval < 0.05 and j > 6):
      sandlength = int(rngval*100 + 3)
      for j2 in range(sandlength):
        rngval2 = int(random.random()*3+1)
        for i2 in range(max(0,tracking-rngval2),tracking):
          terrain[rowCount - 1 - i2][j-j2] = 37
  elif(dimensiongen == "end"):
    for i in range(max(0, tracking)):
      terrain[rowCount - 1 - i][j] = 45
    rngval = random.random()
    if (rngval < 0.1 and j > 3 and j < columnCount-3):
      rngval2 = int(random.random()*5+10)
      for j2 in range(j-1,j+2):
        for i2 in range(tracking, min(tracking+rngval2,rowCount)):
          terrain[rowCount - 1 - i2][j2] = 34
  worlds.save(str(ctx.guild.id), terrain, dimensiongen)
  worlds.savesetting(str(ctx.guild.id),[selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessage, selectmessage, dimension])

async def setblock(ctx, x, y, blockid):
  selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(str(ctx.guild.id))
  terrain = worlds.load(str(ctx.guild.id), dimension)
  x = int(x)
  y = int(y)
  blockid = int(blockid)
  if(x>=0 and x<columnCount and y>=0 and y<rowCount and (x!=px or rowCount-1-y!=py) and blockid>=0 and blockid<47):
    terrain[rowCount-1-y][x] = blockid
  worlds.save(str(ctx.guild.id), terrain, dimension)
  worlds.savesetting(str(ctx.guild.id),[selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension])
  
async def setblock2(ctx, x, y, blockid):
  selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(str(ctx.guild.id))
  terrain = worlds.load(str(ctx.guild.id), dimension)
  x = int(x)
  y = int(y)
  blockid = int(blockid)
  if(x>=0 and x<columnCount and y>=0 and y<rowCount and (x!=px or y!=py) and blockid>=0 and blockid<47):
    terrain[y][x] = blockid
    worlds.save(str(ctx.guild.id), terrain, dimension)
    worlds.savesetting(str(ctx.guild.id),[selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension])
  if(blockid == 19 and await blockcheck(ctx, 34, [x,y+1,x+1,y+1,x+2,y,x+2,y-1,x+2,y-2,x+1,y-3,x,y-3,x-1,y-2,x-1,y-1,x-1,y])):
    await setblock3(ctx, 43, [x, y, x+1, y, x+1, y-1, x+1, y-2, x, y-2, x, y-1])
    if(dimension=="nether"):
      await switch(ctx, "overworld")
    else:
      await switch(ctx, "nether")
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(str(ctx.guild.id))
    terrain = worlds.load(str(ctx.guild.id), dimension)
  elif(blockid == 19 and await blockcheck(ctx, 34, [x-1,y+1,x,y+1,x+1,y,x+1,y-1,x+1,y-2,x,y-3,x-1,y-3,x-2,y-2,x-2,y-1,x-2,y])):
    await setblock3(ctx, 43, [x-1, y, x, y, x, y-1, x, y-2, x-1, y-2, x-1, y-1])
    if(dimension=="nether"):
      await switch(ctx, "overworld")
    else:
      await switch(ctx, "nether")
    selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(str(ctx.guild.id))
    terrain = worlds.load(str(ctx.guild.id), dimension)
async def setblock3(ctx, blockid, coords):
  selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(str(ctx.guild.id))
  terrain = worlds.load(str(ctx.guild.id), dimension)
  blockid = int(blockid)
  for i in range(int(len(coords)/2)):
    x = int(coords[2*i])
    y = int(coords[2*i+1])
    if(x>=0 and x<columnCount and y>=0 and y<rowCount and (x!=px or rowCount-1-y!=py) and blockid>=0 and blockid<47):
      terrain[y][x] = blockid
  worlds.save(str(ctx.guild.id), terrain, dimension)
  worlds.savesetting(str(ctx.guild.id),[selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension])

async def blockcheck(ctx, lookfor, coords):
  selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(str(ctx.guild.id))
  terrain = worlds.load(str(ctx.guild.id), dimension)
  for i in range(int(len(coords)/2)):
    x = int(coords[2*i])
    y = int(coords[2*i+1])
    if(x>=0 and x<columnCount and y>=0 and y<rowCount and (x!=px or rowCount-1-y!=py)):
      if terrain[y][x] != int(lookfor):
        return False
  return True

async def createtree(ctx, i, j):
  for i2 in range(i, i+2):
    await setblock(ctx, j, i2, 9)
  await setblock (ctx, j, i+2, 10)
  await setblock (ctx, j-1, i+2, 10)
  await setblock (ctx, j+1, i+2, 10)
  await setblock (ctx, j-2, i+2, 10)
  await setblock (ctx, j+2, i+2, 10)
  
  await setblock (ctx, j, i+3, 10)
  await setblock (ctx, j-1, i+3, 10)
  await setblock (ctx, j+1, i+3, 10)
  await setblock (ctx, j-2, i+3, 10)
  await setblock (ctx, j+2, i+3, 10)

  await setblock (ctx, j, i+4, 10)
  await setblock (ctx, j-1, i+4, 10)
  await setblock (ctx, j+1, i+4, 10)
  
  await setblock (ctx, j, i+5, 10)
  await setblock (ctx, j-1, i+5, 10)
  await setblock (ctx, j+1, i+5, 10)


async def switch(ctx, dimensionselect:str):
  selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimension = worlds.loadsetting(str(ctx.guild.id))
  worlds.savesetting(str(ctx.guild.id),[selected, px, py, pxpast, pypast, delayNum, removereact, columnCount, rowCount, cameraX, cameraY, mapmessageid, selectmessageid, dimensionselect])