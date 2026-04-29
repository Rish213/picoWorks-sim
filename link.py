import random
import time
import threading

class Link:
    def __init__(self, loss_rate, min_latency, max_latency):
        self.loss_rate = loss_rate
        self.min_latency = min_latency
        self.max_latency = max_latency

    def transmit(self, packet, receiver):
        # Drop packet
        if random.random() < self.loss_rate:
            return

        latency = random.uniform(self.min_latency, self.max_latency)

        def delayed_delivery():
            time.sleep(latency)
            receiver.receive(packet, latency)

        threading.Thread(target=delayed_delivery).start()
