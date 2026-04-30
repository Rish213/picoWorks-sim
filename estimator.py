import time

class LinkEstimator:
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.sent_log = []
        self.recv_log = []
        self.latency_log = []

    def log_sent(self):
        self.sent_log.append(time.time())

    def log_received(self, latency):
        now = time.time()
        self.recv_log.append(now)
        self.latency_log.append((now, latency))

    def compute(self):
        now = time.time()

        # Sliding window filtering
        self.sent_log = [t for t in self.sent_log if now - t <= self.window_size]
        self.recv_log = [t for t in self.recv_log if now - t <= self.window_size]
        self.latency_log = [(t, l) for (t, l) in self.latency_log if now - t <= self.window_size]

        sent = len(self.sent_log)
        received = len(self.recv_log)

        if sent < 5:
            return {
                "loss": 0,
                "throughput": 0,
                "latency": 0,
                "valid": False
            }

        loss = 1 - (received / sent)
        throughput = received / self.window_size

        # Average latency
        if self.latency_log:
            avg_latency = sum(l for (_, l) in self.latency_log) / len(self.latency_log)
        else:
            avg_latency = 0

        return {
            "loss": loss,
            "throughput": throughput,
            "latency": avg_latency,
            "valid": True
        }