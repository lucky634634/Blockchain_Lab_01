import tkinter as tk
from tkinter import messagebox
import subprocess
import threading

PORT = 50000


class RaftManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Raft Manager")
        self.nodes = {}
        self.node_processes = {}
        self.node_id_counter = 0
        self.child_windows = {}
        self.Setup()

    def AddNode(self):
        node_id = self.node_id_counter
        self.node_id_counter += 1
        self.node_list.insert(tk.END, f"Node {node_id}")
        print(f"Node {node_id} added")
        self.node_processes[node_id] = subprocess.Popen(
            ["python", "RaftNode.py", str(node_id)]
        )
        pass

    def RemoveNode(self):
        if self.node_list.curselection():
            node_id = self.node_list.curselection()[0]
            self.node_list.delete(node_id)
            self.node_processes[node_id].terminate()
            print(f"Node {node_id} removed")
            if node_id in self.child_windows:
                self.child_windows[node_id].destroy()
                del self.child_windows[node_id]

    def ViewNode(self):
        if self.node_list.curselection():
            node_id = self.node_list.curselection()[0]
            print(f"Viewing Node {node_id}")
            self.child_windows[node_id] = tk.Toplevel(self.root)
            self.child_windows[node_id].title(f"Node {node_id}")
            self.child_windows[node_id].geometry("800x600")
            self.child_windows[node_id].frame = tk.Frame(self.child_windows[node_id])

    def Setup(self):
        self.root.geometry("800x600")

        self.root.frame = tk.Frame(self.root)
        self.root.frame.pack()
        self.node_list = tk.Listbox(self.root.frame, width=100, height=10)
        self.node_list.pack(pady=10)

        self.add_node_button = tk.Button(
            self.root.frame, text="Add Node", command=self.AddNode
        )
        self.add_node_button.pack(pady=10)

        self.remove_node_button = tk.Button(
            self.root.frame, text="Remove Node", command=self.RemoveNode
        )
        self.remove_node_button.pack(pady=10)

        self.view_node_button = tk.Button(
            self.root.frame, text="View Node", command=self.ViewNode
        )
        self.view_node_button.pack(pady=10)

    def GetState(self, node_id):
        pass

    def SetState(self, node_id, state):
        pass

    def Run(self):
        self.root.mainloop()


if __name__ == "__main__":
    manager = RaftManager()
    manager.Run()
