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
dfAll = pd.read_csv('finalResultsForSymAnalyse.csv',usecols=range(1, 7))

dfNameGraphs = pd.read_csv('symAnalyse.csv',usecols=range(1, 7))

#df = pd.read_csv("resultsOverview.csv", usecols=range(2, 8))

#print(df.iloc[0])

#print(df.dtypes)

#Pearson-Korrelationskoeffizienten
# Korrelation zwischen den Spalten berechnen
correlation_matrixAll = dfAll.corr()
correlation_matrixNameGraphs = dfNameGraphs.corr()

# Kendall oder Spearman, indem du den Parameter method angibst:
correlation_matrix_Sp_All = dfAll.corr(method='spearman') #'kendall')
correlation_matrix_SP_NameGraphs = dfNameGraphs.corr(method='spearman')


corrAllRound = correlation_matrixAll.round(3)
corrNamRound = correlation_matrixNameGraphs.round(3)

corrAllSpRound =correlation_matrix_Sp_All.round(3)
corrNamSpRound = correlation_matrix_SP_NameGraphs.round(3)


corrAllRound.to_csv('correlation_matrixAll.csv', index=True)
corrNamRound.to_csv('correlation_matrixNameGraphs.csv', index=True)
corrAllSpRound.to_csv('spearman_correlation_matrixAll.csv', index=True)
corrNamSpRound.to_csv('spearman_correlation_matrixNameGraphs.csv', index=True)



'''
# Unabhängige Variable ist die erste Spalte (Index 0), abhängige Variable ist die zweite Spalte (Index 1)
X = df.iloc[:, [0,1,2,3]]  # Unabhängige Variable (erste Spalte)
y = df.iloc[:, 4]    # Abhängige Variable (4 Spalte)

# In Trainings- und Testdaten aufteilen
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Lineare Regression initialisieren und trainieren
model = LinearRegression()
model.fit(X_train, y_train)

# Vorhersagen auf den Testdaten machen
y_pred = model.predict(X_test)

# Ergebnisse anzeigen
print("Koeffizienten:", model.coef_)
print("Intercept:", model.intercept_)
print("Mean Squared Error (MSE):", mean_squared_error(y_test, y_pred))
print("R² (Bestimmtheitsmaß):", r2_score(y_test, y_pred))

# Visualisierung der Regressionsgeraden
plt.scatter(X_test, y_test, color='blue', label='Daten')
plt.plot(X_test, y_pred, color='red', label='Vorhersage')
plt.xlabel('X')
plt.ylabel('y')
plt.title('Lineare Regression')
plt.legend()
plt.show()
'''
