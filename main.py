import CSP_Solver
import csvWriter
import file_Extraction
import os

# Path to the directory with the adj. Matritces files of k-regular graphs
graph_ordner_pfad = "./graphAdj"
colorAdj_ordner_pfad = "./colorAdj"

if __name__ == "__main__":
     # All files in the path specified above
    dateien = os.listdir(graph_ordner_pfad)
    
    #  filter for only asc datafiles 
    graphFiles = [f for f in dateien if "asc" in f]

    dateien = os.listdir(colorAdj_ordner_pfad)
    colorAdjFiles = [f for f in dateien if "sage" in f]
   
    
    file_Extraction.getColorAdjMatFromFile("colorAdj/2col-list.sage")
   
