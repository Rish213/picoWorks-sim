import time
from node import Node
from link import Link
from estimator import LinkEstimator
from controller import ModeController
from metrics import print_metrics
import config

def run_simulation():
    node_a = Node("A")
    node_b = Node("B")

    link = Link(
        config.PACKET_LOSS_RATE,
        config.MIN_LATENCY,
        config.MAX_LATENCY,
        bandwidth_bps=config.LINK_BANDWIDTH,     
        buffer_size=30        
    )

    estimator = LinkEstimator()
    controller = ModeController()

    node_a.estimator = estimator
    node_b.estimator = estimator

    start_time = time.time()
    last_print = time.time()

    while time.time() - start_time < config.SIMULATION_TIME:

        stats = estimator.compute()

        # Only update mode if estimate is valid
        if stats["valid"]:
            mode = controller.update(
                stats["loss"],
                stats["throughput"],
                stats["latency"]    
            )
        else:
            mode = controller.mode  # hold previous mode

        node_a.send(link, node_b, mode)

        #send_interval = config.MODE_SEND_INTERVAL[mode]
        time.sleep(0.05)

        if time.time() - last_print >= 1:
            print(f"[ESTIMATOR] Loss: {stats['loss']:.2f} | Throughput: {stats['throughput']:.2f} B/s | Latency: {stats['latency']:.2f}s")            
            print(f"[CURRENT MODE] {mode}\n")
            last_print = time.time()

    # wait for remaining packets
    time.sleep(1)

    print_metrics(node_a, node_b)

if __name__ == "__main__":
    run_simulation()
