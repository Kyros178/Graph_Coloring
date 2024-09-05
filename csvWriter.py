import csv
import numpy as np  
import json
import os


def saveColorings(filename,graphAdj,colorAdj,array_of_dictColorings):
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
    
            # Überschriften der Spalten (optional)
            writer.writerow(['Graph adj. Mat.', 'Color adj. Mat.', 'Dictionary of colorings'])
            
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([graphAdj,colorAdj,coloringsToString( array_of_dictColorings ) ])


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
