import CSP_Solver
import csvWriter
import k_RegularGraphs_from_file_Extraction
import os

# Path to the directory with the adj. Matritces files of k-regular graphs
ordner_pfad = "./graphAdj"

if __name__ == "__main__":
     # All files in the path specified above
    dateien = os.listdir(ordner_pfad)
    
    #  filter for only asc datafiles 
    graphFiles = [f for f in dateien if "asc" in f]

    print(graphFiles)
