"""===========================================================================
| TEXT COLOUR CONTRAST CALCULATOR
|   By: Max Huang
|   Last edited: May 3rd, 2020
|
| This program calculates the colour contrast between two colours in
| accordance with W3C's Web Content Accessibility Guidelines.
==========================================================================="""

import time, re, colorama
colorama.init()

# Terminal colours.
class tc:

  useColour = True
  
  PURPLE = '\033[95m' if useColour else ''
  BLUE   = '\033[94m' if useColour else ''
  GREEN  = '\033[92m' if useColour else ''
  YELLOW = '\033[93m' if useColour else ''
  RED    = '\033[91m' if useColour else ''
  WHITE  = '\033[0m'  if useColour else ''

# Returns the match if success (False if fail).
def exactMatch(regex, findStr):

  finds = regex.findall(findStr)
  return finds[0] if len(finds) == 1 else False

# Allows for the input of a colour in RGB or hex. Runs until valid input.
def inputColour(inputText, textColour=tc.WHITE, inputColour=tc.BLUE):

  hexTest = re.compile('#[a-fA-F0-9]{6}')
  rgbTest = re.compile('\d+[,\s]{1}\d+[,\s]{1}\d+')

  while True:

    print(f'{textColour}{inputText}{inputColour}')
    c = input(' > ')
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

# Gets the relative luminance of a number (between 0 and 1).
def getRelativeLuminance(colour):

  r = gammaCorrection(colour['r'] / 255) * 0.2126
  g = gammaCorrection(colour['g'] / 255) * 0.7152
  b = gammaCorrection(colour['b'] / 255) * 0.0722

  return r + g + b

# Gets the WCAG score (Fail, AA, AAA). AAA score is optional.
def WCAGScore(variable, AAThreshold, AAAThreshold=-1):

  if variable < AAThreshold:
    return f'{tc.RED}Fail'

  if AAAThreshold == -1:
    return f'{tc.GREEN}AA'

  if variable < AAAThreshold:
    return f'{tc.YELLOW}AA'
  return f'{tc.GREEN}AAA'


firstRun = True
runAgain = 'y'

while runAgain == 'y' or runAgain == 'Y':

  if firstRun:
    print(f'{tc.PURPLE}*================================================================*')
    print('| TEXT COLOUR CONTRAST CALCULATOR                                |')
    print('|                                                                |')
    print('| In accordance with W3C\'s Web Content Accessibility Guidelines. |')
    print('*================================================================*\n')
  else:
    print(tc.PURPLE)
    print('==================================================================\n')

  c1 = inputColour(f'Enter colour 1 (hex or rgb):')
  c2 = inputColour(f'Enter colour 2 (hex or rgb):')

  l1 = getRelativeLuminance(c1)
  l2 = getRelativeLuminance(c2)

  contrastRatio = (l1 + 0.05) / (l2 + 0.05)
  if contrastRatio < 1:
    contrastRatio = 1 / contrastRatio

  normalTextScore      = WCAGScore(contrastRatio, 4.5, 7)
  largeTextScore       = WCAGScore(contrastRatio, 3, 4.5)
  graphicalObjectScore = WCAGScore(contrastRatio, 3)

  print(tc.WHITE)
  print('------------------------------------------------------------------\n')
  print(f'Relative luminance of colour 1:    {tc.BLUE}{l1}{tc.WHITE}')
  print(f'Relative luminance of colour 2:    {tc.BLUE}{l2}{tc.WHITE}')
  print(f'Contrast ratio                     {tc.BLUE}{contrastRatio}')

  print(tc.WHITE)
  print('Contrast ratings for...')
  print(f' - Normal text:          {normalTextScore}{tc.WHITE}')
  print(f' - Large text:           {largeTextScore}{tc.WHITE}')
  print(f' - Graphical objects:    {graphicalObjectScore}')

  print(tc.WHITE)
  print(f'Run again? (y/n){tc.BLUE}')
  runAgain = str(input(' > ')[0])
  firstRun = False

print(tc.WHITE)
print('Closing...')
time.sleep(1)
