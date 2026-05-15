PACKET_LOSS_RATE = 0.3      # % packets dropped
MIN_LATENCY = 0.05         # seconds
MAX_LATENCY = 0.2
SIMULATION_TIME = 15        # seconds
SEND_INTERVAL = 0.1        # seconds
LINK_BANDWIDTH = 2_000_000   # bytes/sec (2 MB/s)


PACKET_SIZES = {
    "P0": 100,        # telemetry / commands
    "P1": 500,        # metadata
    "P2": 100_000,    # keyframe + bbox (~100 KB)
    "P3": 300_000     # video frame (~300 KB)
}

#USEFULNESS_THRESHOLDS = {
#    "P0": 0.5,   # telemetry / commands
#    "P1": 1.5,   # metadata
#    "P2": 3.0,   # keyframes
#    "P3": 5.0    # video
#}