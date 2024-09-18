import CSP_Solver
import csvWriter
import file_Extraction
import os
import numpy as np
import networkx as nx
import helpFunction

#todo !!!!!!!!!!!!!! überprüfen ob das eigenwert abfragen der Matrixen korrekt ist oder ob so lösungen übersehen werden???!!!!!
# Path to the directory with the adj. Matritces files of k-regular graphs
graph_ordner_pfad = "./graphAdj/"
colorAdj_ordner_pfad = "./colorAdj/"

csvFile = "results.csv"
csvFileOverview = "resultsOverview.csv"

if __name__ == "__main__":
    
    colMat = file_Extraction.getColorAdjMatFromDir(colorAdj_ordner_pfad)
    listGraphs = file_Extraction. getGraphListFromDir(graph_ordner_pfad)

    negTotal = 0
    posTotal = 0
    graphCounter = 0
    for graph in listGraphs: #[:4]: #todo wieder alle graphen prüfem
        posibleMatrixes = []
        k = graph.degree(1)
        graphCounter +=1
        numColors = list( colMat.keys() )
        negCount = 0
        posCount = 0
        adjGraph = nx.to_numpy_array(graph)

        
        for nColor in numColors:
            for reg, listMat in colMat[nColor].items():
                if reg == k:
                
                    for cAM in listMat:
                       
                        #check for eigenvalues of colMat and adj. Mat of Graph compare https://www.math.uni-bielefeld.de/~frettloe/papers/perf-gr-col.pdf Theorem 10
                        #todo check ausbauen um zu testen ob es probleme macht
                        if  not helpFunction.eigenvalueCheckPositiv(graph,cAM):
                            #print(eigenvaluesColMat)
                            negCount +=1
                            continue
                        solution = CSP_Solver.solveGraphCSP(graph,cAM)


                        if not solution:
                            #print(f"no solution for Graph: {graph.adj} \n and a colMat: {cAM}")
                            
                            negCount +=1
                        else:
                            csvWriter.saveColorings(csvFile,f"Graph no. {graphCounter}", adjGraph, cAM, solution )

                            posibleMatrixes.append(cAM)
                            posCount +=1
        print(f"posCount(graph and colMat have coloring): {posCount}\n negCount: {negCount}")
        csvWriter.saveGraphAndColoring(csvFileOverview,f"Graph no. {graphCounter}", adjGraph, posibleMatrixes)
        negTotal += negCount
        posTotal += posCount
        
    print(f"Insgesammt wurden {posTotal+negTotal} Farbinzidenzmatrizen untersucht hiervon sind {posCount} durch den eigenwert check durchgekommen und {negCount} wurden hierdurch zurückgewiesen")
