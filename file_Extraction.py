import networkx as nx
import re
import numpy as np

#
def strToAdjDicFormate(str, numNodes):
  G = nx.Graph()
  for i in range(1, numNodes+1):
      G.add_node(i)

  for s in str:
    t = s.split(":")
    x = int(t[0])
    
    for i in t[1].split():
      
      G.add_edge(x, int(i))
  #re = {int(t[0]): todo}
  print(nx.is_regular(G))
  return G

#todo die anzahl der Farben muss  noch aus dem File gelesen werden
def getGraphMatricsFormFile(fileName):
  f = open(fileName , "r")
  s = f.read()
  lis = []
  for g in s.split("Graph ")[1:]:
    graph = g.split("Taillenweite")[0].split('\n')[1:]
    finalGraph = graph[1:-1]
    lis.append(finalGraph)

    for g in lis:
      print(strToAdjDicFormate(g, 8).adj)
      print("\n")


def getColorAdjMatFromFile(fileName):
  f = open(fileName , "r")
  s = f.read()
  colorings = []
  
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
      
    # Ausgabe der extrahierten Informationen
    for match in matchesMat:
      #print(f"Gefundene Matrix: {match}")
      mat.append(np.array(match))
      
    colorings.append((typ,mat))

  for tup in colorings:
    print(tup[0])
    print(tup[1])
  







  
      
if __name__ == "__main__":
  fileName = "./08_4_3.asc"
  f = open(fileName , "r")
  s = f.read()
  #g = s.split("Graph ")
  lis = []
  testGraph = None
  for g in s.split("Graph ")[1:]:
    graph = g.split("Taillenweite")[0].split('\n')[1:]
    #print("Graph: ")
    testGraph = graph[1:-1]
    lis.append(testGraph)
    #print(graph[1:-1])
    #print("\n\n")

    #todo muss die acht noch umwandeln in die anzal der Knoten von dem Graphen
    #print(strToAdjDicFormate(testGraph, 8))
    for g in lis:
      print(strToAdjDicFormate(g, 8).adj)
      print("\n")
