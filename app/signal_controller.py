class AdaptiveSignalController:
    """
    Adaptive traffic signal controller.

    Determines green-signal duration for each lane based
    on the detected traffic density.

    This is a simulation/decision-support component.
    It does NOT directly control a physical traffic signal.
    """

    def __init__(self,
                 minimum_green = 15,
                 maximum_green = 60,
                 yellow_time = 5,
                 all_red_time = 2   ):

        self.minimum_green = minimum_green
        self.maximum_green = maximum_green
        self.yellow_time = yellow_time
        self.all_red_time = all_red_time

    # ========================================================
    # CALCULATE GREEN TIME
    # ========================================================

    def calculate_green_time(self,
                             vehicle_count,
                             density_score  ):
        """
        Calculate green time using traffic density.

        Higher traffic density receives more green time.
        """

        # Convert density score from 0–100
        # into the configured signal range.

        green_time = (self.minimum_green +
                      (density_score / 100) * (self.maximum_green - self.minimum_green))

        # Add a small influence from actual
        # vehicle count.

        if vehicle_count >= 10:
            green_time += 5

        elif vehicle_count >= 5:
            green_time += 2

        # Keep within safe configured range.

        green_time = min(green_time, self.maximum_green)
        green_time = max(green_time, self.minimum_green)

        return int(round(green_time))

    # ========================================================
    # DETERMINE PRIORITY
    # ========================================================

    @staticmethod
    def get_priority(density_score):
        """
        Determine signal priority from density.
        """

        if density_score >= 75:
            return "VERY HIGH"

        elif density_score >= 50:
            return "HIGH"

        elif density_score >= 25:
            return "MEDIUM"

        else:
            return "LOW"

    # ========================================================
    # GENERATE SIGNAL PLAN
    # ========================================================

    def generate_signal_plan(self, lane_data):
        """
        Generate an adaptive signal plan for all lanes.
        """

        signal_plan = {}

        for lane_number, data in lane_data.items():

            vehicle_count = data["vehicle_count"]
            density = data["density"]

            # Convert lane density category
            # into a numerical score.

            density_score = (self.density_to_score(density))

            green_time = (self.calculate_green_time(vehicle_count,density_score))

            priority = (self.get_priority(density_score))

            signal_plan[lane_number] = {
                                            "vehicle_count":vehicle_count,
                                            "density":density,
                                            "density_score":density_score,
                                            "green_time":green_time,
                                            "yellow_time":self.yellow_time,
                                            "all_red_time":self.all_red_time,
                                            "priority":priority
                                        }

        return signal_plan

    # ========================================================
    # DENSITY CATEGORY → SCORE
    # ========================================================

    @staticmethod
    def density_to_score(density):

        mapping = {
                    "LOW": 20,
                    "MEDIUM": 45,
                    "HIGH": 70,
                    "SEVERE": 90
                  }

        return mapping.get(density.upper(), 20)

    # ========================================================
    # SELECT NEXT LANE
    # ========================================================

    @staticmethod
    def select_priority_lane(signal_plan):
        """
        Select the lane with the highest traffic priority.
        """

        if not signal_plan:
            return None

        priority_lane = max(signal_plan.items(),
                            key=lambda item:
                                item[1]["density_score"]
                           )

        return priority_lane[0]

    # ========================================================
    # COMPLETE DECISION
    # ========================================================

    def decide(self, lane_data):
        """
        Generate complete adaptive signal decision.
        """

        signal_plan = (self.generate_signal_plan(lane_data))
        priority_lane = (self.select_priority_lane(signal_plan))

        return {
                "signal_plan":signal_plan,
                "priority_lane":priority_lane
               }