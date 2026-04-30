import random
import time
import threading
from collections import deque

class Link:
    def __init__(self, loss_rate, min_latency, max_latency, bandwidth_pps=10, buffer_size=50):
        self.loss_rate = loss_rate
        self.min_latency = min_latency
        self.max_latency = max_latency

        self.bandwidth_pps = bandwidth_pps  # packets per second
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
        interval = 1 / self.bandwidth_pps

        while True:
            time.sleep(interval)

            with self.lock:
                # Check if all queues are empty
                if not any(self.queues.values()):
                    continue

                packet = None
                receiver = None

                # Priority order
                for p in ["P0", "P1", "P2", "P3"]:
                    if self.queues[p]:
                        packet, receiver = self.queues[p].popleft()
                        break

            # Packet loss
            if random.random() < self.loss_rate:
                continue

            latency = random.uniform(self.min_latency, self.max_latency)

            def deliver():
                time.sleep(latency)
                receiver.receive(packet, latency)

            threading.Thread(target=deliver).start()