"""
Emergency Dispatch System
File: incident_module.py

Purpose:
    Defines the Incident and IncidentManager classes.

Classes:
    Incident
        Represents a single emergency incident.

    IncidentManager
        Manages multiple incidents.
"""


from datetime import datetime


# ============================================================
# INCIDENT CLASS
# ============================================================

class Incident:
    """
    Represents an emergency incident.
    """

    VALID_PRIORITIES = {"high", "medium", "low"}

    VALID_STATUSES = {
        "new",
        "assigned",
        "en_route",
        "on_scene",
        "closed"
    }

    # Valid incident lifecycle transitions.
    VALID_TRANSITIONS = {
        "new": {"assigned", "closed"},
        "assigned": {"en_route", "closed"},
        "en_route": {"on_scene", "closed"},
        "on_scene": {"closed"},
        "closed": set()
    }

    def __init__(
        self,
        incident_id,
        location,
        description,
        priority,
        status="new",
        timestamp=None,
        assigned_ambulance=None
    ):
        """
        Initialise an incident.

        Parameters:
            incident_id (int):
                Unique incident ID.

            location (str):
                Incident location.

            description (str):
                Description of the incident.

            priority (str):
                high, medium, or low.

            status (str):
                new, assigned, en_route, on_scene, or closed.

            timestamp (datetime):
                Time the incident was created.

            assigned_ambulance (int or None):
                ID of the assigned ambulance.
        """

        # Validate basic fields.
        if not isinstance(incident_id, int):
            raise TypeError("Incident ID must be an integer.")

        if not isinstance(location, str) or not location.strip():
            raise ValueError("Location cannot be empty.")

        if (
            not isinstance(description, str)
            or not description.strip()
        ):
            raise ValueError("Description cannot be empty.")

        # Validate priority.
        priority = priority.lower() if isinstance(priority, str) else priority

        if priority not in self.VALID_PRIORITIES:
            raise ValueError(
                "Invalid priority. "
                "Priority must be high, medium, or low."
            )

        # Validate status.
        if status not in self.VALID_STATUSES:
            raise ValueError(
                "Invalid status. "
                "Status must be new, assigned, en_route, "
                "on_scene, or closed."
            )

        self.id = incident_id
        self.location = location.strip()
        self.description = description.strip()
        self.priority = priority
        self.status = status
        self.timestamp = (
            timestamp
            if timestamp is not None
            else datetime.now()
        )
        self.assigned_ambulance = assigned_ambulance

    # --------------------------------------------------------
    # GET DETAILS
    # --------------------------------------------------------

    def get_details(self):
        """
        Return a formatted string containing all
        incident information.
        """

        ambulance = (
            self.assigned_ambulance
            if self.assigned_ambulance is not None
            else "None"
        )

        return (
            "\n"
            "================ INCIDENT DETAILS ================\n"
            f"Incident ID       : {self.id}\n"
            f"Location          : {self.location}\n"
            f"Description       : {self.description}\n"
            f"Priority          : {self.priority}\n"
            f"Status            : {self.status}\n"
            f"Timestamp         : {self.timestamp}\n"
            f"Assigned Ambulance: {ambulance}\n"
            "===================================================="
        )

    # --------------------------------------------------------
    # ASSIGN AMBULANCE
    # --------------------------------------------------------

    def assign_ambulance(self, ambulance_id):
        """
        Assign an ambulance to the incident.

        The incident status changes to 'assigned'.
        """

        if not isinstance(ambulance_id, int):
            raise TypeError(
                "Ambulance ID must be an integer."
            )

        if self.status != "new":
            raise ValueError(
                "An ambulance can only be assigned to a "
                "new incident."
            )

        self.assigned_ambulance = ambulance_id
        self.status = "assigned"

    # --------------------------------------------------------
    # UPDATE STATUS
    # --------------------------------------------------------

    def update_status(self, new_status):
        """
        Update the incident status.

        Only valid statuses and valid lifecycle transitions
        are allowed.
        """

        if new_status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid status '{new_status}'. "
                "Valid statuses are: "
                "new, assigned, en_route, on_scene, closed."
            )

        if new_status == self.status:
            return

        allowed = self.VALID_TRANSITIONS[self.status]

        if new_status not in allowed:
            raise ValueError(
                f"Invalid status transition: "
                f"{self.status} -> {new_status}."
            )

        self.status = new_status

    def __str__(self):
        """Return a concise incident summary."""

        ambulance = (
            self.assigned_ambulance
            if self.assigned_ambulance is not None
            else "None"
        )

        return (
            f"Incident {self.id} | "
            f"{self.location} | "
            f"{self.priority} | "
            f"{self.status} | "
            f"Ambulance: {ambulance}"
        )


# ============================================================
# INCIDENT MANAGER CLASS
# ============================================================

