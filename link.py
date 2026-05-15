import random
import time
import threading
from collections import deque

class Link:
    def __init__(self, loss_rate, min_latency, max_latency, bandwidth_bps, buffer_size=50):
        self.loss_rate = loss_rate
        self.min_latency = min_latency
        self.max_latency = max_latency

        self.bandwidth_bps = bandwidth_bps # packets per second
        self.buffer_size = buffer_size

        self.queues = {
            "P0": deque(),
            "P1": deque(),
            "P2": deque(),
            "P3": deque()
        }
        self.lock = threading.Lock()

        # Start worker thread
        threading.Thread(target=self.process_queue, daemon=True).start()

    def transmit(self, packet, receiver):
        priority = packet["type"]

        with self.lock:
            total_size = sum(len(q) for q in self.queues.values())

            if total_size >= self.buffer_size:
                # Drop lowest priority first
                for p in ["P3", "P2", "P1"]:
                    if self.queues[p]:
                        self.queues[p].pop()
                        print(f"[LINK] Dropped {p} packet")
                        break
                else:
                    # Only P0 left → drop incoming packet
                    print("[LINK] Critical buffer full → drop incoming")
                    return

            self.queues[priority].append((packet, receiver))

    def process_queue(self):
        while True:

            with self.lock:

                if not any(self.queues.values()):
                    continue

                packet = None
                receiver = None

                # Priority order
                for p in ["P0", "P1", "P2", "P3"]:
                    if self.queues[p]:
                        packet, receiver = self.queues[p].popleft()
                        break

            # Simulate packet loss
            if random.random() < self.loss_rate:
                continue

            # Transmission delay (bytes / bandwidth)
            transmission_delay = packet["size"] / self.bandwidth_bps

            # RF / network latency
            propagation_delay = random.uniform(
                self.min_latency,
                self.max_latency
            )

            total_delay = transmission_delay + propagation_delay

            def deliver():
                time.sleep(total_delay)
                receiver.receive(packet, total_delay)

            threading.Thread(target=deliver).start()