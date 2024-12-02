import grpc
from concurrent import futures
import time
import random
import raft_pb2
import raft_pb2_grpc

import RaftManager_pb2
import RaftManager_pb2_grpc

MANAGER_PORT = 50000


class RaftNode(raft_pb2_grpc.RaftServicer):
    def __init__(self, node_id, port):
        self.node_id = node_id
        self.port = port
        self.isActive = True
        self.peers = []

        # Node states
        self.role = "follower"
        self.current_term = 0
        self.voted_for = None
        self.log = []  # List of LogEntry(term, command)

        # Commit state
        self.commit_index = 0
        self.last_applied = 0

        # Leader state
        self.next_index = {}
        self.match_index = {}

        # Timeout and election
        self.election_timeout = random.uniform(5, 10)
        self.timeout_reset = time.time()
    
    def setup(self):
        self.role = "follower"
        self.current_term = 0
        self.voted_for = None
        self.log = []  # List of LogEntry(term, command)

        # Commit state
        self.commit_index = 0
        self.last_applied = 0

        # Leader state
        self.next_index = {}
        self.match_index = {}

        self.timeout_reset = time.time()

    def RequestVote(self, request, context):
        if request.term > self.current_term:
            self.current_term = request.term
            self.role = "follower"
            self.voted_for = None

        vote_granted = False
        if (self.voted_for is None or self.voted_for == request.candidateId) and (
            len(self.log) == 0
            or (
                request.lastLogTerm > self.log[-1].term
                or (
                    request.lastLogTerm == self.log[-1].term
                    and request.lastLogIndex >= len(self.log) - 1
                )
            )
        ):
            self.voted_for = request.candidateId
            vote_granted = True

        print(
            f"Node {self.node_id} received RequestVote from Node {request.candidateId}: {'Granted' if vote_granted else 'Denied'}"
        )
        return raft_pb2.RequestVoteResponse(
            term=self.current_term, voteGranted=vote_granted
        )

    def AppendEntries(self, request, context):
        if request.term < self.current_term:
            return raft_pb2.AppendEntriesResponse(term=self.current_term, success=False)

        # Reset election timeout since we received a heartbeat
        self.timeout_reset = time.time()
        self.role = "follower"
        self.current_term = request.term

        # Check log consistency
        if request.prevLogIndex >= len(self.log) or (
            request.prevLogIndex >= 0
            and self.log[request.prevLogIndex].term != request.prevLogTerm
        ):
            return raft_pb2.AppendEntriesResponse(term=self.current_term, success=False)

        # Append new entries
        self.log = self.log[: request.prevLogIndex + 1] + list(request.entries)

        # Update commit index
        if request.leaderCommit > self.commit_index:
            self.commit_index = min(request.leaderCommit, len(self.log) - 1)

        print(
            f"Node {self.node_id} received AppendEntries from Leader {request.leaderId}"
        )
        return raft_pb2.AppendEntriesResponse(term=self.current_term, success=True)

    def start_election(self):
        self.current_term += 1
        self.role = "candidate"
        self.voted_for = self.node_id
        votes = 1
        total_votes = 0

        print(f"Node {self.node_id} starting election for term {self.current_term}")

        for peer in self.peers:
            with grpc.insecure_channel(f"localhost:{peer}") as channel:
                try:
                    stub = raft_pb2_grpc.RaftStub(channel)
                    total_votes += 1
                    response = stub.GetIsActive(raft_pb2.GetIsActiveRequest(nodeId = self.node_id))
                    if not response.active:
                        continue
                    response = stub.RequestVote(
                        raft_pb2.RequestVoteRequest(
                            term=self.current_term,
                            candidateId=self.node_id,
                            lastLogIndex=len(self.log) - 1,
                            lastLogTerm=self.log[-1].term if self.log else 0,
                        )
                    )
                    if response.voteGranted:
                        votes += 1
                        print(
                            f"Node {self.node_id} received vote from Node {peer - 50050}"
                        )
                except grpc.RpcError as e:
                    self.HandleError(e)
                

        if votes > total_votes // 2:
            self.role = "leader"
            print(f"Node {self.node_id} became the leader for term {self.current_term}")

        self.SendRoleToManager()

    def HandleError(self, e):
        if e.code() == grpc.StatusCode.UNAVAILABLE:
            print("UNAVAILABLE")
            return
        if e.code() == grpc.StatusCode.UNIMPLEMENTED:
            print("UNIMPLEMENTED")
            return
        if e.code() == grpc.StatusCode.CANCELLED:
            print("CANCELLED")
            return
        if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
            print("DEADLINE_EXCEEDED")
            return
        if e.code() == grpc.StatusCode.INTERNAL:
            print("INTERNAL")
            return
        if e.code() == grpc.StatusCode.UNKNOWN:
            print("UNKNOWN")
            return
        if e.code() == grpc.StatusCode.UNAUTHENTICATED:
            print("UNAUTHENTICATED")
            return
        if e.code() == grpc.StatusCode.PERMISSION_DENIED:
            print("PERMISSION_DENIED")
            return
        if e.code() == grpc.StatusCode.RESOURCE_EXHAUSTED:
            print("RESOURCE_EXHAUSTED")
            return

    def run(self):
        try:
            while True:
                if self.isActive == False:
                    self.setup()
                    continue
                if (
                    self.role == "follower"
                    and time.time() - self.timeout_reset > self.election_timeout
                ):
                    self.start_election()
                elif self.role == "leader":
                    self.send_heartbeats()
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass

    def send_heartbeats(self):
        print(f"Leader Node {self.node_id} sending heartbeats")
        for peer in self.peers:
            with grpc.insecure_channel(f"localhost:{peer}") as channel:
                try:
                    stub = raft_pb2_grpc.RaftStub(channel)
                    response = stub.GetIsActive(raft_pb2.GetIsActiveRequest(nodeId = self.node_id))
                    if not response.active:
                        continue
                    stub.AppendEntries(
                        raft_pb2.AppendEntriesRequest(
                            term=self.current_term,
                            leaderId=self.node_id,
                            prevLogIndex=len(self.log) - 1,
                            prevLogTerm=self.log[-1].term if self.log else 0,
                            entries=[],
                            leaderCommit=self.commit_index,
                        )
                    )
                except grpc.RpcError:
                    print(
                        f"Leader Node {self.node_id} failed to connect to Node {peer - 50050}"
                    )

    def SetIsActive(self, request, context):
        self.isActive = request.active
        self.role = "follower"
        print(f"Node {self.node_id} set active to {request.active}")
        return raft_pb2.SetIsActiveResponse(success=True)

    def GetIsActive(self, request, context):
        return raft_pb2.GetIsActiveResponse(active=self.isActive)

    def AddPeer(self, request, context):
        if request.port in self.peers:
            return raft_pb2.AddPeerResponse(success=False)
        self.peers.append(request.port)
        print(f"Node {self.node_id} added peer {request.port}")
        return raft_pb2.AddPeerResponse(success=True)

    def RemovePeer(self, request, context):
        self.peers.remove(request.port)
        return raft_pb2.RemovePeerResponse(success=True)

    def GetPeers(self, request, context):
        return raft_pb2.GetPeersResponse(peers=self.peers)

    def GetNodeId(self, request, context):
        return raft_pb2.GetNodeIdResponse(nodeId=self.node_id)

    def GetRole(self, request, context):
        return raft_pb2.GetRoleResponse(role=self.role)
    
    def Test(self, request, context):
        return raft_pb2.TestResponse(success=self.isActive)

    def SendRoleToManager(self):
        try:
            with grpc.insecure_channel(f"localhost:{MANAGER_PORT}") as channel:
                stub = RaftManager_pb2_grpc.RaftManagerStub(channel)
                stub.SendRole(
                    RaftManager_pb2.SendRoleRequest(nodeId=self.node_id, role=self.role)
                )
        except grpc.RpcError:
            print(f"Node {self.node_id} failed to connect to manager")
        print(f"Node {self.node_id} sent role {self.role} to manager")

    def Serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        raft_pb2_grpc.add_RaftServicer_to_server(self, server)
        server.add_insecure_port(f"[::]:{self.port}")
        server.start()
        print(f"Node {self.node_id} running on port {self.port}")
        self.run()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python RaftNode.py <node_id>")
        sys.exit(1)
    node_id = int(sys.argv[1])
    port = 50050 + node_id
    node = RaftNode(node_id, port)
    node.Serve()
