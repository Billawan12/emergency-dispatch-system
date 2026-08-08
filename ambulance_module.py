"""
Emergency Dispatch System
File: ambulance_module.py

Purpose:
    Defines the Ambulance and AmbulanceManager classes.

Classes:
    Ambulance
        Represents an ambulance.

    AmbulanceManager
        Manages multiple ambulances.
"""


# ============================================================
# AMBULANCE CLASS
# ============================================================

class Ambulance:
    """
    Represents an ambulance.
    """

    VALID_STATUSES = {
        "available",
        "busy",
        "offline"
    }

    def __init__(
        self,
        ambulance_id,
        name,
        x,
        y,
        status="available",
        current_incident=None
    ):
        """
        Initialise an ambulance.
        """

        if not isinstance(ambulance_id, int):
            raise TypeError(
                "Ambulance ID must be an integer."
            )

        if not isinstance(name, str) or not name.strip():
            raise ValueError(
                "Ambulance name cannot be empty."
            )

        if not isinstance(x, (int, float)):
            raise TypeError(
                "x coordinate must be a number."
            )

        if not isinstance(y, (int, float)):
            raise TypeError(
                "y coordinate must be a number."
            )

        if isinstance(x, bool) or isinstance(y, bool):
            raise TypeError(
                "Coordinates must be numeric values."
            )

        if status not in self.VALID_STATUSES:
            raise ValueError(
                "Invalid ambulance status. "
                "Status must be available, busy, or offline."
            )

        if (
            current_incident is not None
            and not isinstance(current_incident, int)
        ):
            raise TypeError(
                "Current incident ID must be an integer or None."
            )

        self.id = ambulance_id
        self.name = name.strip()
        self.x = float(x)
        self.y = float(y)
        self.status = status
        self.current_incident = current_incident

    # --------------------------------------------------------
    # SET STATUS
    # --------------------------------------------------------

    def set_status(self, new_status):
        """
        Update the ambulance status.
        """

        if new_status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid ambulance status '{new_status}'. "
                "Valid statuses are: "
                "available, busy, offline."
            )

        self.status = new_status

        # If an ambulance becomes available or offline,
        # it should not retain a current incident.
        if new_status in {"available", "offline"}:
            self.current_incident = None

    # --------------------------------------------------------
    # GET LOCATION
    # --------------------------------------------------------

    def get_location(self):
        """Return ambulance coordinates as an (x, y) tuple."""

        return self.x, self.y

    # --------------------------------------------------------
    # IS AVAILABLE
    # --------------------------------------------------------

    def is_available(self):
        """Return True only when the ambulance is available."""

        return self.status == "available"

    # --------------------------------------------------------
    # STRING REPRESENTATION
    # --------------------------------------------------------

    def __str__(self):
        """Return a readable ambulance summary."""

        incident = (
            self.current_incident
            if self.current_incident is not None
            else "None"
        )

        return (
            f"Ambulance {self.id} | "
            f"{self.name} | "
            f"Location: ({self.x:.4f}, {self.y:.4f}) | "
            f"Status: {self.status} | "
            f"Incident: {incident}"
        )


# ============================================================
# AMBULANCE MANAGER CLASS
# ============================================================

