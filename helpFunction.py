import networkx as nx
import numpy as np
import pynauty as nauty



#@profile
def eigenvalueCheckPositiv(graph,cAM):
    dec = 4
    adjGraph = nx.to_numpy_array(graph)
    #print(adjGraph)
    eigenvaluesGraph = np.round(np.linalg.eigvals(adjGraph) , decimals=dec) 
    #gets eigenvalues of colMat and removes duplicates because we only have to check if they are ones in the eigenvalues of the graph adj. Mat.
    eig = np.round(np.linalg.eigvals(cAM) , decimals=dec) 
    eigenvaluesColMat = np.unique( eig )

    #check for eigenvalues of colMat and adj. Mat of Graph compare https://www.math.uni-bielefeld.de/~frettloe/papers/perf-gr-col.pdf Theorem 10
    return  np.all(np.isin(eigenvaluesColMat, eigenvaluesGraph))

#@profile
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

        if i < 5:
            G = nx.hypercube_graph(i)
            new_labels = {node: index for index, node in enumerate(G.nodes())}
            GnewNodes = nx.relabel_nodes(G, new_labels)
            graphenUndNamen[f"Hypercube_dim={i}"] = GnewNodes
        
    return graphenUndNamen

#@profile
def importantGraphInfo(name,graph):
    head = ["Name: ", " Regularität: ", " k-zusammenhangs Zahl: "," Anzahl Knoten: "," Anzahl Automorphismen: ", " Anzahl ColMat m. Färb.: "," Anzahl Färbungen: "]
    node = list(graph.nodes())[0]
    reg = int(len(list( graph.neighbors(node ))))
    conectNum = k_con(graph)
    numNodes = graph.number_of_nodes()
    G_nauty = nauty.Graph(numNodes)
    # Füge die Kanten aus dem NetworkX-Graphen hinzu
    if 0 in graph.nodes:
        for n in graph.nodes:
            G_nauty.connect_vertex(n, list(graph.neighbors(n)) )
    else:
        for n in graph.nodes:
            # Graphen aus datei fangen mit 1 an und müssen auf 0 runtergesetzt werden
            G_nauty.connect_vertex(n-1, [i-1 for i in list(graph.neighbors(n))] )
    

    automorphism_group = nauty.autgrp(G_nauty )
    num = float(automorphism_group[1])
    offset = float( automorphism_group[2])
    autSize = num * (10**offset)
    adjGraph = nx.to_numpy_array(graph)
    info = {
        "Name": name,
        "Reg": reg,
        "k-zusmZahl": conectNum ,
        "numNodes": numNodes,
        "autGrupSize": autSize,
    }

    return info




if __name__ == "__main__":

    print("test")
    importantGraphs()
