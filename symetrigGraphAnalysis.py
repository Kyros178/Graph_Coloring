import os
import networkx as nx
import numpy as np
import inspect

import file_Extraction
import CSP_Solver
import csvWriter
import helpFunction




colorAdj_ordner_pfad = "./colorAdj/"
filename = "symAnalyse.csv"

if __name__ == "__main__":

    

    listGraphs = helpFunction.importantGraphs()
    colMat =  file_Extraction.getColorAdjMatFromDir(colorAdj_ordner_pfad)

    
        
    
    for (name,graph) in listGraphs.items():
        info = helpFunction.importantGraphInfo(name,graph)
        reg = info["Reg"]
        
    
        numColorings = 0
        numPosColInzMat = 0
        for c in range(2,5):
            if not reg in colMat[c].keys():
                print("regularitäts probleme")
                continue
            for cAM in colMat[c][reg]:
                
               
                if not helpFunction.eigenvalueCheckPositiv(graph,cAM):
                    continue
                    
                result = CSP_Solver.solveGraphCSP(graph,cAM)
                
                if result:
                    numColorings += len(result)
                    numPosColInzMat += 1


                    
        csvWriter.saveSymInfo(filename,info,numPosColInzMat, numColorings)
        
        print(info)
