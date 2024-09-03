import networkx as nx
import re
import numpy as np

#
def strToGraph(str, numNodes):
  G = nx.Graph()
  for i in range(1, numNodes+1):
      G.add_node(i)

  for s in str:
    t = s.split(":")
    x = int(t[0])
    
    for i in t[1].split():
      
      G.add_edge(x, int(i))
  #re = {int(t[0]): todo}
  # todo check if graph is regulär
  if not nx.is_regular(G):
    print("Ein ausgelesener Graph war nicht regulär Irgendwas mit dem auslesen stimmt nicht \n ERROR!!!!!!!!!!!!!!!!")
  
  return G

#todo die anzahl der Farben muss  noch aus dem File gelesen werden
def getGraphMatricsFormFile(fileName):
  print(f"Get Graphs from file: {fileName}")
  numNodes = int( fileName.split("/")[-1].split("_")[0] )

  f = open(fileName , "r")
  s = f.read()
  lis = []
  result = []
  for g in s.split("Graph ")[1:]:
    #print(g)
    #print("test")
    graph = g.split("Taillenweite")[0].split('\n')[1:]
    finalGraph = graph[1:-1]
    lis.append(finalGraph)

  for g in lis:
    result.append( strToGraph(g, numNodes) )

  return result


def getColorAdjMatFromFile(fileName):
  print(f"Get Colorings from file: {fileName}")
  f = open(fileName , "r")
  s = f.read()
  colorings = {}
  numCol = 0
  
  for g in s.split("#")[1:]:
    
    # Regulärer Ausdruck, um alle 'Matrix(...)' Einträge zu finden
    patternMat = r'Matrix\((.*?)\)'

    patternColorTyp = r'l\d{2}'

    # Alle passenden Einträge extrahieren
    matchesMat = re.findall(patternMat, g)

    matchesColorTyp = re.findall(patternColorTyp, g)

    
    typ = ""
    mat = []

    for match in matchesColorTyp:
      #print(f"Gefundener Farb Typ: {match}")
      typ = match
      numCol = typ[1]
      
    # Ausgabe der extrahierten Informationen
    for match in matchesMat:
      #print(f"Gefundene Matrix: {match}")
      mat.append(np.array(match))
      
    colorings[int(typ[2])] = mat

#  for tup in colorings:
 #   print(tup[0])
  #  print(tup[1])
  result = {int(numCol): colorings}
  #print(f"Colors: {numCol}")

  return result








  
      
if __name__ == "__main__":
  fileName = "./graphAdj/08_4_3.asc"
  result = getGraphMatricsFormFile(fileName)

