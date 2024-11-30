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

        self.setup()

    def add_node(self):
        node_id = self.node_id_counter
        self.node_id_counter += 1
        self.node_list.insert(tk.END, f"Node {node_id}")
        print(f"Node {node_id} added")
        pass

    def remove_node(self):
        pass

    def setup(self):
        self.root.geometry("800x600")

        self.root.frame = tk.Frame(self.root)
        self.root.frame.pack()
        self.node_list = tk.Listbox(self.root.frame, width=100, height=10)
        self.node_list.pack(pady=10)

        self.add_node_button = tk.Button(
            self.root.frame, text="Add Node", command=self.add_node
        )
        self.add_node_button.pack(pady=10)

        self.remove_node_button = tk.Button(
            self.root.frame, text="Remove Node", command=self.remove_node
        )
        self.remove_node_button.pack(pady=10)

    def GetState(self, node_id):
        pass

    def SetState(self, node_id, state):
        pass

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    manager = RaftManager()
    manager.run()
