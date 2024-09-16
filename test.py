import os
import networkx as nx
import inspect
import file_Extraction

def k_con(g):
        max = 0
        for i in range(1,12):
                if nx.is_k_edge_connected(g, i):
                        max = i
                else:
                        return max
        return max


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

for i in range(1,5):
        num = str(i)
        
        graphenUndNamen["K_{"+num+"}"] = nx.complete_graph(i)  # d-simplex
        graphenUndNamen[f"Hypercube_dim={i}"] = nx.hypercube_graph(i)


graph_ordner_pfad = "./graphAdj/"
dateien = os.listdir(graph_ordner_pfad)          # All files in the path specified above
graphFiles = [f for f in dateien if "asc" in f]  #  filter for only asc datafiles
# filter graphs where the regularity is over 5 because we have no color Matrixes for that 
graphFiles = [f for f in graphFiles if not "6_3.asc" in f and not "7_3.asc" in f]

listGraphs = []
for file in graphFiles:
        listGraphs.extend( file_Extraction.getGraphMatricsFormFile(graph_ordner_pfad  + file) )

num =0
for g in listGraphs:
        num +=1
        for  (name, graph) in graphenUndNamen.items():
                # num ==1 : #
                if num ==1 : # nx.algorithms.isomorphism.GraphMatcher(g, graph).is_isomorphic() :
                        node = list(graph.nodes())[0]
                        if 4 > graph.number_of_nodes() or graph.degree(node ) < 3 :
                                continue
                        print("Name des Graphens: ",name)
                        #print(graph)
                        if "Hypercube_dim" in name :
                                continue
                        print("Nachbarn: ", len( list( graph.neighbors(node ) ) ))
                        print(k_con(graph))

#aut_group = nx.algorithms.isomorphism.GraphMatcher(B, B).is_isomorphic()