class IncidentManager:
    """
    Manages a collection of Incident objects.
    """

    def __init__(self):
        """Initialise an empty incident list and ID counter."""

        self.incidents = []
        self.next_id = 1

    # --------------------------------------------------------
    # CREATE INCIDENT
    # --------------------------------------------------------

    def create_incident(
        self,
        location,
        description,
        priority
    ):
        """
        Create and store a new incident.

        The Incident class performs the detailed validation.
        """

        if not isinstance(location, str) or not location.strip():
            raise ValueError(
                "Location cannot be empty."
            )

        if (
            not isinstance(description, str)
            or not description.strip()
        ):
            raise ValueError(
                "Description cannot be empty."
            )

        if not isinstance(priority, str):
            raise TypeError(
                "Priority must be a string."
            )

        incident = Incident(
            incident_id=self.next_id,
            location=location,
            description=description,
            priority=priority
        )

        self.incidents.append(incident)
        self.next_id += 1

        return incident

    # --------------------------------------------------------
    # GET INCIDENT BY ID
    # --------------------------------------------------------

    def get_incident_by_id(self, incident_id):
        """
        Retrieve an incident by ID.

        Returns:
            Incident if found.
            None if not found.
        """

        for incident in self.incidents:
            if incident.id == incident_id:
                return incident

        return None

    # --------------------------------------------------------
    # GET ALL INCIDENTS
    # --------------------------------------------------------

    def get_all_incidents(self):
        """Return all incidents."""

        return list(self.incidents)

    # --------------------------------------------------------
    # GET ACTIVE INCIDENTS
    # --------------------------------------------------------

    def get_active_incidents(self):
        """
        Return incidents that are not closed.
        """

        return [
            incident
            for incident in self.incidents
            if incident.status != "closed"
        ]

    # --------------------------------------------------------
    # GET NEW INCIDENTS
    # --------------------------------------------------------

    def get_new_incidents(self):
        """
        Return incidents that have not yet been dispatched.
        """

        return [
            incident
            for incident in self.incidents
            if incident.status == "new"
        ]

    # --------------------------------------------------------
    # GET TOTAL INCIDENTS
    # --------------------------------------------------------

    def get_total_incidents(self):
        """Return the total number of incidents."""

        return len(self.incidents)

    # --------------------------------------------------------
    # GET ACTIVE INCIDENT COUNT
    # --------------------------------------------------------

    def get_active_incident_count(self):
        """Return the number of incidents that are not closed."""

        return len(self.get_active_incidents())

    # --------------------------------------------------------
    # DELETE INCIDENT
    # --------------------------------------------------------

    def delete_incident(self, incident_id):
        """
        Delete an incident by ID.

        Active assigned incidents should not be deleted because
        doing so could leave an ambulance pointing to an
        incident that no longer exists.

        Returns:
            True if deleted.

        Raises:
            ValueError if incident does not exist or is active.
        """

        incident = self.get_incident_by_id(incident_id)

        if incident is None:
            raise ValueError(
                f"Incident {incident_id} was not found."
            )

        if incident.status != "closed":
            raise ValueError(
                "Only closed incidents can be deleted."
            )

        self.incidents.remove(incident)
        return True


# ============================================================
# TEST CODE
# ============================================================

if __name__ == "__main__":

    print("=" * 65)
    print("INCIDENT MODULE TESTS")
    print("=" * 65)

    manager = IncidentManager()

    # --------------------------------------------------------
    # Create sample incidents
    # --------------------------------------------------------

    print("\n[1] Creating sample incidents")

    incident1 = manager.create_incident(
        "Nairobi",
        "Major road accident",
        "high"
    )

    incident2 = manager.create_incident(
        "Karen",
        "Medical emergency",
        "medium"
    )

    incident3 = manager.create_incident(
        "Eastleigh",
        "Building collapse",
        "high"
    )

    print(f"[OK] Created {manager.get_total_incidents()} incidents")

    # --------------------------------------------------------
    # Display concise summaries
    # --------------------------------------------------------

    print("\n[2] All incidents")

    for incident in manager.get_all_incidents():
        print(incident)

    # --------------------------------------------------------
    # Retrieve by ID
    # --------------------------------------------------------

    print("\n[3] Retrieve incident by ID")

    found = manager.get_incident_by_id(1)

    if found:
        print(found.get_details())

    missing = manager.get_incident_by_id(999)

    print(
        f"Missing incident result: {missing}"
    )

    # --------------------------------------------------------
    # Assignment and lifecycle
    # --------------------------------------------------------

    print("\n[4] Test incident lifecycle")

    incident1.assign_ambulance(1)
    print(f"[OK] {incident1}")

    incident1.update_status("en_route")
    print(f"[OK] {incident1}")

    incident1.update_status("on_scene")
    print(f"[OK] {incident1}")

    incident1.update_status("closed")
    print(f"[OK] {incident1}")

    # --------------------------------------------------------
    # Active incidents
    # --------------------------------------------------------

    print("\n[5] Active incidents")

    for incident in manager.get_active_incidents():
        print(incident)

    print(
        f"Active count: "
        f"{manager.get_active_incident_count()}"
    )

    # --------------------------------------------------------
    # New incidents
    # --------------------------------------------------------

    print("\n[6] New incidents")

    for incident in manager.get_new_incidents():
        print(incident)

    # --------------------------------------------------------
    # Error handling
    # --------------------------------------------------------

    print("\n[7] Validation tests")

    tests = [
        (
            "Empty location",
            lambda: manager.create_incident(
                "",
                "Test description",
                "low"
            )
        ),
        (
            "Empty description",
            lambda: manager.create_incident(
                "Nairobi",
                "",
                "low"
            )
        ),
        (
            "Invalid priority",
            lambda: manager.create_incident(
                "Nairobi",
                "Test description",
                "urgent"
            )
        ),
        (
            "Invalid status",
            lambda: incident2.update_status("invalid")
        ),
        (
            "Invalid lifecycle transition",
            lambda: incident2.update_status("closed")
        )
    ]

    for name, test in tests:

        try:
            test()
            print(f"[FAIL] {name}")
        except (ValueError, TypeError) as error:
            print(f"[PASS] {name}: {error}")

    print("\n" + "=" * 65)
    print("INCIDENT MODULE TESTS COMPLETE")
    print("=" * 65)