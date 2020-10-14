class Node:
  """
  little dot
  """
  def __init__(self, name, word):
    self.name = name
    self.word = word
    self.winner = 0

  def getName(self):
    return self.name

  def isWord(self):
    return self.word

  def __str__(self):
    return self.name

  def setWinner(self, winner):
    """winner is an integer, either 1 or 2 representing whether the word is a goal word for player 1 or 2"""
    self.winner = winner
  
  def getWinner(self):
    """get whether the winner is 1 or 2 for this word"""
    return self.winner

  # 3 functions below from https://stackoverflow.com/questions/4901815/object-of-custom-type-as-dictionary-key/4901847

  def __hash__(self):
    return hash((self.name))

  def __eq__(self, other):
    return (self.name) == (other.name)

  def __ne__(self, other):
    # Not strictly necessary, but to avoid having both x==y and x!=y
    # True at the same time
    return not(self == other)

class Edge:
  """
  connecting boi
  """  
  def __init__(self, src, dest):
    """
    src and dest are nodes
    """
    self.src = src
    self.dest = dest
  
  def getSource(self):
    return self.src
  
  def getDest(self):
    return self.dest

  def __str__(self):
    return self.src.getName() + "-->" + self.dest.getName()

class Graph(object):
  """
  'look at this graph' - Nickelback
  """
  def __init__(self, edges = {Node("", False):[]}):
    self.edges = edges
    for i in edges.keys():
      if i.getName() == "":
        self.root = i
        break 

  def addNode(self, node):
    """adds a unique node to the array, returns the node"""
    if node in self.edges:
      raise ValueError("NodeError")
    else:
      self.edges[node] = []
    return node

  def addEdge(self, edge):
    """adds a unique edge to the graph, with existing nodes
    returns edge if successful, otherwise returns -1 or keyerror"""
    dest = edge.getDest()
    src = edge.getSource()
    if type(dest) != Node or type(src) != Node:
      return -2
    if dest in self.edges[src] or dest == src:
      return -1
    if dest not in self.edges.keys() or src not in self.edges.keys():
      raise KeyError(f"Invalid Src/Dest {src}, {dest}")
    self.edges[src].append(dest)
    return edge
  
  def getChildren(self, node):
    """
    returns a list of the children of the node
    """
    return self.edges[node]
  
  def getRoot(self):
    """returns the root node"""
    return self.root
  
  def getNode(self, name):
    """returns the node with name 'name', if not found, returns -1"""
    for i in self.edges.keys():
      if i.getName() == name:
        return i
    return -1

  def delNode(self, node):
    """deletes the node with the name 'name', if not found, returns -1"""
    self.edges.pop(node, None)

  def __str__(self):
    disp = []
    for i in self.edges.items():
      disp.append([i[0].getName(), [j.getName() for j in i[1]]])

    return str(disp)
