import os
import networkx as nx
import inspect
import file_Extraction
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# CSV-Datei einlesen
df = pd.read_csv('./Results/finalResultsForSymAnalyse.csv') #,usecols=range(1, 7))

#  Regularität, k-zus. Zahl: , Anz. Knoten, Anz. Automorphismen, Anzahl ColMat mit Färb., Anz. Färbungen 
col = 5
max_value = df.iloc[:, col].max()


# Alle Zeilen anzeigen, bei denen Spalte 5 den maximalen Wert hat
result = df[df.iloc[:, col] == max_value]
result2 = df[df.iloc[:, col] == max_value-2]
# Ausgabe der Zeilen mit dem maximalen Wert
df_maxFarbMatr = pd.concat([result, result2], ignore_index=True) #result.append(result2, ignore_index=True)
#print(result)
#print( result2 )
print(df_maxFarbMatr)


print("\n\n num. Färbungen\n\n")
#  Regularität, k-zus. Zahl: , Anz. Knoten, Anz. Automorphismen, Anzahl ColMat mit Färb., Anz. Färbungen 
col = 6
max_value = df.iloc[:, col].max()


# Alle Zeilen anzeigen, bei denen Spalte 3 den maximalen Wert hat
result = df[df.iloc[:, col] == max_value]
for i in range(2,5400):
    result2 = df[df.iloc[:, col] == max_value-i]
    
    if len(result2) > 0:
        #print(i)
        #print( len(result2) )
        break
# Ausgabe der Zeilen mit dem maximalen Wert
df_maxFarbAnzahl = pd.concat([result, result2], ignore_index=True) #result.append(result2, ignore_index=True)
#print(result)
#print( len(result2) )
print(df_maxFarbAnzahl)

col = 6
min_value = df.iloc[:, col].min()


# Alle Zeilen anzeigen, bei denen Spalte 5 den maximalen Wert hat
resultMinFärbungen = df[df.iloc[:, col] == min_value]
print("\n\nminimsle Färbungen\n\n")
print(resultMinFärbungen)

df_maxFarbMatr.to_csv('graphsMaxFarbMat.csv', index=False)
df_maxFarbAnzahl.to_csv('graphsMaxFarben.csv', index=False)
resultMinFärbungen.to_csv('graphsMinFarben.csv', index=False)
