import time

class Node:
    def __init__(self, name):
        self.name = name
        self.received_packets = 0
        self.sent_packets = 0
        self.sent_timestamps = []
        self.received_timestamps = []

    def send(self, link, receiver, mode):
        now = time.time()

        # Initialize timers if not present
        if not hasattr(self, "last_p0"):
            self.last_p0 = 0
            self.last_p1 = 0
            self.last_p2 = 0

        # --- P0: ALWAYS send (critical loop) ---
        if now - self.last_p0 >= 0.1:   # 10 Hz
            packet = {
                "timestamp": now,
                "type": "P0"
            }
            link.transmit(packet, receiver)
            self.sent_packets += 1
            self.last_p0 = now

        # --- P1: metadata ---
        if mode in ["RAW", "VISUAL", "INFER"]:
            if now - self.last_p1 >= 0.3:   # ~3 Hz
                packet = {
                    "timestamp": now,
                    "type": "P1"
                }
                link.transmit(packet, receiver)
                self.sent_packets += 1
                self.last_p1 = now

        # --- P2: keyframes ---
        if mode in ["RAW", "VISUAL"]:
            if now - self.last_p2 >= 1.0:   # ~1 Hz
                packet = {
                    "timestamp": now,
                    "type": "P2"
                }
                link.transmit(packet, receiver)
                self.sent_packets += 1
                self.last_p2 = now

        # --- P3: video stream ---
        if mode == "RAW":
            # continuous stream (high load)
            packet = {
                "timestamp": now,
                "type": "P3"
            }
            link.transmit(packet, receiver)
            self.sent_packets += 1

    def receive(self, packet, latency):
        self.received_packets += 1
        self.received_timestamps.append(time.time())

        if hasattr(self, "estimator"):
            self.estimator.log_received(latency)   # ← IMPORTANT CHANGE

        now = time.time()
        actual_latency = now - packet["timestamp"]

        print(f"[{self.name}] {packet['type']} | Latency: {actual_latency:.3f}s")

    def get_packet_type(self, mode):
        import random

        if mode == "RAW":
            # heavy video
            r = random.random()
            if r < 0.05:
                return "P0"
            elif r < 0.15:
                return "P1"
            elif r < 0.35:
                return "P2"
            else:
                return "P3"

        elif mode == "VISUAL":
            r = random.random()
            if r < 0.1:
                return "P0"
            elif r < 0.3:
                return "P1"
            elif r < 0.6:
                return "P2"
            else:
                return "P3"

        elif mode == "INFER":
            r = random.random()
            if r < 0.2:
                return "P0"
            elif r < 0.5:
                return "P1"
            else:
                return "P2"

        elif mode == "SAFE":
            r = random.random()
            if r < 0.6:
                return "P0"
            else:
                return "P1"
