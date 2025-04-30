import tkinter as tk
from tkinter import ttk, messagebox

class SmartCampusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Campus Navigator & Task Scheduler")
        self.root.geometry("1000x600")

        self.task_list = []

        title_label = ttk.Label(root, text="CSUF Campus Navigator",font=("Arial", 16, "bold"), foreground="darkblue", anchor="center")
        title_label.pack(pady=(15, 10))
        

        
        #Shortest Path Algorithm: Implement Dijkstra’s algorithm to find the shortest path 
        #between two buildings. Refer to dijkstra algorithm.py.
        
        shortest_path = tk.LabelFrame(root, text="Campus Navigation", fg="blue",font=("Arial", 12, "bold"))
        shortest_path.pack(fill="x", padx=10, pady=5,)

        spacing = ttk.LabelFrame(root)
        spacing.pack(fill="x", padx=10, pady=(0, 15))  

        self.start_building = tk.StringVar()
        self.end_building = tk.StringVar()
        buildings = ["Titan Hall" , "Langsdorf Hall", "McCarthy Hall", "Pollak Library", "Computer Science", "Nutwood Parking Structure"]  #will update more based on mapping

        ttk.Label(shortest_path, text="Start:").pack(side="left", padx=5)
        ttk.Combobox(shortest_path, textvariable=self.start_building, values=buildings, width=20).pack(side="left")
        ttk.Label(shortest_path, text="End:").pack(side="left", padx=5)
        ttk.Combobox(shortest_path, textvariable=self.end_building, values=buildings, width=20).pack(side="left")

        ttk.Button(shortest_path, text="Find Shortest Path", command=self.find_path).pack(side="left", padx=10)

        #Minimum Spanning Tree (MST): Use Prim’s or Kruskal’s algorithm to deter-
        #mine optimal maintenance routes covering all buildings. See prim algorithm.py and
        #kruskal algorithm.py.
        
        mst_route = tk.LabelFrame(root, text="Maintenance Routes",fg="blue",font=("Arial", 12, "bold"))
        mst_route.pack(fill="x", padx=10, pady=5)
        ttk.Button(mst_route, text="Display optimal maintenance route", command=self.show_mst).pack(padx=10, pady=5)

        spacing = ttk.LabelFrame(root)
        spacing.pack(fill="x", padx=10, pady=(0, 15))

        #String Matching: Implement KMP or Boyer-Moore algorithms to search for building
        #names or room numbers. See kmp algorithm.py and boyer moore.py.

        search_building = tk.LabelFrame(root, text="Building Search",fg="blue",font=("Arial", 12, "bold"))
        search_building.pack(fill="x", padx=10, pady=5)
        self.search_entry = ttk.Entry(search_building,width=50)
        self.search_entry.pack(side="left", padx=5)
        ttk.Button(search_building, text="Search", command=self.search_building).pack(side="left", padx=5)

        spacing = ttk.LabelFrame(root)
        spacing.pack(fill="x", padx=10, pady=(0, 15))

        #Task Scheduling: Apply the Activity Selection Problem (greedy approach) to sched-
        #ule tasks without overlaps. Refer to activity selection.py

        task_schedule = tk.LabelFrame(root, text="Task Scheduling",fg="blue",font=("Arial", 12, "bold"))
        task_schedule.pack(fill="x", padx=10, pady=5)

        ttk.Label(task_schedule, text="Task name:").pack(side="left", padx=5)
        self.task_name = ttk.Entry(task_schedule, width=15)
        self.task_name.pack(side="left")

        ttk.Label(task_schedule, text="Start time:").pack(side="left", padx=5)
        self.task_start = ttk.Entry(task_schedule, width=8)
        self.task_start.pack(side="left")

        ttk.Label(task_schedule, text="End time:").pack(side="left", padx=5)
        self.task_end = ttk.Entry(task_schedule, width=8)
        self.task_end.pack(side="left")

        ttk.Button(task_schedule, text="Add Task", command=self.add_task).pack(side="left", padx=5)
        ttk.Button(task_schedule, text="Optimize Schedule", command=self.optimize_tasks).pack(side="left", padx=5)

        spacing = ttk.LabelFrame(root)
        spacing.pack(fill="x", padx=10, pady=(0, 15))

        #Sorting: Use Merge Sort or Quick Sort to organize tasks by priority or time. Refer
        #to merge sort.py and quick sort.py.

        sort_tasks = tk.LabelFrame(root, text="Sort Tasks",fg="blue",font=("Arial", 12, "bold"))
        sort_tasks.pack(fill="x", padx=10, pady=5)
        self.sort_option = tk.StringVar()
        ttk.Label(sort_tasks, text="Sort tasks by: ").pack(side="left")
        ttk.Combobox(sort_tasks, textvariable=self.sort_option, values=["Time", "Priority"], width=15).pack(side="left", padx=5)
        ttk.Button(sort_tasks, text="Sort", command=self.sort_tasks).pack(side="left", padx=5)

        #Campus Map Display
        ttk.Button(root, text="Display Campus Map", command=self.show_map).pack(pady=5)


        #Output Screen
        output_frame = ttk.LabelFrame(root, text="Outputs: ")
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.result_box = tk.Text(output_frame, wrap="word")
        self.result_box.pack(fill="both", expand=True)


    #Input algorithms and functions here...
    def find_path(self):
        start = self.start_building.get()
        end = self.end_building.get()
        self.result_box.insert(tk.END, f"Path from {start} to {end}\n")

    def show_mst(self):
        self.result_box.insert(tk.END, "Displaying optimal maintenance route...\n")

    def search_building(self):
        query = self.search_entry.get()
        self.result_box.insert(tk.END, f"Looking for: {query}\n")

    def add_task(self):
        name = self.task_name.get()
        start = self.task_start.get()
        end = self.task_end.get()
        self.task_list.append((name, start, end))
        self.result_box.insert(tk.END, f"Task Added. {name} ({start}-{end})\n")

    def optimize_tasks(self):
        self.result_box.insert(tk.END, f"Optimizing {len(self.task_list)} tasks...\n")

    def sort_tasks(self):
        criteria = self.sort_option.get()
        self.result_box.insert(tk.END, f"Sorting tasks by {criteria}\n")

    def show_map(self):
        self.result_box.insert(tk.END, "Displaying campus graph...\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartCampusGUI(root)
    root.mainloop()
