import reporting as rt


import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import messagebox

root = tk.Tk()  # Creaza fereastra principala
root.title('Task Management')
root.geometry('800x800')

prio = ['High', 'Medium', 'Low']
states = ['In progres', 'Completed', 'Blocked']


def addTask():
    state = comboState.get()
    name = entryTaskName.get()
    prior = comboPrior.get()
    deadline = calTask.get_date()
    description = entryDescTask.get()
    
    if not name or not prior:
        messagebox.showerror("Error","Nume sau prioritate nedefinita!")
        return 
    
    if not checkTask(name,state,prio):
        return
    if not state :
        state = 'In progres'
    if not description :
        description = ' '
        
    new_task = {
        "nume" : name,
        "descr" : description,
        "prioritate" : prior,
        "deadline" : deadline,
        "stare" : state
    }
    try:
        rt.saveCSV(new_task)
        messagebox.showinfo('Succes','Taskul adaugat in fisierul CSV!')
        entryTaskName.delete(0, tk.END)
        entryDescTask.delete(0, tk.END)
        comboPrior.set('')
        comboState.set('')
    except:
        messagebox.showerror('Error!', 'Cannot Add Task')
        
def checkTask(nume, stare, prioritate):
    df = rt.loadCSV()
    
    # Verificăm dacă DataFrame-ul este gol
    if df.empty:
        return True  # Dacă DataFrame-ul este gol, putem adăuga task-ul fără probleme
    
    # Iterăm prin fiecare rând din DataFrame pentru a verifica dacă există un task similar
    for index, row in df.iterrows():
        if row['nume'] == nume and row['stare'] == stare and row['prioritate'] == prioritate:
            messagebox.showerror("Error", "Task-ul deja există!")
            return False
    
    return True

# Delete    

def delTask():
    # Load la CSV
    tasks = rt.loadCSV()

    # Selected listbox value
    try:
        # luam valoarea din lista
        taskIndex = listbox.curselection()[0]
    except:
        messagebox.showerror('Error','Selecteaza un task')
        return
    try: 
        # Delete task
        tasks = tasks.drop(index=taskIndex)
        #Reset index
        tasks = tasks.reset_index(drop = True)
        # Save
        rt.saveDataframeCSV(tasks)
        # delete lisbox
        listbox.delete(taskIndex)
        messagebox.showinfo('Succes!','Task sters!')
    except Exception as e:
        messagebox.showerror('Error', f'No task deleted {e}')
    
     

def editTask():
    # Load la CSV
    tasks = rt.loadCSV()
    
    # Luam valorile din entry 
    state = comboState.get()
    name = entryTaskName.get()
    prior = comboPrior.get()
    deadline = calTask.get_date()
    description = entryDescTask.get()
    
    # Luam index din lista 
    try:
        # luam valoarea din lista
        taskIndex = listbox.curselection()[0]
    except:
        messagebox.showerror('Error','Selecteaza un task')
        return
    
    if state: 
        tasks.at[taskIndex,'stare'] = state
        
        
    if name:
        tasks.at[taskIndex,'nume']= name
        
    if prior:
        tasks.at[taskIndex,'prioritate']= prior
        
    if deadline:
        tasks.at[taskIndex,'deadline']= deadline
    if description:
        tasks.at[taskIndex,'descr']= description
    try:
        tasks = tasks.reset_index(drop = True)
        rt.saveDataframeCSV(tasks)
        
        # reincarcam listbox
        showTasks()
        messagebox.showinfo('Succes', 'Task editat cu succes!')
        
        # Resetare campuri de entry
        entryTaskName.delete(0, tk.END)
        entryDescTask.delete(0, tk.END)
        comboPrior.set('')
        comboState.set('')
    except Exception as e:
        messagebox.showerror('Error', f'Nu se poate edita: {e}')
    
def showTasks():
    listbox.delete(0,tk.END)
    tasks = rt.loadCSV()
    # trebuie sa luam fiecare rand din dataframe
    for index, row in tasks.iterrows():
        task_info = f"{row['nume']} | {row['descr']} | {row['prioritate']} | {row['deadline']} | {row['stare']}"
        listbox.insert(tk.END, task_info)

# Adauga Task
labelAddTask = tk.Label(root, text='Adauga task')
labelAddTask.grid(row=0, column=0, padx=10, pady=10, sticky="e")

entryTaskName = tk.Entry(root, width=30)
entryTaskName.grid(row=0, column=1, pady=0, padx=20, sticky="w")

entryDescTask = tk.Entry(root, width=30)
entryDescTask.grid(row=0, column=2, pady=0, padx=20, sticky="w")

comboPrior = ttk.Combobox(root, values=prio)
comboPrior.grid(row=1, column=1, pady=0, padx=20, sticky="w")

calTask = Calendar(root, selectmode='day')
calTask.grid(row=2, column=1, columnspan = 2, rowspan=3, padx=10, pady=10, sticky="n")

comboState = ttk.Combobox(root, values=states)
comboState.grid(row=1, column=2, pady=0, padx=20, sticky="w")

buttonAddTask = tk.Button(root, text='ADD', command=addTask)
buttonAddTask.grid(row=1, column=0, padx=20, pady=0, sticky="n")

# Editeaza Task
labelEditTask = tk.Label(root, text='Editeaza task->')
labelEditTask.grid(row=5, column=0, pady=10, padx=20, sticky="e")

buttonEditTask = tk.Button(root, text='EDIT', command=editTask)
buttonEditTask.grid(row=5, column=1, padx=0, pady=0, sticky="w")

# Sterge Task
labelDelTask = tk.Label(root, text='Sterge task->')
labelDelTask.grid(row=6, column=0, pady=10, padx=20, sticky="e")

buttonDelTask = tk.Button(root, text='Sterge', command = delTask)
buttonDelTask.grid(row=6, column=1, padx=0, pady=0, sticky="w")

# Lista de Task-uri

buttonShowTasks =tk.Button(root, command=showTasks,text='Lista de Taskuri')
buttonShowTasks.grid(row=10 , column=4, padx=0, pady=0, sticky="w")

listbox = tk.Listbox(root, width=80, height=10)
listbox.grid(row=10, column=0, columnspan=3, pady=20, padx=20, sticky="n")


# Filter 

root.mainloop()

