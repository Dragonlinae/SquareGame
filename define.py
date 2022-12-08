import requests

async def define(ctx, word:str):
  api = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en_US/%s" %word)
  if(api.status_code==200):
    apijson = api.json()[0]
    result = await formatArr(apijson)
    result = result.split("\n")
    group = ""
    for segment in result:
      if(len(group + "\n" + segment) < 2000):
        group += "\n" + segment
      else:
        await ctx.send(group)
        group = segment
    await ctx.send(group)
  else:
    await ctx.send("Not found")

async def formatArr(query):
  result = ""
  if(isinstance(query,dict)):
    for k,v in query.items():
      if(isinstance(v,list)):
        result += "\n" + k + ":"
        for part in v:
          result += "\n" + (await formatArr(part)).replace("\n", "\n     ").strip("\n")
      elif(isinstance(v,dict)):
        result += "\n" + k + ":"
        result += "\n" + (await formatArr(v)).replace("\n", "\n     ").strip("\n")
      else:
        result += "\n" + k + ": " + str(v)
      print(str(v))
  elif(isinstance(query,list)):
    for part in query:
      result += "\n" + part
  else:
    result += "\n" + query
  return result