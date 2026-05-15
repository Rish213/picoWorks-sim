import time
import config


class LinkEstimator:
    def __init__(self, window_size=5):
        self.window_size = window_size

        # Logs
        self.sent_log = []
        self.recv_log = []
        self.latency_log = []

    def log_sent(self, packet):
        now = time.time()

        self.sent_log.append({
            "time": now,
            "size": packet["size"]
        })

    def log_received(self, packet, latency):

        self.recv_log.append({
            "time": time.time(),
            "size": packet["size"]
        })

        self.latency_log.append({
            "time": time.time(),
            "latency": latency
        })

    def compute(self):
        now = time.time()

        # Sliding window filtering
        self.sent_log = [
            p for p in self.sent_log
            if now - p["time"] <= self.window_size
        ]

        self.recv_log = [
            p for p in self.recv_log
            if now - p["time"] <= self.window_size
        ]

        self.latency_log = [
            p for p in self.latency_log
            if now - p["time"] <= self.window_size
        ]

        # Byte accounting
        sent_bytes = 0
        recv_bytes = 0

        for p in self.sent_log:
            sent_bytes += p["size"]

        for p in self.recv_log:
            recv_bytes += p["size"]

        # Average latency
        avg_latency = 0

        if len(self.latency_log) > 0:
            total_latency = 0

            for p in self.latency_log:
                total_latency += p["latency"]

            avg_latency = total_latency / len(self.latency_log)

        # Prevent divide-by-zero
        if sent_bytes == 0:
            return {
                "loss": 0,
                "throughput": 0,
                "latency": avg_latency,
                "valid": False
            }

        # Proper bounded loss
        loss = 1 - (recv_bytes / sent_bytes)

        loss = max(0, min(1, loss))

        # Throughput in bytes/sec
        throughput = recv_bytes / self.window_size

        return {
            "loss": loss,
            "throughput": throughput,
            "latency": avg_latency,
            "valid": True
        }