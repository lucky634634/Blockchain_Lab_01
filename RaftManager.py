import tkinter as tk
from tkinter import messagebox
import subprocess
import threading

import grpc
import RaftManager_pb2
import RaftManager_pb2_grpc
from concurrent import futures

PORT = 50000


class NodeWindow:
    def __init__(self, manager, node_id):
        self.parent = manager
        self.node_id = node_id
        self.Setup()

    def Setup(self):
        self.parent = manager.root
        self.root = tk.Toplevel(self.parent)
        self.root.title(f"Node {self.node_id}")
        self.root.geometry("800x600")
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.listBox = tk.Listbox(self.frame, width=100, height=10)
        self.listBox.pack()


class RaftManager(RaftManager_pb2_grpc.RaftManagerServicer):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Raft Manager")
        self.nodes = {}
        self.node_processes = {}
        self.node_id_counter = 0
        self.child_windows = {}
        self.Setup()

    def AddNode(self):
        if len(self.nodes) >= 10:
            messagebox.showinfo("Error", "Cannot add more than 10 nodes")
            return
        node_id = self.node_id_counter
        self.node_id_counter += 1
        self.node_list.insert(tk.END, f"Node {node_id}")
        print(f"Node {node_id} added")
        self.node_processes[node_id] = subprocess.Popen(
            ["python", "RaftNode.py", str(node_id)]
        )

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
            self.child_windows[node_id] = NodeWindow(self.root, node_id)

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

    def GetPeers(self, node_id):
        pass

    def AddPeer(self, node_id, peer):
        pass

    def RemovePeer(self, node_id, peer):
        pass

    def Run(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        RaftManager_pb2_grpc.add_RaftManagerServicer_to_server(self, server)
        server.add_insecure_port(f"[::]:{PORT}")
        server.start()
        self.root.mainloop()


if __name__ == "__main__":
    manager = RaftManager()
    manager.Run()
