import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

from dijkstra_algorithm import dijkstra, reconstruct_path
from activity_selection import select_activities
from kmp_algorithm import kmp_search
from mst_algo import compute_mst 

from networkx_utils import build_graph, draw_graph
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from networkx_utils import build_graph, draw_graph, draw_mst
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def convert_to_24_hour(hour, minute, ampm):
        hour = int(hour)
        minute = int(minute)
        if ampm == "PM" and hour != 12:
            hour += 12
        if ampm == "AM" and hour == 12:
            hour = 0
        return hour + minute / 60

class SmartCampusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Campus Navigator & Task Scheduler")
        self.root.geometry("1215x700")
        self.tasks = []

       
        try:
         logo = tk.PhotoImage(file="school_logo.png")
         logo = logo.subsample(8, 8)  
        except Exception as e:
         logo = None
         print(f"Error loading logo: {e}")


        title_frame = ttk.Frame(root)
        title_frame.pack(pady=(15, 10))

        if logo:
         logo_label = ttk.Label(title_frame, image=logo)
         logo_label.image = logo  
         logo_label.pack(side="left", padx=10)

        title_label = ttk.Label(title_frame, text="CSUF Campus Navigator", font=("Arial", 25, "bold"), foreground="orange")
        title_label.pack(side="left")

    

        
        self.graph = build_graph()
                
        #Shortest Path Algorithm: Implement Dijkstra’s algorithm to find the shortest path 
        #between two buildings. Refer to dijkstra algorithm.py.
        
        shortest_path = tk.LabelFrame(root, text="Campus Navigation", fg="blue",font=("Arial", 12, "bold"))
        shortest_path.pack(fill="x", padx=10, pady=5,)

        spacing = ttk.LabelFrame(root)
        spacing.pack(fill="x", padx=10, pady=(0, 15))  

        self.start_building = tk.StringVar()
        self.end_building = tk.StringVar()
        buildings = list(self.graph.nodes())  #will update more based on mapping

        ttk.Label(shortest_path, text="Start:").pack(side="left", padx=5)
        ttk.Combobox(shortest_path, textvariable=self.start_building, values=buildings, width=20).pack(side="left")
        ttk.Label(shortest_path, text="End:").pack(side="left", padx=5)
        ttk.Combobox(shortest_path, textvariable=self.end_building, values=buildings, width=20).pack(side="left")

        ttk.Button(shortest_path, text="Find Shortest Path", command=self.find_path).pack(side="left", padx=10)
        
        mst_route = tk.LabelFrame(root, text="Maintenance Routes",fg="blue",font=("Arial", 12, "bold"))
        mst_route.pack(fill="x", padx=10, pady=5)
        ttk.Button(mst_route, text="Display optimal maintenance route", command=self.show_mst).pack(padx=10, pady=5)

        spacing = ttk.LabelFrame(root)
        spacing.pack(fill="x", padx=10, pady=(0, 15))

        search_building = tk.LabelFrame(root, text="Building Search",fg="blue",font=("Arial", 12, "bold"))
        search_building.pack(fill="x", padx=10, pady=5)
        self.search_entry = ttk.Entry(search_building,width=50)
        self.search_entry.pack(side="left", padx=5)
        ttk.Button(search_building, text="Search", command=self.search_building).pack(side="left", padx=5)

        spacing = ttk.LabelFrame(root)
        spacing.pack(fill="x", padx=10, pady=(0, 15))

        task_schedule = tk.LabelFrame(root, text="Task Scheduling", fg="blue", font=("Arial", 12, "bold"))
        task_schedule.pack(fill="x", padx=10, pady=5)

        ttk.Label(task_schedule, text="Task name:").pack(side="left", padx=5)
        self.task_name = ttk.Entry(task_schedule, width=15)
        self.task_name.pack(side="left")

        ttk.Label(task_schedule, text="Start time:").pack(side="left", padx=5)
        self.start_hour = ttk.Combobox(task_schedule, width=5, values=[str(i) for i in range(1, 13)])
        self.start_hour.pack(side="left")
        self.start_minute = ttk.Combobox(task_schedule, width=5, values=[f"{i:02}" for i in range(0, 60, 5)])
        self.start_minute.pack(side="left")
        self.start_ampm = ttk.Combobox(task_schedule, width=5, values=["AM", "PM"])
        self.start_ampm.pack(side="left")

        ttk.Label(task_schedule, text="End time:").pack(side="left", padx=5)
        self.end_hour = ttk.Combobox(task_schedule, width=5, values=[str(i) for i in range(1, 13)])
        self.end_hour.pack(side="left")
        self.end_minute = ttk.Combobox(task_schedule, width=5, values=[f"{i:02}" for i in range(0, 60, 5)])
        self.end_minute.pack(side="left")
        self.end_ampm = ttk.Combobox(task_schedule, width=5, values=["AM", "PM"])
        self.end_ampm.pack(side="left")

        ttk.Label(task_schedule, text="Priority (1-5):").pack(side="left", padx=5)
        self.task_priority = ttk.Entry(task_schedule, width=5)
        self.task_priority.pack(side="left")

        ttk.Button(task_schedule, text="Add Task", command=self.add_task).pack(side="left", padx=5)
        ttk.Button(task_schedule, text="Optimize Schedule", command=self.optimize_tasks).pack(side="left", padx=5)

        spacing = ttk.LabelFrame(root)
        spacing.pack(fill="x", padx=10, pady=(0, 15))

        sort_tasks = tk.LabelFrame(root, text="Sort Tasks", fg="blue", font=("Arial", 12, "bold"))
        sort_tasks.pack(fill="x", padx=10, pady=5)
        self.sort_option = tk.StringVar()
        ttk.Label(sort_tasks, text="Sort tasks by: ").pack(side="left")
        ttk.Combobox(sort_tasks, textvariable=self.sort_option, values=["Start Time", "End Time", "Priority"], width=15).pack(side="left", padx=5)
        ttk.Button(sort_tasks, text="Sort", command=self.sort_tasks).pack(side="left", padx=5)

        tk.Button(root, text="Display Campus Map",fg="blue", font=("Arial", 12, "bold"), command=self.show_map).pack(pady=5)


        #Output Screen
        output_frame = tk.LabelFrame(root, text="Outputs: ", fg="blue", font=("Arial", 12, "bold"))
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)


        self.result_box = ScrolledText(
         output_frame,
         wrap="word",
         font=("Courier New", 10),
         bg="#ffffff",
         fg="#000000",
         insertbackground="black"  
)
        self.result_box.pack(fill="both", expand=True, padx=5, pady=5)
        self.result_box.insert(tk.END, "Results will appear here...\n")

    def find_path(self):
        start = self.start_building.get()
        end = self.end_building.get()

        adj = {
        node: [(nbr, data['weight']) 
               for nbr, data in self.graph[node].items()]
        for node in self.graph.nodes()
    }

        distances, previous = dijkstra(adj, start)
        path = reconstruct_path(previous, start, end)
        self.last_path = path
        cost = distances[end]

        if path:
            self.result_box.insert(tk.END, f"Shortest path from {start} to {end}:\n{' -> '.join(path)}\nCost: {cost} meter(s)\n\n")
        else:
            self.result_box.insert(tk.END, f"No path found from {start} to {end}.\n\n")


    def show_mst(self):
     try:
        mst = compute_mst(self.graph)
        mst_edges = list(mst.edges())

        win = tk.Toplevel(self.root)
        win.title("Optimal Maintenance Route (MST)")
        win.geometry("600x500")

        fig = draw_mst(self.graph, mst_edges)
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        self.result_box.insert(tk.END, "Optimal maintenance route (MST) displayed.\n\n")
     except Exception as e:
        messagebox.showerror("Error", f"Failed to compute MST: {e}")


    def search_building(self):
        query = self.search_entry.get()
        buildings = list(self.graph.nodes())
    
        matches = [b for b in buildings if kmp_search(b, query)]
        if matches:
            self.result_box.insert(tk.END, f"Search results for '{query}':\n")
            for match in matches:
                self.result_box.insert(tk.END, f"- {match}\n")
        else:
            self.result_box.insert(tk.END, f"No buildings found matching '{query}'.\n")
        self.result_box.insert(tk.END, "\n")


    def add_task(self):
        name = self.task_name.get().strip()


        if any(task['name'].lower() == name.lower() for task in self.tasks):
            messagebox.showerror("Duplicate Task", f"A task named '{name}' already exists.")
            return


        try:
            start = convert_to_24_hour(self.start_hour.get(), self.start_minute.get(), self.start_ampm.get())
            end = convert_to_24_hour(self.end_hour.get(), self.end_minute.get(), self.end_ampm.get())


            if start >= end:
                raise ValueError("Start time must be before end time.")


        except Exception as e:
            messagebox.showerror("Invalid Time", f"Error in time input: {e}")
            return


        try:
            priority = int(self.task_priority.get())
            if not (1 <= priority <= 5):
                raise ValueError("Priority must be between 1 (highest) and 5 (lowest).")
       
        except Exception as e:
            messagebox.showerror("Invalid Priority", f"{e}")
            return


        self.tasks.append({"name": name, "start": start, "end": end, "priority": priority})
        self.result_box.insert(tk.END, f"Task Added. {name} ({start:.2f}-{end:.2f}, Priority: {priority})\n")


    def optimize_tasks(self):
        task_tuples = [(task['name'], task['start'], task['end']) for task in self.tasks]
        optimized = select_activities(task_tuples)
    
        self.result_box.insert(tk.END, "Optimized Task Schedule:\n")
        for name, start, end in optimized:
            self.result_box.insert(tk.END, f"- {name} ({start}-{end})\n")
        self.result_box.insert(tk.END, "\n")


    def sort_tasks(self):
        criteria = self.sort_option.get()
        self.result_box.insert(tk.END, f"Sorting tasks by {criteria}\n")

        criteria_map = {
            "Start Time": "start",
            "End Time": "end",
            "Priority": "priority"
        }

        if criteria not in criteria_map:
            self.result_box.insert(tk.END, "Invalid sorting criteria.\n")
            return

        key = criteria_map[criteria]
        sorted_tasks = sorted(self.tasks, key=lambda task: int(task.get(key, 0)))
    
        self.result_box.delete(1.0, tk.END)
        self.result_box.insert(tk.END, f"Tasks sorted by {criteria}:\n")
        for task in sorted_tasks:
            name = task['name']
            start = task['start']
            end = task['end']
            priority = task.get('priority', 0)
            self.result_box.insert(tk.END, f"- {name}: Start {start}, End {end}\n")

    def show_map(self):
        win = tk.Toplevel(self.root)
        win.title("Campus Map")
        win.geometry("1000x800")

        fig = draw_graph(
        self.graph,
        highlight_path=getattr(self, 'last_path', None),
    )
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartCampusGUI(root)
    root.mainloop()
