import grpc
import Raft_pb2
import Raft_pb2_grpc
import RaftManager_pb2
import RaftManager_pb2_grpc
from concurrent import futures

import sys
import time
import random

import Database

MANGER_PORT = 40000
NODE_PORT_OFFSET = 50000


class RaftNode(Raft_pb2_grpc.RaftServicer):
    def __init__(self, nodeId: int, port: int):
        self.isRunning = True
        self.isActive = True
        self.nodeId = nodeId
        self.port = port
        self.peerPorts = [(NODE_PORT_OFFSET + i) for i in range(5) if i != nodeId]
        self.role = "Follower"  # Follower, Candidate, Leader
        self.currentTerm = 0
        self.voteFor = None

        self.log = []

        self.commitIndex = 0
        self.lastApplied = 0

        self.nextIndex = {}
        self.matchIndex = {}

        self.electionTimeout = random.uniform(5, 10)
        self.timeoutReset = time.time()

        self.leaderId = None

        self.database = Database.Database()

    def SetIsActive(self, request, context):
        self.isActive = request.isActive
        return Raft_pb2.SetIsActiveResponse(isActive=self.isActive)

    def GetIsActive(self, request, context):
        return Raft_pb2.GetIsActiveResponse(isActive=self.isActive)

    def RequestVote(self, request, context):
        print(f"Node {self.nodeId} received vote request from {request.candidateId}")
        if request.term < self.currentTerm:
            return Raft_pb2.RequestVoteResponse(
                term=self.currentTerm, voteGranted=False
            )
        if (self.voteFor is None or self.voteFor == request.candidateId) and (
            len(self.log) == 0
            or self.log[-1].term < request.lastLogTerm
            or request.lastLogIndex >= len(self.log) - 1
        ):
            self.voteFor = request.candidateId
            return Raft_pb2.RequestVoteResponse(term=self.currentTerm, voteGranted=True)
        return Raft_pb2.RequestVoteResponse(term=self.currentTerm, voteGranted=False)

    def AppendEntries(self, request, context):
        if request.term < self.currentTerm:
            return Raft_pb2.AppendEntriesResponse(term=self.currentTerm, success=False)

        # print(f"Node {self.nodeId} received append entries from {request.leaderId}")
        self.timeoutReset = time.time()
        self.role = "Follower"
        self.currentTerm = request.term
        self.leaderId = request.leaderId
        self.SendRole()

        if request.prevLogIndex >= len(self.log) or (
            request.prevLogIndex >= 0
            and self.log[request.prevLogIndex].term != request.prevLogTerm
        ):
            return Raft_pb2.AppendEntriesResponse(term=self.currentTerm, success=False)

        self.log = self.log[: request.prevLogIndex + 1] + list(request.entries)

        if request.leaderCommit > self.commitIndex:
            self.commitIndex = min(request.leaderCommit, len(self.log) - 1)
            self.ApplyLog()

        return Raft_pb2.AppendEntriesResponse(term=self.currentTerm, success=True)

    def AddPeer(self, request, context):
        if request.port in self.peerPorts:
            return Raft_pb2.AddPeerResponse(port=request.port)

        self.peerPorts.append(request.port)
        self.peerPorts.sort()
        print("Add peer port" + str(request.port))
        return Raft_pb2.AddPeerResponse(port=request.port)

    def RemovePeer(self, request, context):
        if request.port not in self.peerPorts:
            return Raft_pb2.RemovePeerResponse(port=request.port)

        self.peerPorts.remove(request.port)
        print("Remove peer port" + str(request.port))
        return Raft_pb2.RemovePeerResponse(port=request.port)

    def StartElection(self):
        self.role = "Candidate"
        self.currentTerm += 1
        self.voteFor = None
        votes = 1
        totalVotes = 1
        for peerPort in self.peerPorts:
            try:
                with grpc.insecure_channel(f"localhost:{peerPort}") as channel:
                    stub = Raft_pb2_grpc.RaftStub(channel)
                    response = stub.GetIsActive(
                        Raft_pb2.GetIsActiveRequest(isActive=True)
                    )
                    if response.isActive == False:
                        continue
                    totalVotes += 1
                    response = stub.RequestVote(
                        Raft_pb2.RequestVoteRequest(
                            term=self.currentTerm,
                            candidateId=self.nodeId,
                            lastLogIndex=len(self.log) - 1,
                            lastLogTerm=self.log[-1].term if len(self.log) > 0 else 0,
                        )
                    )
                    if response.voteGranted:
                        votes += 1
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.UNKNOWN:
                    print(f"Error: Unknown peer {peerPort}")
                if e.code() == grpc.StatusCode.UNAVAILABLE:
                    print(f"Error: Unavailable peer {peerPort}")
        print(f"Node {self.nodeId} received {votes} votes out of {totalVotes}")
        if votes > totalVotes // 2:
            self.role = "Leader"
            self.leaderId = self.nodeId
            print(f"Node {self.nodeId} became leader")
        self.SendRole()

    def SendHeartBeats(self):
        for peer in self.peerPorts:
            with grpc.insecure_channel(f"localhost:{peer}") as channel:
                try:
                    stub = Raft_pb2_grpc.RaftStub(channel)
                    response = stub.GetIsActive(
                        Raft_pb2.GetIsActiveRequest(isActive=True)
                    )

                    if not response.isActive:
                        continue

                    stub.AppendEntries(
                        Raft_pb2.AppendEntriesRequest(
                            term=self.currentTerm,
                            leaderId=self.nodeId,
                            prevLogIndex=len(self.log) - 1,
                            prevLogTerm=self.log[-1].term if len(self.log) > 0 else 0,
                            entries=[],
                            leaderCommit=self.commitIndex,
                        )
                    )
                except grpc.RpcError as e:
                    if e.code() == grpc.StatusCode.UNKNOWN:
                        print(f"Error: Unknown peer {peer}")

    def ApplyLog(self):
        while self.lastApplied < self.commitIndex:
            self.lastApplied += 1
            term, command = self.log[self.lastApplied]
            self.database.ApplyCommand(command)

    def SendCommand(self, request, context):
        if not self.isActive:
            return Raft_pb2.SendCommandResponse(status="Not active")
        if self.role != "Leader":
            return Raft_pb2.SendCommandResponse(status="Not leader")
        print(f"Node {self.nodeId} received command {request.command}")

        status = self.database.ApplyCommand(request.command)
        print(
            f"Node {self.nodeId} applied command {request.command} and returned status {status}"
        )

        return Raft_pb2.SendCommandResponse(status=status)

    def GetId(self, port: int) -> int:
        return port - NODE_PORT_OFFSET

    def Loop(self):
        self.SendIsActive()
        self.SendRole()
        try:
            while self.isRunning:
                if not self.isActive:
                    time.sleep(1)
                    continue
                # if self.leaderId != None:
                #     with grpc.insecure_channel(
                #         f"localhost:{self.leaderId + NODE_PORT_OFFSET}"
                #     ) as channel:
                #         stub = Raft_pb2_grpc.RaftStub(channel)
                #         try:
                #             response = stub.GetIsActive(
                #                 Raft_pb2.GetIsActiveRequest(isActive=True)
                #             )
                #             if response.isActive == False:
                #                 self.leaderId = None
                #                 self.timeoutReset = time.time()
                #                 self.role = "Follower"
                #         except grpc.RpcError as e:
                #             if e.code() == grpc.StatusCode.UNKNOWN:
                #                 print(f"Error: Unknown leader {self.leaderId}")
                #             if e.code() == grpc.StatusCode.UNAVAILABLE:
                #                 print(f"Error: Unavailable leader {self.leaderId}")
                if (
                    self.role != "Leader"
                    and time.time() - self.timeoutReset > self.electionTimeout
                ):
                    self.StartElection()
                elif self.role == "Leader":
                    self.SendHeartBeats()
                self.SendIsActive()
                self.SendRole()
                self.SendTerm()
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass

    def Run(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        Raft_pb2_grpc.add_RaftServicer_to_server(self, server)
        server.add_insecure_port(f"[::]:{port}")
        print(f"Starting node {nodeId} on port {port}")
        server.start()
        self.Loop()
        print(f"Node {nodeId} stopped")

    def SendIsActive(self):
        try:
            with grpc.insecure_channel(f"localhost:{MANGER_PORT}") as channel:
                stub = RaftManager_pb2_grpc.RaftManagerStub(channel)
                response = stub.SendIsActive(
                    RaftManager_pb2.IsActiveRequest(
                        nodeId=self.nodeId, isActive=self.isActive
                    )
                )
        except grpc.RpcError as e:
            pass

    def SendRole(self):
        try:
            with grpc.insecure_channel(f"localhost:{MANGER_PORT}") as channel:
                stub = RaftManager_pb2_grpc.RaftManagerStub(channel)
                response = stub.SendRole(
                    RaftManager_pb2.SendRoleRequest(nodeId=self.nodeId, role=self.role)
                )
        except grpc.RpcError as e:
            pass

    def SendTerm(self):
        try:
            with grpc.insecure_channel(f"localhost:{MANGER_PORT}") as channel:
                stub = RaftManager_pb2_grpc.RaftManagerStub(channel)
                response = stub.SendTerm(
                    RaftManager_pb2.SendTermRequest(
                        nodeId=self.nodeId, term=self.currentTerm
                    )
                )
        except grpc.RpcError as e:
            pass

    def Stop(self, request, context):
        self.isRunning = False
        return Raft_pb2.StopResponse(stopped=True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python RaftNode.py <port>")
        sys.exit(1)

    nodeId = int(sys.argv[1])
    port = NODE_PORT_OFFSET + nodeId

    node = RaftNode(nodeId, port)
    node.Run()
