
import re

def exactMatch(regex, findStr):

  finds = regex.findall(findStr)
  return finds[0] if len(finds) == 1 else False

def inputColour(inputText):

  hexTest = re.compile('#[a-fA-F0-9]{6}')
  rgbTest = re.compile('\d+[,\s]{1}\d+[,\s]{1}\d+')

  while True:

    c = input(inputText)
    hexMatch = exactMatch(hexTest, c)
    rgbMatch = exactMatch(rgbTest, c)

    if hexMatch:
      return {
        'r': int(hexMatch[1:3], 16),
        'g': int(hexMatch[3:5], 16),
        'b': int(hexMatch[5:7], 16)
      }

    elif rgbMatch:
      rgbSplit = re.split('\s|,', rgbMatch)
      return {
        'r': int(rgbSplit[0]),
        'g': int(rgbSplit[1]),
        'b': int(rgbSplit[2])
      }
    
    else:
      print('Invalid input.')

c1 = inputColour('Enter colour #1 (hex or rgb):\n > ')
c2 = inputColour('Enter colour #2 (hex or rgb):\n > ')
