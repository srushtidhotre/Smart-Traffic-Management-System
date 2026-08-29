class EmergencyVehicleDetector:

    def __init__(self):
        self.emergency_classes = {
            "ambulance",
            "fire truck",
            "fire_truck",
            "firetruck",
            "police",
            "police car",
            "police_car"
        }

    # Check whether vehicle is an emergency vehicle
    def is_emergency_vehicle(self, vehicle_class):

        if not vehicle_class:
            return False

        vehicle_class = (
            vehicle_class
            .lower()
            .strip()
        )

        return (
            vehicle_class
            in self.emergency_classes
        )

    # Get emergency vehicle type
    def get_emergency_type(self, vehicle_class):

        if not self.is_emergency_vehicle(
            vehicle_class
        ):
            return None

        vehicle_class = (
            vehicle_class
            .lower()
            .strip()
        )

        if "ambulance" in vehicle_class:
            return "Ambulance"

        if "fire" in vehicle_class:
            return "Fire Truck"

        if "police" in vehicle_class:
            return "Police Vehicle"

        return "Emergency Vehicle"

    # Find emergency vehicles
    def detect(self, tracks):

        emergency_vehicles = []

        for track in tracks:

            vehicle_class = track.get(
                "class_name",
                ""
            )

            if self.is_emergency_vehicle(
                vehicle_class
            ):

                emergency_vehicles.append(
                    track
                )

        return emergency_vehicles