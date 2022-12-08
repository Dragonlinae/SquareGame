file = open('raintext.txt')
try:
  rainlines = file.readlines()
  rainlines = rainlines[0].split(".")
finally:
  file.close()

def rain(line):
  if(line=="~There Will Come Soft Rains by Ray Bradbury"):
    return("~" + rainlines[0] + ".")
  line = line[1:-1]
  for i in range(len(rainlines)):
    if(line==rainlines[i]):
      try:
        return("~" + rainlines[i+1] + ".")
      except:
        return
  