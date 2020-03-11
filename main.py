import re

# Terminal colours
class tc:
  PURPLE = '\033[95m'
  BLUE   = '\033[94m'
  GREEN  = '\033[92m'
  YELLOW = '\033[93m'
  RED    = '\033[91m'
  WHITE  = '\033[0m'

# Returns the match if success (False if fail).
def exactMatch(regex, findStr):

  finds = regex.findall(findStr)
  return finds[0] if len(finds) == 1 else False

# Allows for the input of a colour in RGB or hex. Runs until valid input.
def inputColour(inputText):

  hexTest = re.compile('#[a-fA-F0-9]{6}')
  rgbTest = re.compile('\d+[,\s]{1}\d+[,\s]{1}\d+')

  while True:

    c = input(tc.WHITE + inputText)
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
      print(f'{tc.YELLOW}Invalid input.')

# Converts computer brightness to human eye brightness.
def gammaCorrection(val):

  return val / 12.92 if val < 0.03928 else ((val + 0.055) / 1.055) ** 2.4

# Gets the relative luminance of a number (between 0 and 1)
def getRelativeLuminance(colour):

  r = gammaCorrection(colour['r'] / 255) * 0.2126
  g = gammaCorrection(colour['g'] / 255) * 0.7152
  b = gammaCorrection(colour['b'] / 255) * 0.0722

  return r + g + b

print(tc.PURPLE)
print('======================================================')
print('|               COLOUR CONTRAST TESTER               |')
print('======================================================\n')

c1 = inputColour(f'Enter colour #1 (hex or rgb):{tc.BLUE}\n > ')
c2 = inputColour(f'Enter colour #2 (hex or rgb):{tc.BLUE}\n > ')

l1 = getRelativeLuminance(c1)
l2 = getRelativeLuminance(c2)

contrastRatio = (l1 + 0.05) / (l2 + 0.05)
if contrastRatio < 1:
  contrastRatio = 1 / contrastRatio

statusMessage = f'{tc.GREEN}Good contrast. Works for all text.'
if contrastRatio < 3:
  statusMessage = f'{tc.RED}Bad contrast. Doesn\'t work for any text.'
elif contrastRatio < 4.5:
  statusMessage = f'{tc.YELLOW}OK contrast. Works for larger text.' 

print(tc.WHITE)
print('------------------------------------------------------\n')
print(f'Relative luminance of colour #1:    {tc.BLUE}{l1}{tc.WHITE}')
print(f'Relative luminance of colour #2:    {tc.BLUE}{l2}{tc.WHITE}')
print(f'Relative luminance of colour #1:    {tc.BLUE}{l1}{tc.WHITE}')
print(f'Contrast ratio                      {tc.BLUE}{contrastRatio}\n')
print(f'{statusMessage}{tc.WHITE}\n')
print('======================================================')
