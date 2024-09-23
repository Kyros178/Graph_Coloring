import csv
import numpy as np  
import json
import os


def saveColorings(filename,graphName,graphAdj,colorAdj,array_of_dictColorings):
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
    
            # Überschriften der Spalten (optional)
            writer.writerow(['Graph name','Graph adj. Mat.', 'colour incidence matrix ', 'Dictionary of colorings'])
            
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([graphName, graphAdj,colorAdj,coloringsToString( array_of_dictColorings ) ])


def saveGraphAndColoring(filename,graphName,info,numPosColInzMat, numColorings,graphAdj,colorAdjList):
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
    
            # Überschriften der Spalten (optional)
            writer.writerow(['Graph name','Graph adj. Mat.', " Regularität: ", " k-zusammenhangs Zahl: "," Anzahl Knoten: "," Anzahl Automorphismen: ", " Anzahl ColMat m. Färb.: "," Anzahl Färbungen: ", 'List of possible colour incidence matrix in this and the following columns '])
            
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        json_serializable_list = [arr.tolist() for arr in colorAdjList]
        writer.writerow([graphName, graphAdj,info["Reg"], info["k-zusmZahl"] , info["numNodes"], info["autGrupSize"],numPosColInzMat, numColorings]  +  colorAdjList  )  #json.dumps(json_serializable_list ))

        

def saveSymInfo(filename,info,numPosColInzMat, numColorings):
    head = ["Name", " Regularität", " k-zus. Zahl: "," Anz. Knoten"," Anz. Automorphismen", " Anzahl ColMat mit Färb."," Anz. Färbungen"]
      
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
    
            # Überschriften der Spalten (optional)
            writer.writerow(head)
            
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        ''' falls ich eine liste brauche
        list =[]
        list.append(info["Name"])
        list.append( info["Reg"])
        list.append(info["k-zusmZahl"] )
        list.append(info["numNodes"])
        list.append(info["autGrupSize"])
        list.append(numPosColInzMat)
        list.append(numColorings)
        '''
        writer.writerow( [info["Name"], info["Reg"], info["k-zusmZahl"] , info["numNodes"], info["autGrupSize"],numPosColInzMat, numColorings] )

        
    
def coloringsToString(listOfColorings):
    result = []
    for col in listOfColorings:
        result.append(json.dumps(col))
    return result



if __name__ == "__main__":
    arr1 =  np.zeros((3,3)) 
    arr2 =  np.zeros((4,4))  
    thisdict = {
        1: 2,
        2: 2,
        3: 1,
        4: 2
    }


    # Innerhalb der Schleife:
    #dict_str = json.dumps(thisdict)
    dict_str = coloringsToString([thisdict,thisdict])
    # Dateiname der CSV-Datei
    csvFile = 'output.csv'

    saveColorings(csvFile,arr1,arr2,dict_str)



'''


# An die bestehende CSV-Datei anhängen
#with open(filename, mode='a', newline='') as file:

# CSV-Datei schreiben
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Überschriften der Spalten (optional)
    writer.writerow(['Array1', 'Array2', 'Dictionary'])

    # Daten in die CSV schreiben
    writer.writerow([arr1, arr2, [dict_str,dict_str,dict_str]])
    writer.writerow([arr1, arr2, dict_str])

'''
