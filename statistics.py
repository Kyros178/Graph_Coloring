import csvWriter
import file_Extraction
import os
import numpy as np
import networkx as nx
from  brutForceSolver import bruteForce
import time
import CSP_Solver

graph_ordner_pfad = "./graphAdj/"
colorAdj_ordner_pfad = "./colorAdj/"

def vergleicher(graphs,colMats):
    numNodes =  graphs[0].number_of_nodes()
    reg = len( list(graphs[0].neighbors(1) ) )
    print(numNodes,reg)
    start_time = time.time()
    #bruteForce
    for g in graphs:
        for c_A_M in colMats:
            bruteForce(g,c_A_M)
    end_time = time.time()

    bruteForce_time = end_time - start_time

    start_time = time.time()
    
    for g in graphs:
        for c_A_M in colMats:
            solution = CSP_Solver.solveGraphCSPBadConstraints(g,c_A_M)
            print(solution)
    end_time = time.time()

    CSPSolverBad_time = end_time - start_time

    start_time = time.time()
    
    for g in graphs:
        for c_A_M in colMats:
            solution = CSP_Solver.solveGraphCSP(g,c_A_M)
            print(solution)
    end_time = time.time()

    CSPSolverOpt_time = end_time - start_time

    print(
        f"Time Brute Force: {bruteForce_time}  \n \
        Time CSP Solver badConstraints: {CSPSolverBad_time}\
        Time CSP Solver Optimiert: {CSPSolverOpt_time}")

            

if __name__ == "__main__":
    dateien = os.listdir(colorAdj_ordner_pfad)
    colorAdjFiles = [f for f in dateien if "sage" in f]

    # key 1 is the color and key 2 is the regularity
    colMat = {}
   
    
    for file in colorAdjFiles:
        colMat.update( file_Extraction.getColorAdjMatFromFile(colorAdj_ordner_pfad  + file) )

    
    # key 1 is the number of nodes and  key 2 is the regularity
    graphs = {}
    
    dateien = os.listdir(graph_ordner_pfad)          # All files in the path specified above
    graphFiles = [f for f in dateien if "asc" in f]  #  filter for only asc datafiles
    # filter graphs where the regularity is over 5 because we have no color Matrixes for that 
    graphFiles = [f for f in graphFiles if not "6_3.asc" in f and not "7_3.asc" in f]

    for file in graphFiles:
        numNodes =int(  file.split("_")[0] )
        reg = int(  file.split("_")[1] )
        #print(f"Nodes: {numNodes}, Regulraität: {reg}")
        #print(file)
        if not numNodes in graphs.keys():
            dict = {} 
            dict[reg] = file_Extraction.getGraphMatricsFormFile(graph_ordner_pfad  + file)
            graphs[numNodes] = dict
        else:
            dict = {}
            dict[reg] = file_Extraction.getGraphMatricsFormFile(graph_ordner_pfad  + file)
            graphs[numNodes].update(dict)


    #print(len( list(graphs[8][4][0].neighbors(1)) ))

   
    vergleicher(graphs[7][4], colMat[3][4])
   


   
