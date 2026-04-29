import time

class Node:
    def __init__(self, name):
        self.name = name
        self.received_packets = 0
        self.sent_packets = 0

    def send(self, link, receiver):
        packet = {
            "timestamp": time.time()
        }
        self.sent_packets += 1
        link.transmit(packet, receiver)

    def receive(self, packet, latency):
        self.received_packets += 1
        now = time.time()
        actual_latency = now - packet["timestamp"]

        print(f"[{self.name}] Received packet | Latency: {actual_latency:.3f}s")
