import CSP_Solver
import csvWriter
import file_Extraction
import os
import numpy as np
import networkx as nx

#todo !!!!!!!!!!!!!! überprüfen ob das eigenwert abfragen der Matrixen korrekt ist oder ob so lösungen übersehen werden???!!!!!
# Path to the directory with the adj. Matritces files of k-regular graphs
graph_ordner_pfad = "./graphAdj/"
colorAdj_ordner_pfad = "./colorAdj/"

csvFile = "results.csv"

if __name__ == "__main__":
    dateien = os.listdir(graph_ordner_pfad)          # All files in the path specified above
    graphFiles = [f for f in dateien if "asc" in f]  #  filter for only asc datafiles
    # filter graphs where the regularity is over 5 because we have no color Matrixes for that 
    graphFiles = [f for f in graphFiles if not "6_3.asc" in f and not "7_3.asc" in f]

    dateien = os.listdir(colorAdj_ordner_pfad)
    colorAdjFiles = [f for f in dateien if "sage" in f]

    colMat = {}
    listGraphs = []
    
    for file in colorAdjFiles:
        colMat.update( file_Extraction.getColorAdjMatFromFile(colorAdj_ordner_pfad  + file) ) 
    #print(colMat.keys())
    for file in graphFiles:
        listGraphs.extend( file_Extraction.getGraphMatricsFormFile(graph_ordner_pfad  + file) )



    for graph in listGraphs[:1]: #todo wieder alle graphen prüfem
        k = graph.degree(1)
        numColors = list( colMat.keys() )
        negCount = 0
        posCount = 0

        adjGraph = nx.to_numpy_array(graph)
        #print(adjGraph)

        eigenvaluesGraph = np.round(np.linalg.eigvals(adjGraph) , decimals=8) 
        
        for nColor in numColors:
            for reg, listMat in colMat[nColor].items():
                if reg == k:
                    #print(f"Regularität: {reg} mit {len(listMat)} color Matritzen")
                    for cAM in listMat:
                        #gets eigenvalues of colMat and removes duplicates because we only have to check if they are ones in the eigenvalues of the graph adj. Mat.
                        eig =np.round(np.linalg.eigvals(cAM) , decimals=8) 
                        eigenvaluesColMat = np.unique( eig )
                        #check for eigenvalues of colMat and adj. Mat of Graph compare https://www.math.uni-bielefeld.de/~frettloe/papers/perf-gr-col.pdf Theorem 10
                        if not  np.all(np.isin(eigenvaluesColMat, eigenvaluesGraph)):
                            #print(eigenvaluesColMat)
                            negCount +=1
                            continue
                        solution = CSP_Solver.solveGraphCSP(graph,cAM)
                        csvWriter.saveColorings(csvFile, adjGraph, cAM, solution )

                        if not solution:
                            #print(f"no solution for Graph: {graph.adj} \n and a colMat: {cAM}")
                            
                            negCount +=1
                        else:
                            posCount +=1
        print(f"posCount(graph and colMat have coloring): {posCount}\n negCount: {negCount}")
