import json
from string import ascii_lowercase

def loadWords(filepath):
  """
  Imports all words from dictionary, returns words as a dict with values of 1.
  Current dictionary used: filtered version of ubuntu dictionary, with no words < 4 char long, proper nouns, or possessive words with apostrophes
  """
  with open(filepath, "r") as f:
    return json.load(f)

def gameSetup():
  """
  Initial Game Setup. Returns a string - Player Name.
  """
  with open("gameinfo.txt") as f:
    text = f.read()
  print(text)
  return input("Enter your name: ").strip()

def isWord(word, wordlist):
  """
  Checks whether or not word is in wordlist.
  Returns TRUE/FALSE: whether or not the challenge was successful.
  Note: passing large lists between functions *should* be done by reference, so having wordlist as an input shouldnt be a problem.
  """
  #TODO: check if current word is in dictionary
  
  if len(word) >= 4:
    if word.lower() in wordlist:
      return (True)
    return False
  return False

def promptWord(word, wordlist, name):
  """
  Word is the current word, wordlist is the dictionary, prevPlayer is the previous player.
  Prompts the previous player which word they were going for.
  Returns True/False: whether or not the challenge is successful.
  """
  while True:
    challengeWord = input(f"    {name}, which word were you going for? Spell it exactly. ").lower()
    if challengeWord.isalpha() and (word in challengeWord):
      break 
    else:
      print("      Invalid input. Make sure the current word is a substring of what you're trying to spell.")
  return False if isWord(challengeWord, wordlist) else True

def challengePrompt(word, name):
  """
  Prompt the player the manner in which they would like to challenge.
  Returns either "w" or "a" indicating the mode of challenge.
  """
  while True:
    challengeOption = input(f"    {name}, how would you like to challenge?\n\
    --> Type w if you think the current letters form a word.\n\
    --> Type a to ask Zyka which word they were going for. ").lower()

    if challengeOption == "w" or challengeOption == "a":
      break
    else:
      print("    Invalid input, try again.")
  return challengeOption
    

def parseInput(inp, word):
  """
  inp is a string representing player input for the current turn.
  word is a string representing the current string of letters in play

  Parses each turn input made by players.

  On a regular turn, parseInput returns the updated word.
  If the input indicates a challenge, parseInput returns -1.
  If the input is invalid, parseInput returns -2.
  If the input indicates help, parseInput returns -3.
  """
  line = [i.lower() for i in inp.split()]
  lenInput= len(line)

  if lenInput > 1 or lenInput== 0:
    return -2

  else:
    line = line[0]
    challenge = ["/ch", "/chal", "/challenge"]
    helptext = ["/h", "/help"]
    if line in challenge:
      return -1
    if line in helptext:
      return -3
    elif word in line and len(word) + 1 == len(line) and line.isalpha:
      return line
    else:
      return -2


