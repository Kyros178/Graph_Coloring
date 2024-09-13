from re import T
from constraint import *
import numpy as np
import networkx as nx


def create_Constrains(graph, c_A_M, numberOfColors):
    functions = []
    for nodeToCheck in graph.nodes:
        neighbors = graph.neighbors(nodeToCheck)


        def f(*arg):
          sum = np.zeros(numberOfColors)
          # counts the number for each color in the "nachbarschaft" of nodeToCheck
          for color in arg[1:]:
            sum[color] +=1

          if not np.array_equal(sum , c_A_M[arg[0]]):
            return False
          return True

        var = []
        var.append(nodeToCheck)
        var.extend(neighbors)
        functions.append((f,var))
    return functions


def solveGraphCSP(graph,c_A_M) -> [dict]:
  numberOfColors =  len(c_A_M[0])

  constrainsTuple = create_Constrains(graph, c_A_M, numberOfColors)
  problem = Problem()

  for n in graph.nodes:
    problem.addVariable(n, range(numberOfColors))

  for (f,var) in constrainsTuple:
    problem.addConstraint(FunctionConstraint(f),var)

  s= problem.getSolutions()
  return s

def getColorings(s):
  lastColorring = []
  for sol in s:
    col = []
    for i in range(len(sol.keys())):
      col.append(sol[i])
    lastColorring.append( col )
  return lastColorring




def solveGraphCSPBadConstraints(G,c_A_M) -> [dict]:
    
    numberOfColors = len(c_A_M[0])
    problem = Problem()
    for n in G.nodes:
       problem.addVariable(n, range(numberOfColors))




    def check(*arg):
        #numberOfColors = len(c_A_M[0])
        for i in range(len(arg)) :
            sum = np.zeros(numberOfColors)
            for j in G.neighbors(i+1) :
                #todo rausfinden ob das probleme macht da die knoten in meinem Graphen bei 1 anfangen
                sum[arg[j-1]] += 1

            if not np.array_equal(sum , c_A_M[arg[i]]):
                   return False
        return True


    problem.addConstraint(FunctionConstraint(check))


    s= problem.getSolutions()

    return s
