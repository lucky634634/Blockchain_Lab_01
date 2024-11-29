import grpc
from concurrent import futures
import time
import random
import raft_pb2
import raft_pb2_grpc


class RaftNode(raft_pb2_grpc.RaftServicer):
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers

        # Node states
        self.state = "follower"
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

    def RequestVote(self, request, context):
        if request.term > self.current_term:
            self.current_term = request.term
            self.state = "follower"
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
        self.state = "follower"
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
        self.state = "candidate"
        self.voted_for = self.node_id
        votes = 1

        print(f"Node {self.node_id} starting election for term {self.current_term}")

        for peer in self.peers:
            print(f"Node {self.node_id} connecting to Node {peer}")
            with grpc.insecure_channel(peer) as channel:
                stub = raft_pb2_grpc.RaftStub(channel)
                try:
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
                            f"Node {self.node_id} received vote from Node {peer.split(':')[1]}"
                        )
                except grpc.RpcError:
                    print(f"Node {self.node_id} failed to connect to Node {peer}")

        if votes > len(self.peers) // 2:
            self.state = "leader"
            print(f"Node {self.node_id} became the leader for term {self.current_term}")

    def run(self):
        try:
            while True:
                time.sleep(0.1)
                if (
                    self.state == "follower"
                    and time.time() - self.timeout_reset > self.election_timeout
                ):
                    self.start_election()
                elif self.state == "leader":
                    self.send_heartbeats()
        except KeyboardInterrupt:
            pass

    def send_heartbeats(self):
        for peer in self.peers:
            print(
                f"Leader Node {self.node_id} sending heartbeat to Node {peer.split(':')[1]}"
            )
            with grpc.insecure_channel(peer) as channel:
                stub = raft_pb2_grpc.RaftStub(channel)
                try:
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
                        f"Leader Node {self.node_id} failed to send heartbeat to Node {peer.split(':')[1]}"
                    )


def serve(node_id, peers, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    node = RaftNode(node_id, peers)
    raft_pb2_grpc.add_RaftServicer_to_server(node, server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Node {node_id} running on port {port}")
    node.run()


if __name__ == "__main__":
    import sys

    node_id = int(sys.argv[1])
    port = 50050 + node_id
    peers = [f"localhost:{50050 + i}" for i in range(5) if i != node_id]
    serve(node_id, peers, port)
