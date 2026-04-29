import time
from node import Node
from link import Link
from metrics import print_metrics
import config

def run_simulation():
    node_a = Node("A")
    node_b = Node("B")

    link = Link(
        config.PACKET_LOSS_RATE,
        config.MIN_LATENCY,
        config.MAX_LATENCY
    )

    start_time = time.time()

    while time.time() - start_time < config.SIMULATION_TIME:
        node_a.send(link, node_b)
        time.sleep(config.SEND_INTERVAL)

    # wait for remaining packets
    time.sleep(1)

    print_metrics(node_a, node_b)

if __name__ == "__main__":
    run_simulation()
