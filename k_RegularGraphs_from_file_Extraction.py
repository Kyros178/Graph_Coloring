import networkx as nx

#
def strToAdjDicFormate(str, numNodes):
  G = nx.Graph()
  for i in range(1, numNodes+1):
      G.add_node(i)

  for s in str:
    t = s.split(":")
    x = int(t[0])
    #print(x)
    #print(t[1].split( ))
    for i in t[1].split():
      #print(f"({x},{int(i)})")
      G.add_edge(x, int(i))
  #re = {int(t[0]): todo}
  print(nx.is_regular(G))
  return G

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
