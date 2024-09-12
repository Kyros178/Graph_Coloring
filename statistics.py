import csvWriter
import file_Extraction
import os
import numpy as np
import networkx as nx
from  brutForceSolver import bruteForce
import time
import CSP_Solver
import matplotlib.pyplot as plt

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
            re = bruteForce(g,c_A_M)
            #print("bruteforce result:")
            #print(re)
    end_time = time.time()

    bruteForce_time = end_time - start_time

    start_time = time.time()
    
    for g in graphs:
        for c_A_M in colMats:
            solution = CSP_Solver.solveGraphCSPBadConstraints(g,c_A_M)
            #print(solution)
    end_time = time.time()

    CSPSolverBad_time = end_time - start_time

    start_time = time.time()
    
    for g in graphs:
        for c_A_M in colMats:
            solution = CSP_Solver.solveGraphCSP(g,c_A_M)
            #print(solution)
    end_time = time.time()

    CSPSolverOpt_time = end_time - start_time

    print(f"\
        Time Brute Force: {bruteForce_time}  \n\
        Time CSP Solver badConstraints: {CSPSolverBad_time} \n\
        Time CSP Solver Optimiert: {CSPSolverOpt_time}")

    return (bruteForce_time,CSPSolverBad_time,CSPSolverOpt_time)

            

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


    print("Knoten")
    # Knotenzahl verändern !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    negCount=0
    posCount=0
    runtimes_brut = []
    runtimes_bad = []
    runtimes_opt = []

    #nur bis n = 9 da sonst zu viele lange tests
    #todo wieder auf 9 bringen durch range(5,10) 
    parameter_values =range(5,9)

    numGraphs = [len(graphs[n][4]) for n in parameter_values]

    
    for n in parameter_values:
        #todo richtig implementieren und überprüfen
        #todo zeiten durch anzahl graphen teilen
        # graph mit n Knoten reg= 4 und 3 färbungen
        (bruteForce_time,CSPSolverBad_time,CSPSolverOpt_time) =vergleicher(graphs[n][4], colMat[3][4])
        runtimes_brut.append(bruteForce_time)
        runtimes_bad.append(CSPSolverBad_time)
        runtimes_opt.append(CSPSolverOpt_time)
        
        for g in graphs[n][4]:
            for cAM in colMat[3][4]:
                adjGraph = nx.to_numpy_array(g)
                eigenvaluesGraph = np.round(np.linalg.eigvals(adjGraph) , decimals=8)
                eig =np.round(np.linalg.eigvals(cAM) , decimals=8)
                eigenvaluesColMat = eig # unique wurde hier weggelassen
                if not  np.all(np.isin(eigenvaluesColMat, eigenvaluesGraph)):
                    #print(eigenvaluesColMat)
                    negCount +=1
                else:
                    posCount +=1

    #todo posCount und negCount mit verschieden reg stufen testen da größere reg mehr color
    # Matrizen zulässt!!!!!!!!!!!!!!!!!!!!!!!!!!
    print(f"Es wurden {posCount+ negCount} (Graph, ColMat) Paare gebildet.\
    hiervon konnten { negCount} ignoriert werden und nur {posCount} hätten getestet werden")
    bar_width = 0.25  # Breite der Balken
    index = np.arange(len(parameter_values))  # x-Positionen für die Gruppen

    runtimesPerGraph_brut = [int(a / b) for a, b in zip(runtimes_brut, numGraphs)]  
    runtimesPerGraph_bad  = [int(a / b) for a, b in zip(runtimes_bad, numGraphs)]  
    runtimesPerGraph_opt =  [int(a / b) for a, b in zip(runtimes_opt, numGraphs)]   


    #plot 1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Barplots erstellen
    plt.figure(figsize=(12, 6))
    plt.bar(index, runtimes_brut, bar_width, label='Brute Force', color='skyblue')
    plt.bar(index + bar_width, runtimes_bad, bar_width, label='CSP mit schlechten Constraints', color='lightgreen')
    plt.bar(index + 2 * bar_width, runtimes_opt, bar_width, label='CSP optimiert', color='salmon')
    
    # Achsen und Titel beschriften
    plt.xlabel('Parameter (n)')
    plt.ylabel('Laufzeit (Sekunden)')
    plt.title('Laufzeitvergleich der Solver für alle Graphen mit n Knoten zusammen')
    plt.xticks(index + bar_width, [str(f"Anzahl Knoten: {n}\n Anzahl Graphen: {total}") for n, total in zip(parameter_values, numGraphs) ])
    plt.legend()
    
    # Plot anzeigen
    plt.tight_layout()
    plt.savefig('z_anzKnoten_Gesamt_plot.png')
    plt.show()

    plt.close()
    #plot 2 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    
    # Barplots erstellen
    plt.figure(figsize=(12, 6))
    plt.bar(index, runtimesPerGraph_brut, bar_width, label='Brute Force', color='skyblue')
    plt.bar(index + bar_width, runtimesPerGraph_bad, bar_width, label='CSP mit schlechten Constraints', color='lightgreen')
    plt.bar(index + 2 * bar_width, runtimesPerGraph_opt, bar_width, label='CSP optimiert', color='salmon')
    
    # Achsen und Titel beschriften
    plt.xlabel('Parameter (n)')
    plt.ylabel('Laufzeit (Sekunden)')
    plt.title('Laufzeitvergleich der Solver durchschnitt pro Graph mit n Knoten  ')
    plt.xticks(index + bar_width, [str(n) for n in parameter_values])
    plt.legend()
    
    # Plot anzeigen
    plt.tight_layout()
    plt.savefig('z_anzKnoten_Einzeln_plot.png')
    plt.show()

    

    plt.close()
    

    print("regularität")
    #Regularität verändern !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    runtimes_brut = []
    runtimes_bad = []
    runtimes_opt = []

    #nur bis n = 9 da sonst zu viele lange tests
    #todo wieder auf 9 bringen durch range(5,10) 
    parameter_values =range(3,6)

    numGraphs = [len(graphs[8][r]) for r in parameter_values]

    
    for r in parameter_values:
        #todo richtig implementieren und überprüfen
        #todo zeiten durch anzahl graphen teilen
        # graph mit n Knoten reg= 4 und 3 färbungen
        (bruteForce_time,CSPSolverBad_time,CSPSolverOpt_time) =vergleicher(graphs[8][r], colMat[3][r])
        runtimes_brut.append(bruteForce_time)
        runtimes_bad.append(CSPSolverBad_time)
        runtimes_opt.append(CSPSolverOpt_time)
        
    bar_width = 0.25  # Breite der Balken
    index = np.arange(len(parameter_values))  # x-Positionen für die Gruppen

    runtimesPerGraph_brut = [int(a / b) for a, b in zip(runtimes_brut, numGraphs)]  
    runtimesPerGraph_bad  = [int(a / b) for a, b in zip(runtimes_bad, numGraphs)]  
    runtimesPerGraph_opt =  [int(a / b) for a, b in zip(runtimes_opt, numGraphs)]   


    #plot 1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Barplots erstellen
    plt.figure(figsize=(12, 6))
    plt.bar(index, runtimes_brut, bar_width, label='Brute Force', color='skyblue')
    plt.bar(index + bar_width, runtimes_bad, bar_width, label='CSP mit schlechten Constraints', color='lightgreen')
    plt.bar(index + 2 * bar_width, runtimes_opt, bar_width, label='CSP optimiert', color='salmon')
    
    # Achsen und Titel beschriften
    plt.xlabel('Parameter (r)')
    plt.ylabel('Laufzeit (Sekunden)')
    plt.title('Laufzeitvergleich der Solver für alle Graphen mit regularität r zusammen')
    plt.xticks(index + bar_width, [str(f"regularität: {r}\n Anzahl Graphen: {total}") for r, total in zip(parameter_values, numGraphs) ])
    plt.legend()
    
    # Plot anzeigen
    plt.tight_layout()
    plt.savefig('z_reg_Gesamt_plot.png')
    plt.show()

    plt.close()
    #plot 2 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    
    # Barplots erstellen
    plt.figure(figsize=(12, 6))
    plt.bar(index, runtimesPerGraph_brut, bar_width, label='Brute Force', color='skyblue')
    plt.bar(index + bar_width, runtimesPerGraph_bad, bar_width, label='CSP mit schlechten Constraints', color='lightgreen')
    plt.bar(index + 2 * bar_width, runtimesPerGraph_opt, bar_width, label='CSP optimiert', color='salmon')
    
    # Achsen und Titel beschriften
    plt.xlabel('Parameter (r)')
    plt.ylabel('Laufzeit (Sekunden)')
    plt.title('Laufzeitvergleich der Solver durchschnitt pro Graph mit regularität r  ')
    plt.xticks(index + bar_width, [str(r) for r in parameter_values])
    plt.legend()
    
    # Plot anzeigen
    plt.tight_layout()
    plt.savefig('z_reg_Einzeln_plot.png')
    plt.show()




    
    plt.close()

    print("Färbungen")
    #Farbzahl verändern verändern !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    runtimes_brut = []
    runtimes_bad = []
    runtimes_opt = []

    #nur bis n = 9 da sonst zu viele lange tests
    #todo wieder auf 9 bringen durch range(5,10) 
    parameter_values =range(2,5)

    numGraphs = [len(graphs[8][4]) for f in parameter_values]

    
    for f in parameter_values:
        #todo richtig implementieren und überprüfen
        #todo zeiten durch anzahl graphen teilen
        # graph mit n Knoten reg= 4 und 3 färbungen
        (bruteForce_time,CSPSolverBad_time,CSPSolverOpt_time) =vergleicher(graphs[8][4], colMat[f][4])
        runtimes_brut.append(bruteForce_time)
        runtimes_bad.append(CSPSolverBad_time)
        runtimes_opt.append(CSPSolverOpt_time)
        
    bar_width = 0.25  # Breite der Balken
    index = np.arange(len(parameter_values))  # x-Positionen für die Gruppen

    runtimesPerGraph_brut = [int(a / b) for a, b in zip(runtimes_brut, numGraphs)]  
    runtimesPerGraph_bad  = [int(a / b) for a, b in zip(runtimes_bad, numGraphs)]  
    runtimesPerGraph_opt =  [int(a / b) for a, b in zip(runtimes_opt, numGraphs)]   


    #plot 1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Barplots erstellen
    plt.figure(figsize=(12, 6))
    plt.bar(index, runtimes_brut, bar_width, label='Brute Force', color='skyblue')
    plt.bar(index + bar_width, runtimes_bad, bar_width, label='CSP mit schlechten Constraints', color='lightgreen')
    plt.bar(index + 2 * bar_width, runtimes_opt, bar_width, label='CSP optimiert', color='salmon')
    
    # Achsen und Titel beschriften
    plt.xlabel('Parameter (f)')
    plt.ylabel('Laufzeit (Sekunden)')
    plt.title('Laufzeitvergleich der Solver für alle Graphen mit f Farben')
    plt.xticks(index + bar_width, [str(f"anz. Farben: {f}\n Anzahl Graphen: {total}") for f, total in zip(parameter_values, numGraphs) ])
    plt.legend()
    
    # Plot anzeigen
    plt.tight_layout()
    plt.savefig('z_anzFarben_Gesamt_plot.png')
    plt.show()

    plt.close()
    #plot 2 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    
    # Barplots erstellen
    plt.figure(figsize=(12, 6))
    plt.bar(index, runtimesPerGraph_brut, bar_width, label='Brute Force', color='skyblue')
    plt.bar(index + bar_width, runtimesPerGraph_bad, bar_width, label='CSP mit schlechten Constraints', color='lightgreen')
    plt.bar(index + 2 * bar_width, runtimesPerGraph_opt, bar_width, label='CSP optimiert', color='salmon')
    
    # Achsen und Titel beschriften
    plt.xlabel('Parameter (f)')
    plt.ylabel('Laufzeit (Sekunden)')
    plt.title('Laufzeitvergleich der Solver durchschnitt pro Graph mit f Farben ')
    plt.xticks(index + bar_width, [str(f) for f in parameter_values])
    plt.legend()
    
    # Plot anzeigen
    plt.tight_layout()
    plt.savefig('z_anzFarben_Einzeln_plot.png')
    plt.show()



