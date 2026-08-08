"""
Emergency Dispatch System
File: dispatch_module.py

Purpose:
    Provides ambulance dispatch and optimisation functionality.

    The optimizer uses a greedy Search-Based Software
    Engineering (SBSE) approach:

        1. Process incidents by priority.
        2. Find the nearest available ambulance.
        3. Assign the ambulance to the incident.
        4. Mark the ambulance as busy.

Classes:
    DispatchOptimizer
"""


import math
import time

from incident_module import IncidentManager
from ambulance_module import AmbulanceManager


# ============================================================
# DISPATCH OPTIMIZER
# ============================================================

class DispatchOptimizer:
    """
    Performs ambulance dispatch optimisation.
    """

    # Approximate location mapping.
    #
    # Coordinates are represented as:
    # (latitude, longitude)
    LOCATION_MAP = {
        # Nairobi
        "nairobi": (-1.2921, 36.8219),
        "langata": (-1.3676, 36.7460),
        "karen": (-1.3197, 36.7073),
        "eastleigh": (-1.2765, 36.8508),
        "westlands": (-1.2676, 36.8108),
        "kasarani": (-1.2226, 36.8976),
        "kibera": (-1.3133, 36.7870),
        "embakasi": (-1.3167, 36.9000),
        "thika road": (-1.2200, 36.8900),

        # Kenya
        "mombasa": (-4.0435, 39.6682),
        "kisumu": (-0.1022, 34.7617),
        "nakuru": (-0.3031, 36.0800),
        "eldoret": (0.5143, 35.2698),
        "malindi": (-3.2192, 40.1169),

        # East Africa
        "kampala": (0.3476, 32.5825),
        "entebbe": (0.0512, 32.4637),
        "dar es salaam": (-6.7924, 39.2083),
        "arusha": (-3.3869, 36.6830),
        "kigali": (-1.9441, 30.0619),
        "addis ababa": (9.0320, 38.7469)
    }

    # Priority weights used by the greedy dispatch strategy.
    PRIORITY_ORDER = {
        "high": 0,
        "medium": 1,
        "low": 2
    }

    # Approximate average speeds in kilometres per hour.
    ROAD_SPEEDS = {
        "good": 50.0,
        "normal": 40.0,
        "poor": 25.0,
        "bad": 15.0
    }

    # Approximate kilometres represented by one degree
    # of geographic coordinate distance.
    KM_PER_DEGREE = 111.0

    def __init__(self, ambulance_manager):
        """
        Initialise the optimizer with an AmbulanceManager.
        """

        if not isinstance(
            ambulance_manager,
            AmbulanceManager
        ):
            raise TypeError(
                "ambulance_manager must be an "
                "AmbulanceManager instance."
            )

        self.ambulance_manager = ambulance_manager
        self.incident_manager = None

    # --------------------------------------------------------
    # SET INCIDENT MANAGER
    # --------------------------------------------------------

    def set_incident_manager(self, incident_manager):
        """
        Link the optimizer to an IncidentManager.
        """

        if not isinstance(
            incident_manager,
            IncidentManager
        ):
            raise TypeError(
                "incident_manager must be an "
                "IncidentManager instance."
            )

        self.incident_manager = incident_manager

    # --------------------------------------------------------
    # CALCULATE DISTANCE
    # --------------------------------------------------------

    @staticmethod
    def calculate_distance(x1, y1, x2, y2):
        """
        Calculate Euclidean distance between two coordinate
        points.

        Returns distance in coordinate degrees.
        """

        coordinates = [x1, y1, x2, y2]

        if not all(
            isinstance(value, (int, float))
            for value in coordinates
        ):
            raise TypeError(
                "All coordinates must be numbers."
            )

        return math.sqrt(
            (x2 - x1) ** 2 +
            (y2 - y1) ** 2
        )

    # --------------------------------------------------------
    # DISTANCE IN KILOMETRES
    # --------------------------------------------------------

    @classmethod
    def distance_in_km(cls, distance_degrees):
        """
        Convert approximate geographic coordinate distance
        into kilometres.
        """

        return distance_degrees * cls.KM_PER_DEGREE

    # --------------------------------------------------------
    # GET LOCATION COORDINATES
    # --------------------------------------------------------

    def get_location_coordinates(self, location):
        """
        Convert a location description into coordinates.

        Known locations use LOCATION_MAP.

        Unknown locations use the required default:
            (1.0, 1.0)
        """

        if not isinstance(location, str):
            raise TypeError(
                "Location must be a string."
            )

        key = location.strip().lower()

        return self.LOCATION_MAP.get(
            key,
            (1.0, 1.0)
        )

    # --------------------------------------------------------
    # TRAVEL TIME
    # --------------------------------------------------------

    def calculate_travel_time(
        self,
        distance_degrees,
        road_condition="normal"
    ):
        """
        Estimate travel time in hours.

        Distance is converted approximately from coordinate
        degrees to kilometres before applying the speed.
        """

        road_condition = road_condition.lower()

        if road_condition not in self.ROAD_SPEEDS:
            raise ValueError(
                "Invalid road condition. "
                "Use good, normal, poor, or bad."
            )

        distance_km = self.distance_in_km(
            distance_degrees
        )

        speed = self.ROAD_SPEEDS[road_condition]

        return distance_km / speed

    # --------------------------------------------------------
    # FIND NEAREST AVAILABLE AMBULANCE
    # --------------------------------------------------------

    def find_nearest_available_ambulance(
        self,
        incident_x,
        incident_y,
        road_condition="normal"
    ):
        """
        Find the nearest available ambulance.

        Returns:
            (ambulance, distance, travel_time)

        If no ambulance is available:
            (None, None, None)
        """

        if not isinstance(
            incident_x,
            (int, float)
        ):
            raise TypeError(
                "Incident x coordinate must be numeric."
            )

        if not isinstance(
            incident_y,
            (int, float)
        ):
            raise TypeError(
                "Incident y coordinate must be numeric."
            )

        available = (
            self.ambulance_manager
            .get_available_ambulances()
        )

        if not available:
            return None, None, None

        nearest = None
        shortest_distance = float("inf")

        for ambulance in available:

            x, y = ambulance.get_location()

            distance = self.calculate_distance(
                incident_x,
                incident_y,
                x,
                y
            )

            if distance < shortest_distance:

                shortest_distance = distance
                nearest = ambulance

        travel_time = self.calculate_travel_time(
            shortest_distance,
            road_condition
        )

        return (
            nearest,
            shortest_distance,
            travel_time
        )

    # --------------------------------------------------------
    # ASSIGN AMBULANCE TO INCIDENT
    # --------------------------------------------------------

    def assign_ambulance_to_incident(
        self,
        incident_id,
        ambulance_id
    ):
        """
        Assign a specific ambulance to a specific incident.

        Keeps both objects synchronised.
        """

        if self.incident_manager is None:
            raise RuntimeError(
                "IncidentManager has not been set."
            )

        incident = (
            self.incident_manager
            .get_incident_by_id(incident_id)
        )

        if incident is None:
            raise ValueError(
                f"Incident {incident_id} was not found."
            )

        ambulance = (
            self.ambulance_manager
            .get_ambulance_by_id(ambulance_id)
        )

        if ambulance is None:
            raise ValueError(
                f"Ambulance {ambulance_id} was not found."
            )

        if not ambulance.is_available():
            raise ValueError(
                f"Ambulance {ambulance_id} is not available."
            )

        if incident.status != "new":
            raise ValueError(
                f"Incident {incident_id} is not new."
            )

        # Update incident.
        incident.assign_ambulance(
            ambulance.id
        )

        # Update ambulance.
        ambulance.status = "busy"
        ambulance.current_incident = incident.id

        return incident, ambulance

    # --------------------------------------------------------
    # FIND OPTIMAL AMBULANCE ASSIGNMENTS
    # --------------------------------------------------------

    def find_optimal_ambulance_assignments(
        self,
        incidents,
        road_condition="normal"
    ):
        """
        Assign available ambulances to incidents using a
        greedy SBSE strategy.

        Strategy:
            1. Sort by priority.
            2. For each incident, find the nearest available
               ambulance.
            3. Assign it.
            4. Continue until all incidents are processed
               or no ambulances remain.

        Returns a list of result dictionaries.
        """

        if self.incident_manager is None:
            raise RuntimeError(
                "IncidentManager has not been set."
            )

        if not isinstance(incidents, (list, tuple)):
            raise TypeError(
                "incidents must be a list or tuple."
            )

        # Only new incidents should be dispatched.
        dispatchable = [
            incident
            for incident in incidents
            if incident.status == "new"
        ]

        # Highest priority first.
        sorted_incidents = sorted(
            dispatchable,
            key=lambda incident: (
                self.PRIORITY_ORDER.get(
                    incident.priority,
                    99
                ),
                incident.id
            )
        )

        results = []

        for incident in sorted_incidents:

            incident_x, incident_y = (
                self.get_location_coordinates(
                    incident.location
                )
            )

            (
                ambulance,
                distance,
                travel_time
            ) = self.find_nearest_available_ambulance(
                incident_x,
                incident_y,
                road_condition
            )

            if ambulance is None:

                results.append({
                    "incident": incident,
                    "ambulance": None,
                    "distance": None,
                    "travel_time": None,
                    "status": "no_available_ambulance"
                })

                continue

            try:

                self.assign_ambulance_to_incident(
                    incident.id,
                    ambulance.id
                )

                results.append({
                    "incident": incident,
                    "ambulance": ambulance,
                    "distance": distance,
                    "travel_time": travel_time,
                    "status": "assigned"
                })

            except (ValueError, RuntimeError) as error:

                results.append({
                    "incident": incident,
                    "ambulance": None,
                    "distance": None,
                    "travel_time": None,
                    "status": f"assignment_failed: {error}"
                })

        return results

    # --------------------------------------------------------
    # RELEASE AMBULANCE
    # --------------------------------------------------------

    def release_ambulance(self, ambulance_id):
        """
        Release an ambulance and make it available again.

        If the ambulance was assigned to an incident, the
        incident's ambulance reference is cleared.

        The incident itself is not automatically closed.
        """

        ambulance = (
            self.ambulance_manager
            .get_ambulance_by_id(ambulance_id)
        )

        if ambulance is None:
            raise ValueError(
                f"Ambulance {ambulance_id} was not found."
            )

        incident_id = ambulance.current_incident

        if (
            incident_id is not None
            and self.incident_manager is not None
        ):

            incident = (
                self.incident_manager
                .get_incident_by_id(incident_id)
            )

            if incident is not None:
                incident.assigned_ambulance = None

        ambulance.status = "available"
        ambulance.current_incident = None

        return ambulance


