import tkinter as tk
from tkinter import messagebox
import subprocess
import threading

import grpc
import RaftManager_pb2
import RaftManager_pb2_grpc
from concurrent import futures

import raft_pb2
import raft_pb2_grpc

PORT = 50000


class Node:
    def __init__(self, node_id, port):
        self.node_id = node_id
        self.port = port
        self.isActive = True
        self.process = subprocess.Popen(
            ["python", "RaftNode.py", str(node_id)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True,
        )
        self.role = "follower"
        self.peers = []

        self.logText = ""

        self.stdout_thread = threading.Thread(target=self.UpdateLog)
        self.stdout_thread.start()

    def UpdateLog(self):
        while self.isActive:
            line = self.process.stdout.readline()
            if not line:
                continue
            self.logText = line + self.logText
            print(line, end="")
        self.process.stdout.close()
        self.process.stderr.close()

    def Terminate(self):
        result = self.process.terminate()
        if result:
            print(f"Node {self.node_id} terminated")
        self.isActive = False


class NodeWindow:
    def __init__(self, manager, node_id):
        self.manager = manager
        self.parent = manager.root
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
        self.GetPeers()
        self.logText = tk.Text(self.frame, width=80, height=10)
        self.logText.pack()
        self.UpdateLog()

    def GetPeers(self):
        self.listBox.delete(0, tk.END)
        for peer in self.manager.nodes[self.node_id].peers:
            self.listBox.insert(tk.END, peer)

    def UpdateLog(self):
        node = self.manager.nodes[self.node_id].logText
        self.logText.delete("1.0", "end")
        self.logText.insert("1.0", node)
        self.root.after(1000, self.UpdateLog)


class RaftManager(RaftManager_pb2_grpc.RaftManagerServicer):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Raft Manager")
        self.nodes = {}
        self.node_id_counter = 0
        self.child_windows = {}
        self.Setup()

    def AddNode(self):
        if len(self.nodes) >= 10:
            messagebox.showinfo("Error", "Cannot add more than 10 nodes")
            return
        node_id = self.node_id_counter
        self.node_id_counter += 1
        raftNode = Node(node_id, 50050 + node_id)
        self.nodes[node_id] = raftNode
        self.node_list.insert(tk.END, node_id)
        for node in self.nodes:
            for other in self.nodes:
                if other != node and other not in self.nodes[node].peers:
                    self.AddPeer(node, 50050 + other)

    def RemoveNode(self):
        if self.node_list.curselection():
            node_id = self.node_list.curselection()[0]
            print(f"Removing Node {node_id}")
            self.nodes[node_id].process.kill()
            self.node_list.delete(node_id)
            self.nodes.pop(node_id)
            if node_id in self.child_windows:
                self.child_windows[node_id].root.destroy()
                del self.child_windows[node_id]

        for other in self.nodes:
            self.RemovePeer(node_id, 50050 + other)

    def ViewNode(self):
        if self.node_list.curselection():
            node_id = self.node_list.curselection()[0]
            print(f"Viewing Node {node_id}")
            self.child_windows[node_id] = NodeWindow(self, node_id)

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

        self.EnableNodeButton = tk.Button(
            self.root.frame, text="Enable Node", command=self.EnableNode
        )
        self.EnableNodeButton.pack(pady=10)

        self.DisableNodeButton = tk.Button(
            self.root.frame, text="Disable Node", command=self.DisableNode
        )
        self.DisableNodeButton.pack(pady=10)

    def GetState(self, node_id):
        pass

    def SetState(self, node_id, state):
        pass

    def GetPeers(self, node_id):
        with grpc.insecure_channel(f"localhost:{self.nodes[node_id].port}") as channel:
            stub = raft_pb2_grpc.RaftStub(channel)
            response = stub.GetPeers(raft_pb2.GetPeersRequest())
            return response.peers

    def AddPeer(self, node_id, peer):
        with grpc.insecure_channel(f"localhost:{self.nodes[node_id].port}") as channel:
            stub = raft_pb2_grpc.RaftStub(channel)
            response = stub.AddPeer(raft_pb2.AddPeerRequest(port=peer))
            if response.success:
                self.nodes[node_id].peers.append(peer)

    def RemovePeer(self, node_id, peer):
        with grpc.insecure_channel(f"localhost:{self.nodes[node_id].port}") as channel:
            stub = raft_pb2_grpc.RaftStub(channel)
            response = stub.RemovePeer(raft_pb2.RemovePeerRequest(port=peer))
            if response.success:
                self.nodes[node_id].peers.remove(peer)

    def EnableNode(self):
        pass

    def DisableNode(self):
        pass

    def SendRole(self, request, context):
        node_id = request.nodeId
        role = request.role
        self.nodes[node_id].role = role
        return RaftManager_pb2.SendRoleResponse(success=True)

    def Run(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        RaftManager_pb2_grpc.add_RaftManagerServicer_to_server(self, server)
        server.add_insecure_port(f"[::]:{PORT}")
        server.start()
        self.root.mainloop()
        for node in self.nodes.values():
            node.Terminate()


if __name__ == "__main__":
    manager = RaftManager()
    manager.Run()
    exit(0)
