import time


class TrafficSignal:

    def __init__(self):
        self.states = {
            1: "RED",
            2: "GREEN",
            3: "RED"
        }

        self.current_lane = 2
        self.last_change = time.time()

    # Get current signal state
    def get_state(self, lane_number):
        return self.states.get(
            lane_number,
            "RED"
        )

    # Change signal state
    def set_state(self, lane_number, state):

        if state not in [
            "RED",
            "YELLOW",
            "GREEN"
        ]:
            return False

        self.states[lane_number] = state

        return True

    # Set active green lane
    def set_green_lane(self, lane_number):

        for lane in self.states:

            if lane == lane_number:
                self.states[lane] = "GREEN"

            else:
                self.states[lane] = "RED"

        self.current_lane = lane_number
        self.last_change = time.time()

    # Get all signal states
    def get_all_states(self):
        return self.states.copy()