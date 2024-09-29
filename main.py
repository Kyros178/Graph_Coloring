import CSP_Solver
import csvWriter
import file_Extraction
import os
import numpy as np
import networkx as nx
import helpFunction
import sys
import time
import cProfile

#todo !!!!!!!!!!!!!! überprüfen ob das eigenwert abfragen der Matrixen korrekt ist oder ob so lösungen übersehen werden???!!!!!
# Path to the directory with the adj. Matritces files of k-regular graphs
graph_ordner_pfad = "./graphAdj/"
colorAdj_ordner_pfad = "./colorAdj/"

csvFile = "results.csv"
csvFileOverview = "resultsOverview.csv"
fileCsvSymAna = "resultsForSymAnalyse.csv"

#@profile
def main():
    colMat = file_Extraction.getColorAdjMatFromDir(colorAdj_ordner_pfad)
    listGraphs = file_Extraction. getGraphListFromDir(graph_ordner_pfad)

    negTotal = 0
    posTotal = 0
    graphCounter = 0
    print("anzahl Graphen: ", len(listGraphs) )
    start_time = time.time() 
    for graph in listGraphs: #[:4]: #todo wieder alle graphen prüfem

        posibleMatrixes = []
        
        graphCounter +=1
        info = helpFunction.importantGraphInfo(f"Graph no. {graphCounter}",graph)
        k = info["Reg"]
        numColors = list( colMat.keys() )
        negCount = 0
        posCount = 0
        noSolutionCounter = 0
        adjGraph = nx.to_numpy_array(graph)
        numColorInzMatWithColoring = 0
        numColorings = 0
        
        for nColor in numColors:
            for reg, listMat in colMat[nColor].items():
                if reg == k:
                
                    for cAM in listMat:
                        eigValCheckResult = False
                        #check for eigenvalues of colMat and adj. Mat of Graph compare https://www.math.uni-bielefeld.de/~frettloe/papers/perf-gr-col.pdf Theorem 10
                        #todo check ausbauen um zu testen ob es probleme macht
                        if not helpFunction.eigenvalueCheckPositiv(graph,cAM):
                            #print(eigenvaluesColMat)
                            eigValCheckResult = False
                            negCount +=1
                            continue   # continue auskommentieren um zu tesssten ob Eigenwerttest Matritzen ausschließt die  eine Lösung haben
                        else:
                            eigValCheckResult = True
                            posCount +=1
                        solution = CSP_Solver.solveGraphCSP(graph,cAM)
                        

                        if not solution:
                            #print(f"no solution for Graph: {graph.adj} \n and a colMat: {cAM}")
                            
                            noSolutionCounter  +=1
                        else:
                            # check if eigenvalue test was negativ but problem has coloring -> error
                            if not eigValCheckResult:
                                print("Error da test auf Eigenwert Negativ aber es gibt Färbung!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                print(f"Graph no. {graphCounter}", adjGraph, cAM, solution)
                                sys.exit()
                            csvWriter.saveColorings(csvFile,f"Graph no. {graphCounter}", adjGraph, cAM, solution )
                            numColorInzMatWithColoring += 1
                            numColorings += len(solution)
                            posibleMatrixes.append(cAM)

        csvWriter.saveSymInfo( fileCsvSymAna,info,numColorInzMatWithColoring, numColorings) 
        print(f"Der Graph hatte eine Regularität von {k} und hierbei konnten  {negCount} Kombinationen ausgeschlossen werden und {posCount} Paare mussten überprüft werden\n hiervon hatten {noSolutionCounter } keine Lösung")
        csvWriter.saveGraphAndColoring(csvFileOverview,f"Graph no. {graphCounter}",info,numColorInzMatWithColoring, numColorings, adjGraph, posibleMatrixes)
        negTotal += negCount
        posTotal += posCount
        
    print(f"Insgesammt wurden {posTotal+negTotal} Farbinzidenzmatrizen untersucht hiervon sind {posTotal} durch den eigenwert check durchgekommen und {negTotal} wurden hierdurch zurückgewiesen")
    end_time = time.time()
    print(f"Benötigte Zeit in Sekunden: {end_time - start_time }")
    

if __name__ == "__main__":
    #cProfile.run('main()')
    main()
