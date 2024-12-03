import dearpygui
import dearpygui.dearpygui as dpg

import grpc
import Raft_pb2
import Raft_pb2_grpc
import RaftManager_pb2
import RaftManager_pb2_grpc
from concurrent import futures

import sys
import time
import threading
import subprocess
import os

PORT = 40000

NODE_PORT_OFFSET = 50000


class Node:
    def __init__(self, manager, nodeId: int):
        self.nodeId = nodeId
        self.manager = manager
        self.isActive = True
        self.isRunning = True
        self.process = subprocess.Popen(
            ["python", "RaftNode.py", str(nodeId)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )
        self.stdoutThread = threading.Thread(target=self.ReadStdout)
        self.stdoutThread.start()

    def ReadStdout(self):
        while self.isRunning:
            line = self.process.stdout.readline()

            if line == "" or line == "\n":
                continue
            print(f"Node {self.nodeId}: {line}", end="")

        self.process.stdout.close()
        self.process.stderr.close()

    def Stop(self):
        # result = self.process.terminate()
        # if result:
        #     print("Node " + str(self.nodeId) + " stopped")
        self.isRunning = False

        try:
            with grpc.insecure_channel(
                f"localhost:{NODE_PORT_OFFSET + self.nodeId}"
            ) as channel:
                stub = Raft_pb2_grpc.RaftStub(channel)
                stub.Stop(Raft_pb2.StopRequest())
        except grpc.RpcError as e:
            pass


class RaftManager(RaftManager_pb2_grpc.RaftManagerServicer):
    def __init__(self):
        self.nodeList = []
        self.selectedNode = 0
        self.Setup()

    def Setup(self):
        dpg.create_context()
        dpg.create_viewport(title="RaftManager", width=800, height=600)

        with dpg.window(
            label="RaftManager", width=800, height=600, tag="main_window", no_close=True
        ):
            with dpg.table(header_row=True, width=800, tag="raft_table") as nodeTable:
                dpg.add_table_column(label="ID")
                dpg.add_table_column(label="Port")
                dpg.add_table_column(label="IsActive")
                dpg.add_table_column(label="Role")
                dpg.add_table_column(label="CurrentTerm")

                for i in range(5):
                    with dpg.table_row():
                        dpg.add_selectable(
                            label=f"Node {i}",
                            tag=f"node_{i}",
                            callback=self.HandleSelectNode,
                            user_data=i,
                        )
                        dpg.add_text(NODE_PORT_OFFSET + i, tag=f"node_port_{i}")
                        dpg.add_text(True, tag=f"node_active_{i}")
                        dpg.add_text("Role", tag=f"node_role_{i}")
                        dpg.add_text(0, tag=f"node_term_{i}")
            with dpg.table(header_row=True, width=800, tag="node_table"):
                dpg.add_table_column(label="ID")
                for i in range(5):
                    dpg.add_table_column(label=f"Node {i}")

                for i in range(5):
                    with dpg.table_row():
                        dpg.add_text(f"Node {i}")
                        for j in range(5):
                            if i == j:
                                dpg.add_text("X")
                                continue
                            if i < j:
                                dpg.add_text("-")
                                continue
                            dpg.add_checkbox(
                                tag=f"node_{i}_{j}",
                                callback=self.HandleTogglePeer,
                                user_data=f"{i}_{j}",
                                default_value=True,
                            )

            dpg.add_text(tag="SelectedNodeText", default_value="Selected node: -1")
            dpg.add_button(label="Enable", callback=self.HandleEnableButton)
            dpg.add_button(label="Disable", callback=self.HandleDisableButton)
            dpg.add_button(label="Enable All", callback=self.HandleEnableAllButton)
            dpg.add_button(label="Disable All", callback=self.HandleDisableAllButton)

        dpg.setup_dearpygui()
        dpg.show_viewport()

    def HandleSelectNode(self, sender, app_data, user_data):
        print(f"Selected node: {user_data}")
        self.selectedNode = user_data
        dpg.set_value("SelectedNodeText", f"Selected node: {user_data}")

    def HandleTogglePeer(self, sender, app_data, user_data):
        print(f"Toggle peer: {user_data}: {dpg.get_value(user_data)}")

    def HandleEnableButton(self):
        if self.selectedNode != -1:
            print(f"Enabled node: {self.selectedNode}")
            self.nodeList[self.selectedNode].isActive = True
            self.SetActive(self.selectedNode, True)
            dpg.set_value(f"node_active_{self.selectedNode}", True)

    def HandleDisableButton(self):
        if self.selectedNode != -1:
            print(f"Disabled node: {self.selectedNode}")
            self.nodeList[self.selectedNode].isActive = False
            self.SetActive(self.selectedNode, False)
            dpg.set_value(f"node_active_{self.selectedNode}", False)

    def HandleEnableAllButton(self):
        for node in self.nodeList:
            node.isActive = True
            self.SetActive(node.nodeId, True)
            dpg.set_value(f"node_active_{node.nodeId}", True)

    def HandleDisableAllButton(self):
        for node in self.nodeList:
            node.isActive = False
            self.SetActive(node.nodeId, False)
            dpg.set_value(f"node_active_{node.nodeId}", False)

    # def Loop(self):
    #     try:
    #         while dpg.is_dearpygui_running():
    #             dpg.render_dearpygui_frame()
    #     except KeyboardInterrupt:
    #         pass

    def Run(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        RaftManager_pb2_grpc.add_RaftManagerServicer_to_server(self, server)
        server.add_insecure_port(f"[::]:{PORT}")
        server.start()
        time.sleep(1)
        self.nodeList = [Node(self, i) for i in range(5)]
        dpg.start_dearpygui()
        dpg.destroy_context()
        for node in self.nodeList:
            node.Stop()

    def SendIsActive(self, request, context):
        nodeId = request.nodeId
        isActive = request.isActive
        self.nodeList[nodeId].isActive = isActive
        dpg.set_value(f"node_active_{nodeId}", isActive)
        return RaftManager_pb2.IsActiveResponse(isActive=self.nodeList[nodeId].isActive)

    def SendRole(self, request, context):
        nodeId = request.nodeId
        role = request.role
        self.nodeList[nodeId].role = role
        dpg.set_value(f"node_role_{nodeId}", role)
        return RaftManager_pb2.RoleResponse(role=self.nodeList[nodeId].role)

    def SendTerm(self, request, context):
        nodeId = request.nodeId
        term = request.term
        dpg.set_value(f"node_term_{nodeId}", term)
        return RaftManager_pb2.TermResponse(term=self.nodeList[nodeId].currentTerm)

    def SetActive(self, nodeId, isActive):
        self.nodeList[nodeId].isActive = isActive
        with grpc.insecure_channel(f"localhost:{NODE_PORT_OFFSET + nodeId}") as channel:
            stub = Raft_pb2_grpc.RaftStub(channel)
            try:
                stub.SetIsActive(Raft_pb2.SetIsActiveRequest(isActive=isActive))
            except grpc.RpcError as e:
                pass


if __name__ == "__main__":
    manager = RaftManager()
    manager.Run()
    sys.exit(0)
