import networkx as nx
import inspect

# Alle Graphen-Generierungsfunktionen aus dem Modul networkx.generators holen
generators = inspect.getmembers(nx.generators, inspect.isfunction)

# Liste aller Generierungsfunktionen ausgeben
for name, func in generators:
	if not "random" in name:
		signature = inspect.signature(func)  # Signatur der Funktion holen
		print(f"{name}{signature}")
