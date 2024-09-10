
import networkx as nx
import inspect

# Alle Graphen-Generierungsfunktionen aus dem Modul networkx.generators holen
generators = inspect.getmembers(nx.generators, inspect.isfunction)

# Liste aller Generierungsfunktionen ausgeben und sie aufrufen
for name, func in generators:
        
        #continue
        
        if "random" in name:
                #print("random")
                continue
        if "shift_list" in str(inspect.signature(func)):
                #print("shift_list" )
                continue
        if "repeats" in str(inspect.signature(func)):
                #print("repeats")
                continue
        if "tau1" in str(inspect.signature(func)):
                #print("tau1")
                continue
        
        if "h," in str(inspect.signature(func)):
                #print("h,")
                continue
        if "p," in str(inspect.signature(func)):
                #print("p,")
                continue
        if "offsets" in str(inspect.signature(func)):
                #print("offsets")
                continue
        if "G," in str(inspect.signature(func)):
                #print("G,")
                continue
        if "r," in str(inspect.signature(func)):
                #print("r,")
                continue
        if "theta," in str(inspect.signature(func)):
                print("theta,")
                continue
        if "k," in str(inspect.signature(func)):
                #print("k,")
                continue
        if "d," in str(inspect.signature(func)):
                #print("d,")
                continue
        
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        signature = inspect.signature(func)  # Signatur der Funktion holen
        print(f"{name}{signature}")
                
        continue
        # Argumente, die wir für einige Generatoren verwenden könne
        args = {}
        
        # Überprüfen der Signatur und festlegen von Beispielwerten
        for param in signature.parameters.values():
                if param.default is param.empty:
                        # Wenn kein Standardwert vorhanden ist, setzen wir einen Beispielwert
                        if param.name == "n":  # Anzahl der Knoten
                                args[param.name] = 5  # Beispielwert
                        elif param.name == "m":  # Anzahl der Kanten
                                args[param.name] = 4  # Beispielwert
                                # Fügen Sie hier zusätzliche Argumente hinzu, wenn erforderlich

                                # Generierungsfunktion mit den festgelegten Argumenten aufrufen
        if args:
                graph = func(**args)  # Aufruf der Funktion mit den Argumenten
                print(f"Generated graph {name} with {args}: {graph.edges()}")
