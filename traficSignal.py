import random
import time

# 🛑 Simple Traffic Signal Simulation
# Run this file as: python trafficSignal_simple.py

# ---------------- CONSTANTS ----------------
MIN_GREEN = 5        # Minimum time ek side green rahegi
YELLOW_TIME = 2      # Yellow light time
CAR_PASS_PER_TICK = 1  # Ek tick mein kitni car pass hoti hai
ARRIVAL_PROB = 0.6   # Har tick par car aane ki probability
MAX_WAIT = 8         # Max waiting time allowed
THRESHOLD = 3        # Queue difference jisme signal change hoga

# ---------------- SIGNAL CLASS ----------------
class TrafficSignal:
    def __init__(self):
        self.state = "NS_GREEN"             # Start North-South green
        self.time_in_state = 0
        self.next_state_after_yellow = "EW_GREEN"

    def set_state(self, new_state):
        self.state = new_state
        self.time_in_state = 0

    def step(self):
        self.time_in_state += 1

# ---------------- REFLEX AGENT ----------------
class ReflexAgent:
    def decide(self, sensors, signal):
        q_ns = sensors['queue_ns']
        q_ew = sensors['queue_ew']
        wait_ns = sensors['wait_ns']
        wait_ew = sensors['wait_ew']

        # Agar signal yellow hai
        if signal.state == "YELLOW":
            if signal.time_in_state >= YELLOW_TIME:
                return signal.next_state_after_yellow
            return "YELLOW"

        # Agar green minimum time complete nahi hua
        if signal.time_in_state < MIN_GREEN:
            return signal.state

        # North-South green hai abhi
        if signal.state == "NS_GREEN":
            if wait_ew >= MAX_WAIT or (q_ew - q_ns) >= THRESHOLD:
                signal.next_state_after_yellow = "EW_GREEN"
                return "YELLOW"
            return "NS_GREEN"

        # East-West green hai abhi
        if signal.state == "EW_GREEN":
            if wait_ns >= MAX_WAIT or (q_ns - q_ew) >= THRESHOLD:
                signal.next_state_after_yellow = "NS_GREEN"
                return "YELLOW"
            return "EW_GREEN"

        return signal.state

# ---------------- SIMULATION FUNCTION ----------------
def simulate(steps=50, seed=42):
    random.seed(seed)
    queue_ns = 0
    queue_ew = 0

    signal = TrafficSignal()
    agent = ReflexAgent()

    for t in range(1, steps + 1):
        # Random car arrivals
        if random.random() < ARRIVAL_PROB:
            queue_ns += 1
        if random.random() < ARRIVAL_PROB:
            queue_ew += 1

        # Approx waiting time = queue length
        wait_ns = queue_ns
        wait_ew = queue_ew

        sensors = {
            'queue_ns': queue_ns,
            'queue_ew': queue_ew,
            'wait_ns': wait_ns,
            'wait_ew': wait_ew
        }

        # Agent decision
        action = agent.decide(sensors, signal)

        # Update signal state
        if action == "YELLOW" and signal.state != "YELLOW":
            signal.set_state("YELLOW")
        elif action in ("NS_GREEN", "EW_GREEN"):
            signal.set_state(action)

        # Cars pass during green light
        if signal.state == "NS_GREEN":
            passed = min(CAR_PASS_PER_TICK, queue_ns)
            queue_ns -= passed
        elif signal.state == "EW_GREEN":
            passed = min(CAR_PASS_PER_TICK, queue_ew)
            queue_ew -= passed

        signal.step()

        # Print status
        print(f"t={t:03d} | State={signal.state:9} | NS_Q={queue_ns:2d} | EW_Q={queue_ew:2d} | Next={signal.next_state_after_yellow} | Time={signal.time_in_state}")

        # Optional slow print
        # time.sleep(0.1)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    simulate(steps=50)