class AmbulanceManager:
    """
    Manages a collection of Ambulance objects.
    """

    def __init__(self):
        """Initialise an empty ambulance list and ID counter."""

        self.ambulances = []
        self.next_id = 1

    # --------------------------------------------------------
    # ADD AMBULANCE
    # --------------------------------------------------------

    def add_ambulance(self, name, x, y):
        """
        Add a new ambulance.

        New ambulances are available by default.
        """

        if not isinstance(name, str) or not name.strip():
            raise ValueError(
                "Ambulance name cannot be empty."
            )

        if not isinstance(x, (int, float)):
            raise TypeError(
                "x coordinate must be a number."
            )

        if not isinstance(y, (int, float)):
            raise TypeError(
                "y coordinate must be a number."
            )

        ambulance = Ambulance(
            ambulance_id=self.next_id,
            name=name,
            x=x,
            y=y
        )

        self.ambulances.append(ambulance)
        self.next_id += 1

        return ambulance

    # --------------------------------------------------------
    # ADD MULTIPLE AMBULANCES
    # --------------------------------------------------------

    def add_multiple_ambulances(self, ambulance_list):
        """
        Add multiple ambulances.

        Expected format:

            [
                ("Ambulance 1", x, y),
                ("Ambulance 2", x, y)
            ]

        Returns:
            List of newly created ambulances.
        """

        if not isinstance(ambulance_list, (list, tuple)):
            raise TypeError(
                "ambulance_list must be a list or tuple."
            )

        created = []

        for ambulance_data in ambulance_list:

            if (
                not isinstance(ambulance_data, (list, tuple))
                or len(ambulance_data) != 3
            ):
                raise ValueError(
                    "Each ambulance must contain "
                    "name, x, and y."
                )

            name, x, y = ambulance_data

            ambulance = self.add_ambulance(
                name,
                x,
                y
            )

            created.append(ambulance)

        return created

    # --------------------------------------------------------
    # GET AMBULANCE BY ID
    # --------------------------------------------------------

    def get_ambulance_by_id(self, amb_id):
        """
        Retrieve an ambulance by ID.

        Returns None when the ambulance is not found.
        """

        for ambulance in self.ambulances:
            if ambulance.id == amb_id:
                return ambulance

        return None

    # --------------------------------------------------------
    # GET AVAILABLE AMBULANCES
    # --------------------------------------------------------

    def get_available_ambulances(self):
        """Return all available ambulances."""

        return [
            ambulance
            for ambulance in self.ambulances
            if ambulance.is_available()
        ]

    # --------------------------------------------------------
    # UPDATE STATUS
    # --------------------------------------------------------

    def update_status(self, amb_id, new_status):
        """
        Update an ambulance's status.
        """

        ambulance = self.get_ambulance_by_id(amb_id)

        if ambulance is None:
            raise ValueError(
                f"Ambulance {amb_id} was not found."
            )

        ambulance.set_status(new_status)

        return ambulance

    # --------------------------------------------------------
    # GET ALL AMBULANCES
    # --------------------------------------------------------

    def get_all_ambulances(self):
        """Return all ambulances."""

        return list(self.ambulances)

    # --------------------------------------------------------
    # STRING REPRESENTATION
    # --------------------------------------------------------

    def __str__(self):
        """
        Return a concise summary of all ambulances.
        """

        if not self.ambulances:
            return "No ambulances registered."

        lines = []

        for ambulance in self.ambulances:
            lines.append(
                f"Ambulance {ambulance.id} | "
                f"{ambulance.name} | "
                f"Status: {ambulance.status}"
            )

        return "\n".join(lines)


# ============================================================
# TEST CODE
# ============================================================

if __name__ == "__main__":

    print("=" * 65)
    print("AMBULANCE MODULE TESTS")
    print("=" * 65)

    manager = AmbulanceManager()

    # --------------------------------------------------------
    # Add ambulances
    # --------------------------------------------------------

    print("\n[1] Adding ambulances")

    ambulance1 = manager.add_ambulance(
        "Ambulance 1",
        -1.2921,
        36.8219
    )

    ambulance2 = manager.add_ambulance(
        "Ambulance 2",
        -1.3197,
        36.7073
    )

    ambulance3 = manager.add_ambulance(
        "Ambulance 3",
        -1.2765,
        36.8508
    )

    print(
        f"[OK] Added "
        f"{len(manager.get_all_ambulances())} ambulances"
    )

    # --------------------------------------------------------
    # Display all
    # --------------------------------------------------------

    print("\n[2] All ambulances")

    print(manager)

    # --------------------------------------------------------
    # Get location
    # --------------------------------------------------------

    print("\n[3] Location test")

    print(
        f"{ambulance1.name}: "
        f"{ambulance1.get_location()}"
    )

    # --------------------------------------------------------
    # Availability
    # --------------------------------------------------------

    print("\n[4] Availability test")

    print(
        f"Available ambulances: "
        f"{len(manager.get_available_ambulances())}"
    )

    # --------------------------------------------------------
    # Status update
    # --------------------------------------------------------

    print("\n[5] Status test")

    manager.update_status(1, "busy")

    print(ambulance1)

    manager.update_status(1, "available")

    print(ambulance1)

    # --------------------------------------------------------
    # Multiple ambulance addition
    # --------------------------------------------------------

    print("\n[6] Bulk addition test")

    manager.add_multiple_ambulances([
        ("Ambulance 4", -1.3000, 36.8000),
        ("Ambulance 5", -1.2800, 36.8300)
    ])

    print(
        f"Total ambulances: "
        f"{len(manager.get_all_ambulances())}"
    )

    # --------------------------------------------------------
    # Validation tests
    # --------------------------------------------------------

    print("\n[7] Validation tests")

    tests = [
        (
            "Empty name",
            lambda: manager.add_ambulance(
                "",
                -1.2,
                36.8
            )
        ),
        (
            "Invalid x",
            lambda: manager.add_ambulance(
                "Test",
                "invalid",
                36.8
            )
        ),
        (
            "Invalid y",
            lambda: manager.add_ambulance(
                "Test",
                -1.2,
                "invalid"
            )
        ),
        (
            "Invalid status",
            lambda: manager.update_status(
                1,
                "invalid"
            )
        ),
        (
            "Unknown ambulance",
            lambda: manager.update_status(
                999,
                "busy"
            )
        )
    ]

    for name, test in tests:

        try:
            test()
            print(f"[FAIL] {name}")
        except (ValueError, TypeError) as error:
            print(f"[PASS] {name}: {error}")

    print("\n" + "=" * 65)
    print("AMBULANCE MODULE TESTS COMPLETE")
    print("=" * 65)