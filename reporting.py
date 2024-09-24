import pandas as pd 
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
fileJSON = os.path.join(current_dir, 'Tasks.json')
fileCSV = os.path.join(current_dir, 'Tasks.csv')

import pandas as pd

def loadCSV():
    try:
        # Load CSV-ul existent
        df = pd.read_csv(fileCSV)
        
        # Verificăm daca fisierul este gol (fara coloane)
        if df.empty or df.shape[1] == 0:  # Verificam daca nu sunt coloane
            df = pd.DataFrame(columns=["nume", "descr", "prioritate", "deadline", "stare"])
            
    except FileNotFoundError:
        # Daca fisierul nu există, initializam DataFrame-ul cu coloanele necesare
        df = pd.DataFrame(columns=["nume", "descr", "prioritate", "deadline", "stare"])
    
    df = df.reset_index(drop = True)
    return df


def saveCSV(task):
    df = loadCSV()
    
    # Transform task-ul într-un DataFrame
    new_task = pd.DataFrame([task])
    
    # Folosim pd.concat pentru a adauga task-ul nou la DataFrame-ul existent
    df = pd.concat([df, new_task], ignore_index=True)
    
    # Save DataFrame-ul actualizat in CSV
    df.to_csv(fileCSV, index=False)
    
def saveDataframeCSV(tasks):
    tasks.to_csv(fileCSV, index=False)
