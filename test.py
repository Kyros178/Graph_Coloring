import os
import networkx as nx
import inspect
import file_Extraction
import pandas as pd

# CSV-Datei einlesen
df = pd.read_csv('symAnalyse.csv')

#Pearson-Korrelationskoeffizienten
# Korrelation zwischen den Spalten berechnen
correlation_matrix = df.corr()


# Kendall oder Spearman, indem du den Parameter method angibst:
#correlation_matrix = df.corr(method='spearman')

# Korrelationen anzeigen
print(correlation_matrix)
