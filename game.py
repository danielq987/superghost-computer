import json
from helper import *
from treeClasses import Node, Edge, Graph
from statistics import median
import time
import random
import pickle

def loadTree(filepath):
  """loads the already constructed tree from a .p file specified by filepath"""
  print(f">> Loading...")
  return pickle.load(open(filepath, "rb"))

def playerWin(name):
  time.sleep(1)
  print(f"\n{name} wins this round!\n")
  score[0] += 1

def zykaWin():
  time.sleep(1)
  print("\nZyka wins this round!\n")
  score[1] += 1

def playerTurn(curWord, name):
  """Returns updated curWord if a letter was played, -1 for challenge, and -2 for invalid input"""
  parsed = parseInput(input(f"  {name}'s Turn: "), curWord)

  # Challenge
  if parsed == -1:
    successful = True

    # prompt player for type of challenge
    challengeOption = challengePrompt(curWord, name)
    
    # player thinks current word is a word
    if challengeOption == "w":
      successful = isWord(curWord, words)
    # player thinks Zyka is bluffing (although she never bluffs :D)
    else:
      node = tree.getNode(curWord)
      if type(node) == int:
        successful = True
      else:
        while tree.getChildren(node) != []:
          node = tree.getChildren(node)[0]
        time.sleep(1)
        print(f"  Zyka was going for {node.getName()}!")
        successful = False
    
    if successful:
      print(f"  {name}'s challenge was successful!")
      playerWin(name)

    else:
      print(f"  {name}'s challenge was not successful...")
      zykaWin()
    
    return parsed

  elif parsed == -2:
    print("  Invalid Input.")
    return parsed

  else:
    curWord = parsed
    return curWord

def zykaTurn(curWord, name):
  """Returns curWord if a letter is played, -1 if Zyka challenges/round ends"""
  def takeFirst(elem):
    return elem[0]

  zturn = len(curWord) % 2 + 1
  if isWord(curWord, words):
    print("    Zyka thinks this is a word! Checking...")
    time.sleep(1)
    print(f"    {curWord} is a word.")
    zykaWin()
    return -1
  node = tree.getNode(curWord)
  if type(node) == int:
    print("  Zyka challenges.")
    if promptWord(curWord, words, name):
      print(f"      Unfortunately, that is not a valid word.")
      zykaWin()
    else:
      playerWin(name)
    return -1
  
  # zyka deciding play - if the current word is a winning word, choose a random child which wins
  if node.getWinner() == zturn:
    wins = []
    for child in tree.getChildren(node):
      if child.getWinner() == zturn:
        wins.append(child) 
    choice = random.choice(wins)
    return choice.getName()
  
  # if the current word isnt winning, choose the child with most winning subchildren
  else:
    children = tree.getChildren(node)
    ratios = []
    for child in children:
      subchildren = tree.getChildren(child)
      subLeng = len(subchildren)
      if subLeng != 0:
        subWinnerCount = 0 
        for subchild in subchildren:
          if subchild.getWinner() == zturn:
            subWinnerCount += 1
        ratios.append((subWinnerCount/subLeng, child))
    ratios.sort(key=takeFirst)
    choice = random.choice(ratios[:5])
    return choice[1].getName()    

tree = loadTree("tree/tree.p")
words = loadWords("tree/u.txt")
score = [0,0] # First element is player score, second element is zyka score

def main():
  """
  main code
  """
  name = gameSetup()
  turn = 0
  roundNum = 1

  # Looping over each round
  while True:
    print(f"Round {roundNum}!")
    curWord = ""
    endRnd = False
    
    # Looping over each individual turn
    while endRnd != True:
      print("")
      # player turn
      if turn % 2  == 0:
        a = playerTurn(curWord, name) 
        if a == -1:
          endRnd = True
        elif a == -2:
          turn -= 1
        else:
          curWord = a
        turn += 1
      
      # computer turn
      else:
        print("  Zyka's Turn...")
        time.sleep(1)
        a = zykaTurn(curWord, name)
        if type(a) == int:
          endRnd = True
        else:
          curWord = a
          print(f"  Zyka played: {curWord}")
        turn += 1

    curWord = ""
    roundNum += 1
    print(f"{name}: {score[0]} | Zyka: {score[1]}\n")
    time.sleep(1)
    
    
if __name__ == "__main__":
  main()