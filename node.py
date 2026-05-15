import time
import config

class Node:
    def __init__(self, name):
        self.name = name
        self.received_packets = 0
        self.sent_packets = 0
        self.sent_timestamps = []
        self.received_timestamps = []

    def send(self, link, receiver, mode):
        now = time.time()

        # Initialize timers
        if not hasattr(self, "last_p0"):
            self.last_p0 = 0
            self.last_p1 = 0
            self.last_p2 = 0
            self.last_p3 = 0

        # --- P0: ALWAYS (10 Hz) ---
        if now - self.last_p0 >= 0.1:
            packet = {
                "timestamp": now,
                "type": "P0",
                "size": config.PACKET_SIZES["P0"]
            }
            link.transmit(packet, receiver)

            if hasattr(self, "estimator"):
                self.estimator.log_sent(packet)

            self.sent_packets += 1
            self.last_p0 = now

        # --- P1: ALWAYS (low rate, fallback awareness) ---
        if now - self.last_p1 >= 0.5:   # 2 Hz
            packet = {
                "timestamp": now,
                "type": "P1",
                "size": config.PACKET_SIZES["P1"]
            }
            link.transmit(packet, receiver)

            if hasattr(self, "estimator"):
                self.estimator.log_sent(packet)

            self.sent_packets += 1
            self.last_p1 = now

        # --- Mode-dependent layers ---

        # P2: keyframes (only VISUAL + RAW)
        if mode in ["VISUAL", "RAW"]:
            if now - self.last_p2 >= 1.0:

                packet = {
                    "timestamp": now,
                    "type": "P2",
                    "size": config.PACKET_SIZES["P2"]
                }

                link.transmit(packet, receiver)

                if hasattr(self, "estimator"):
                    self.estimator.log_sent(packet)

                self.sent_packets += 1
                self.last_p2 = now

        # P3: video stream (RAW only)
        if mode == "RAW":

            # ~10 FPS equivalent
            if now - self.last_p3 >= 0.1:

                packet = {
                    "timestamp": now,
                    "type": "P3",
                    "size": config.PACKET_SIZES["P3"]
                }

                link.transmit(packet, receiver)

                if hasattr(self, "estimator"):
                    self.estimator.log_sent(packet)

                self.sent_packets += 1
                self.last_p3 = now

    def receive(self, packet, latency):
        self.received_packets += 1
        self.received_timestamps.append(time.time())

        if hasattr(self, "estimator"):
            self.estimator.log_received(packet, latency)   

        now = time.time()
        actual_latency = now - packet["timestamp"]

        print(f"[{self.name}] {packet['type']} | Latency: {actual_latency:.3f}s")
