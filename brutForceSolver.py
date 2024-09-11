
import numpy as np
import networkx as nx


'''
BruteForce testet einfach alle möglichen Färbungen die durch die Funktion colorings gegeben ist darauf ob sie zu der color adj. Matr. passen.
 dies wird in der Funktion correctColoring für jede färbung getan indem für jeden knoten geprüft wird ob die Nachbarn die richtige quantität der Farben hat 
Also das ein Knoten der Farbe i die richtige anzahl an nachbarn mit der Farbe j haben. Todo: testen ob die implementation passt
'''



def colorings(graph, numCol):
  numN = graph.number_of_nodes()
  numRow = numCol**numN
  arr = np.zeros((numRow,numN),dtype=int)
  for col in range(numN):
    for row in range(numRow):
      # col = spalten
      #row = zeile
      arr[row][col] =   np.floor(row/(numCol**col ) )  % numCol

  return arr



# der 4 simplex müsste der K_5 sein
# todo probleme mit Graphen erwehnen wo der erste Knoten die Nummer 0 oder 1 hat!!!
def correktCollorring(G ,col, c_A_M):
  l = len(c_A_M[0])
  for n in G.nodes:
    sum = np.zeros(l)
    colorOfN = col[n-1]

    for n2 in G.adj[n]:
      colorOfN2 = col[n2-1]
      sum[colorOfN2] += 1
    if not np.array_equal(sum , c_A_M[colorOfN]):
      return False
  return True





def bruteForce(G, c_A_M):
  numberOfColors = len(c_A_M[0])
  cols = colorings(G,numberOfColors)
  results = []
  for c in cols:
    if correktCollorring(G, c, c_A_M):
      #print("Eine mögliche Färbung ist: ")
      #print(c)
      results.append(c)
  return results




if __name__ == "__main__":
  K_5 = nx.complete_graph(5)
  print(K_5.nodes() )

  
  colMat = np.array([[0,4],[1,3]])
  #print(colMat)

  #probleme mit der nummerierung aus datei ist es von 1 und natürlich wäre es von 0
  #bruteForce(K_5,colMat)
