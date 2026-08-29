from typing import Dict

class TrafficDensityAnalyzer:
    """
    Calculates overall traffic density and congestion level
    using lane-wise vehicle information.

    The model is intentionally modular so that the thresholds
    can later be calibrated using real traffic data.
    """

    def __init__(self,
                 low_threshold = 25,
                 moderate_threshold = 50,
                 high_threshold = 75        ):
        
        self.low_threshold = low_threshold
        self.moderate_threshold = moderate_threshold
        self.high_threshold = high_threshold

    # ========================================================
    # CALCULATE LANE SCORE
    # ========================================================

    @staticmethod
    def calculate_lane_score(vehicle_count):
        """
        Convert vehicle count into a normalized 0–100 score.

        Initial assumption:
        0 vehicles  -> 0
        15+ vehicles -> 100

        This can later be calibrated using actual road capacity.
        """

        MAX_VEHICLES_PER_LANE = 15

        score = (vehicle_count / MAX_VEHICLES_PER_LANE) * 100

        return min(max(score, 0), 100)

    # ========================================================
    # CALCULATE OVERALL SCORE
    # ========================================================

    def calculate_density_score(self, lane_data: Dict):
        """
        Calculate weighted overall traffic-density score.

        Heavily congested lanes receive more influence than
        lightly occupied lanes.
        """

        if not lane_data:
            return 0.0

        lane_scores = []

        for lane_number, data in lane_data.items():
            vehicle_count = data["vehicle_count"]
            score = self.calculate_lane_score(vehicle_count)
            lane_scores.append(score)

        # Average lane score
        average_score = (sum(lane_scores) / len(lane_scores))

        return round(average_score, 2)

    # ========================================================
    # DETERMINE CONGESTION LEVEL
    # ========================================================

    def get_congestion_level(self, density_score):
        """
        Convert numerical density score
        into a traffic condition.
        """

        if density_score <= self.low_threshold:
            return "LOW"

        elif density_score <= self.moderate_threshold:
            return "MODERATE"

        elif density_score <= self.high_threshold:
            return "HIGH"

        else:
            return "SEVERE"

    # ========================================================
    # FIND MOST CONGESTED LANE
    # ========================================================

    @staticmethod
    def get_most_congested_lane(lane_data):

        if not lane_data:
            return None

        most_congested = max(
                                lane_data.items(),

                                key=lambda item:
                                    item[1]["vehicle_count"]
                            )

        return most_congested[0]

    # ========================================================
    # COMPLETE ANALYSIS
    # ========================================================

    def analyze(self, lane_data):
        """
        Perform complete traffic-density analysis.
        """

        density_score = (self.calculate_density_score(lane_data))

        congestion_level = (self.get_congestion_level(density_score))

        most_congested_lane = (self.get_most_congested_lane(lane_data))

        total_vehicles = sum(data["vehicle_count"]
                            for data in lane_data.values())

        return {
                "total_vehicles":total_vehicles,
                "density_score":density_score,
                "congestion_level":congestion_level,
                "most_congested_lane":most_congested_lane
                }