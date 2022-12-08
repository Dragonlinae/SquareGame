
blockIndex = []
biggestLine = 0
blockFile = open("blockIndex.txt","r")
for item in blockFile.readlines():
  blockIndex.append(item.split("|")[0])
  if len(item) > biggestLine:
    biggestLine = len(item)
blockFile.close()
biggestLineText = ""
for item in range(0,biggestLine + 1):
  biggestLineText += " "

def indexList():
  result = "Minecraft block emotes: (index number | Emote | Block name)`\n"
  data = open("blockIndex.txt","r")
  thirdCount = 1
  indexNum = 0
  for item in data.readlines():
    result += prepFor("%02d"%indexNum + " :`" + item.split("|")[0] + "`: " + item.split("|")[1])
    if thirdCount >= 2:
      result += "\n"
      thirdCount = 0
    thirdCount += 1
    indexNum += 1
  data.close()
  return result


def prepFor(line,gapSize=2):
  line = line[0:len(line)-1]
  airSpace = (biggestLine + 5) - len(line)
  for item in range(0,airSpace + 1):
    line += " "
  for item in range(0,gapSize):
    line += " "
  return line