# ============================================================
# TEST CODE
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("DISPATCH MODULE TESTS")
    print("=" * 70)

    ambulance_manager = AmbulanceManager()
    incident_manager = IncidentManager()

    # --------------------------------------------------------
    # Add sample ambulances
    # --------------------------------------------------------

    ambulance_manager.add_multiple_ambulances([
        ("Ambulance 1", -1.2921, 36.8219),
        ("Ambulance 2", -1.3197, 36.7073),
        ("Ambulance 3", -1.2765, 36.8508)
    ])

    # --------------------------------------------------------
    # Add sample incidents
    # --------------------------------------------------------

    incident_manager.create_incident(
        "Nairobi",
        "Major accident",
        "high"
    )

    incident_manager.create_incident(
        "Karen",
        "Medical emergency",
        "medium"
    )

    incident_manager.create_incident(
        "Eastleigh",
        "Building collapse",
        "high"
    )

    incident_manager.create_incident(
        "Langata",
        "Minor accident",
        "low"
    )

    optimizer = DispatchOptimizer(
        ambulance_manager
    )

    optimizer.set_incident_manager(
        incident_manager
    )

    # --------------------------------------------------------
    # Location mapping test
    # --------------------------------------------------------

    print("\n[1] Location mapping")

    for location in [
        "Nairobi",
        "Karen",
        "Langata",
        "Eastleigh",
        "Mombasa",
        "Kampala",
        "Unknown Location"
    ]:

        coordinates = (
            optimizer.get_location_coordinates(
                location
            )
        )

        print(
            f"{location:<20} -> {coordinates}"
        )

    # --------------------------------------------------------
    # Nearest ambulance test
    # --------------------------------------------------------

    print("\n[2] Nearest ambulance search")

    x, y = optimizer.get_location_coordinates(
        "Nairobi"
    )

    start = time.perf_counter()

    ambulance, distance, travel_time = (
        optimizer.find_nearest_available_ambulance(
            x,
            y,
            "good"
        )
    )

    elapsed = time.perf_counter() - start

    if ambulance is not None:

        print(
            f"Nearest: {ambulance.name}"
        )

        print(
            f"Distance: {distance:.4f} degrees"
        )

        print(
            f"Travel time: {travel_time:.4f} hours"
        )

    else:

        print("No available ambulance.")

    print(
        f"Search time: {elapsed:.6f} seconds"
    )

    # --------------------------------------------------------
    # Multiple assignment test
    # --------------------------------------------------------

    print("\n[3] Optimal assignment")

    start = time.perf_counter()

    results = (
        optimizer.find_optimal_ambulance_assignments(
            incident_manager.get_new_incidents(),
            road_condition="good"
        )
    )

    elapsed = time.perf_counter() - start

    for result in results:

        incident = result["incident"]
        ambulance = result["ambulance"]

        if ambulance is not None:

            print(
                f"Incident {incident.id} "
                f"({incident.priority}) -> "
                f"{ambulance.name}"
            )

        else:

            print(
                f"Incident {incident.id} "
                f"({incident.priority}) -> "
                f"{result['status']}"
            )

    print(
        f"Assignment search time: "
        f"{elapsed:.6f} seconds"
    )

    # --------------------------------------------------------
    # State consistency
    # --------------------------------------------------------

    print("\n[4] State consistency")

    for incident in incident_manager.get_all_incidents():

        print(
            f"Incident {incident.id}: "
            f"{incident.status}, "
            f"Ambulance={incident.assigned_ambulance}"
        )

    for ambulance in ambulance_manager.get_all_ambulances():

        print(
            f"Ambulance {ambulance.id}: "
            f"{ambulance.status}, "
            f"Incident={ambulance.current_incident}"
        )

    # --------------------------------------------------------
    # No available ambulance test
    # --------------------------------------------------------

    print("\n[5] No available ambulance test")

    extra_incident = incident_manager.create_incident(
        "Kampala",
        "Test emergency",
        "high"
    )

    # All ambulances should currently be busy.
    nearest = (
        optimizer.find_nearest_available_ambulance(
            *optimizer.get_location_coordinates("Kampala")
        )
    )

    print(
        "Result:",
        "No ambulance available"
        if nearest[0] is None
        else nearest[0].name
    )

    # --------------------------------------------------------
    # Unknown location test
    # --------------------------------------------------------

    print("\n[6] Unknown location test")

    unknown = (
        optimizer.get_location_coordinates(
            "Unknown Place"
        )
    )

    print(
        f"Unknown location coordinates: {unknown}"
    )

    # --------------------------------------------------------
    # Release test
    # --------------------------------------------------------

    print("\n[7] Ambulance release test")

    busy_ambulances = [
        ambulance
        for ambulance
        in ambulance_manager.get_all_ambulances()
        if ambulance.status == "busy"
    ]

    if busy_ambulances:

        released = optimizer.release_ambulance(
            busy_ambulances[0].id
        )

        print(
            f"[OK] Released {released.name}"
        )

        print(
            f"Status: {released.status}"
        )

        print(
            f"Current incident: "
            f"{released.current_incident}"
        )

    # --------------------------------------------------------
    # Invalid road condition
    # --------------------------------------------------------

    print("\n[8] Invalid road condition test")

    try:

        optimizer.calculate_travel_time(
            1.0,
            "invalid"
        )

        print("[FAIL] Invalid road condition accepted.")

    except ValueError as error:

        print(f"[PASS] {error}")

    print("\n" + "=" * 70)
    print("DISPATCH MODULE TESTS COMPLETE")
    print("=" * 70)