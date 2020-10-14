import json
from helper import *
from treeClasses import Node, Edge, Graph
from statistics import median
import time
import random
import pickle

def loadTree(filepath):
  """
  loads the already constructed tree from a .p file specified by filepath
  """
  print(f">> Loading...")
  return pickle.load(open(filepath, "rb"))

def playerWin(name):
  """
  Displays win text for player with player name and adds 1 to their score.
  """
  time.sleep(1)
  print(f"\n{name} wins this round!\n")
  score[0] += 1

def zykaWin():
  """
  Displays win text for Zyka and adds 1 to her score.
  """
  time.sleep(1)
  print("\nZyka wins this round!\n")
  score[1] += 1

def playerTurn(curWord, name):
  """
  Returns updated curWord if a letter was played, -1 for challenge, and -2 for invalid input
  """
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
      # Check if Zyka has a word in mind
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

  elif parsed == -3:
    print(helptxt)
    return -2
  
  elif parsed == -2:
    print("  Invalid Input. Type /help for help.")
    return parsed

  else:
    curWord = parsed
    return curWord

def zykaChoose(node, zturn):
  """
  Returns a string/word that Zyka chooses to play. Node is the node in the tree corresponding to the current letters in play.
  Decisions: if there are guaranteed wins, choose between one of those randomly
  If there are no guaranteed winning moves, choose between the top 5 children of the node with highest win probability.
  """
  def takeFirst(elem):
    """
    function to ensure sorting is only done by the first element of the tuple
    """
    return elem[0]

  # makes an array of tuples (win%, node) for possible moves
  moves = []
  # node is a guaranteed win
  if node.getWinner() == zturn:
    for child in tree.getChildren(node):
      if child.getWinner() == zturn:
        moves.append((1, child))
    # choose randomly between moves that win
    choice = random.choice(moves)
  
  # if the current word isnt winning, choose the child with most winning subchildren
  else:
    children = tree.getChildren(node)
    # iterates over all children nodes
    for child in children:
      subchildren = tree.getChildren(child)
      subLeng = len(subchildren)
      # check if andy subchildren exist
      if subLeng != 0:
        subWinnerCount = 0 
        # iterates over all subchildrent to find their winner values
        for subchild in subchildren:
          if subchild.getWinner() == zturn:
            subWinnerCount += 1
        moves.append((subWinnerCount/subLeng, child))
      # no subchildren - child.getName is a word
      else:
        moves.append((-1, child))
    # sorts the children and takes the ones with the highest probabilities
    moves.sort(key=takeFirst)
    try:
      choice = random.choice(moves[:5])
    except:
      choice = moves[0]
  # returns the chosen word
  return choice[1].getName()    

def zykaTurn(curWord, name):
  """
  Returns Zyka's move if a letter is played, and -1 if Zyka challenges/round ends.
  """

  zturn = len(curWord) % 2 + 1
  # the letters in play form a valid word
  if isWord(curWord, words):
    print("    Zyka thinks this is a word! Checking...")
    time.sleep(1)
    print(f"    {curWord} is a word.")
    zykaWin()
    return -1
  node = tree.getNode(curWord)

  # the letters in play are not a substring of any valid word
  if type(node) == int:
    print("  Zyka challenges.")
    if promptWord(curWord, words, name):
      print(f"      Unfortunately, that is not a valid word.")
      zykaWin()
    else:
      playerWin(name)
    return -1
  
  # zyka playing a letter
  return zykaChoose(node, zturn)

tree = loadTree("tree/tree.p")
words = loadWords("tree/u.txt")

with open("help.txt", 'r') as f:
  helptxt = f.read()

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
        # Challenge
        if a == -1:
          endRnd = True
        # Invalid input, turn doesn't increment
        elif a == -2:
          turn -= 1
        # Regular turn
        else:
          curWord = a
        turn += 1
      
      # computer turn
      else:
        print("  Zyka's Turn...")
        time.sleep(1)
        a = zykaTurn(curWord, name)
        # challenge
        if type(a) == int:
          endRnd = True
        # regular turn
        else:
          curWord = a
          print(f"  Zyka played: {curWord}")
        turn += 1

    # ending the round
    curWord = ""
    roundNum += 1
    print(f"{name}: {score[0]} | Zyka: {score[1]}\n")
    time.sleep(1)
    
    
if __name__ == "__main__":
  main()