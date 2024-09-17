import os
import networkx as nx
import numpy as np
import inspect
import pynauty as nauty
import file_Extraction
import CSP_Solver
import csvWriter

def k_con(g):
        max = 0
        for i in range(1,12):
                if nx.is_k_edge_connected(g, i):
                        max = i
                else:
                        return max
        return max

def importantGraphs():
    #Platonic Graphs
    graphenUndNamen = {
        "Tetrahedral-Graph": nx.tetrahedral_graph(),
        #"Würfel-Graph": nx.cubical_graph(),
        "Octahedral-Graph": nx.octahedral_graph(),
        "Dodecahedral-Graph": nx.dodecahedral_graph(),
        "Icosahedral-Graph": nx.icosahedral_graph(),
        "Petersen-Graph":nx.petersen_graph()
    }

    for n in range(1,6):
        B = nx.complete_bipartite_graph(n, n)
        num = str(n)
        graphenUndNamen["K_{"+num+","+num+"}"] = B

    for i in range(1,11):
        num = str(i)
        
        graphenUndNamen["K_{"+num+"}"] = nx.complete_graph(i)  # d-simplex
        #graphenUndNamen[f"Hypercube_dim={i}"] = nx.hypercube_graph(i)

    return graphenUndNamen



colorAdj_ordner_pfad = "./colorAdj/"

if __name__ == "__main__":

    

    listGraphs = importantGraphs()
    
    dateien = os.listdir(colorAdj_ordner_pfad)
    colorAdjFiles = [f for f in dateien if "sage" in f]
    colMat = {}

    
    for file in colorAdjFiles:
        colMat.update( file_Extraction.getColorAdjMatFromFile(colorAdj_ordner_pfad  + file) )

        
    head = ("Name: ", " Regularität: ", " k-zusammenhangs Zahl: "," Anzahl Knoten: "," Anzahl Automorphismen: ", " Anzahl ColMat m. Färb.: "," Anzahl Färbungen: ")
    for (name,graph) in listGraphs.items():
        
        node = list(graph.nodes())[0]
        reg = len(list( graph.neighbors(node )))
        conectNum = k_con(graph)
        numNodes = graph.number_of_nodes()
        
        G_nauty = nauty.Graph(numNodes)
        # Füge die Kanten aus dem NetworkX-Graphen hinzu
        for n in graph.nodes:
            G_nauty.connect_vertex(n, list(graph.neighbors(n)) )

        automorphism_group = nauty.autgrp(G_nauty )
        num = float(automorphism_group[1])
        offset = float( automorphism_group[2])
        autSize = num * (10**offset)

    
        numColorings = 0
        numPosColInzMat = 0
        for c in range(2,5):
            if not reg in colMat[c].keys():
                print("regularitäts probleme")
                continue
            for cAM in colMat[c][reg]:
                adjGraph = nx.to_numpy_array(graph)
                eigenvaluesGraph = np.round(np.linalg.eigvals(adjGraph) , decimals=8)
                eig =np.round(np.linalg.eigvals(cAM) , decimals=8)
                eigenvaluesColMat = eig # unique wurde hier weggelassen
                if not  np.all(np.isin(eigenvaluesColMat, eigenvaluesGraph)):
                    continue
                    
                result = CSP_Solver.solveGraphCSP(graph,cAM)
                
                if result:
                    numColorings += len(result)
                    numPosColInzMat += 1


                    
        info = (name,  reg, conectNum ,  numNodes, autSize,numPosColInzMat, numColorings)
        print(head)
        print(info)
