import time

class ModeController:
    def __init__(self):
        self.mode = "RAW"
        self.last_mode_change = time.time()
        self.upgrade_hold_time = 2.0  # seconds

    def update(self, loss, throughput, latency):
        now = time.time()
        prev_mode = self.mode

        # 🔴 Immediate downgrade (safety first)
        if latency > 1.0:
            self.mode = "SAFE"
        elif latency > 0.6:
            self.mode = "INFER"
        elif throughput < 1:
            self.mode = "SAFE"

        else:
            # 🟢 Upgrade logic with delay
            if now - self.last_mode_change > self.upgrade_hold_time:

                if throughput > 9:
                    self.mode = "RAW"
                elif throughput > 5:
                    self.mode = "VISUAL"
                elif throughput > 2:
                    self.mode = "INFER"

        if self.mode != prev_mode:
            print(f"[MODE CHANGE] {prev_mode} → {self.mode}")
            self.last_mode_change = now

        return self.mode