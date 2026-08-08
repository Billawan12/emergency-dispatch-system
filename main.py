"""
Emergency Dispatch System
File: main.py

Purpose:
    Provides the interactive command-line interface and
    integrates the IncidentManager, AmbulanceManager,
    and DispatchOptimizer.
"""


from incident_module import IncidentManager
from ambulance_module import AmbulanceManager
from dispatch_module import DispatchOptimizer


# ============================================================
# MENU
# ============================================================

def display_menu():
    """Display the main menu."""

    print("\n" + "=" * 60)
    print("EMERGENCY DISPATCH SYSTEM")
    print("=" * 60)
    print("1. Report a new incident")
    print("2. View all incidents")
    print("3. View available ambulances")
    print("4. Run dispatch")
    print("5. Exit")
    print("=" * 60)


# ============================================================
# REPORT INCIDENT
# ============================================================

def report_incident(incident_manager):
    """Create an incident from user input."""

    print("\n" + "-" * 60)
    print("REPORT NEW INCIDENT")
    print("-" * 60)

    try:

        location = input(
            "Location: "
        ).strip()

        description = input(
            "Description: "
        ).strip()

        priority = input(
            "Priority (high/medium/low): "
        ).strip().lower()

        incident = incident_manager.create_incident(
            location,
            description,
            priority
        )

        print("\n[OK] Incident created.")
        print(f"ID       : {incident.id}")
        print(f"Location : {incident.location}")
        print(f"Priority : {incident.priority}")
        print(f"Status   : {incident.status}")

    except (ValueError, TypeError) as error:

        print(f"\n[ERROR] {error}")

    except (EOFError, KeyboardInterrupt):

        print("\n[ERROR] Incident entry cancelled.")

    except Exception as error:

        print(
            f"\n[ERROR] Unable to create incident: "
            f"{error}"
        )


# ============================================================
# VIEW INCIDENTS
# ============================================================

def view_all_incidents(incident_manager):
    """Display all incidents."""

    print("\n" + "-" * 60)
    print("ALL INCIDENTS")
    print("-" * 60)

    try:

        incidents = (
            incident_manager.get_all_incidents()
        )

        if not incidents:

            print("No incidents recorded.")
            return

        print(
            f"{'ID':<5}"
            f"{'Location':<15}"
            f"{'Priority':<10}"
            f"{'Status':<12}"
            f"{'Ambulance'}"
        )

        print("-" * 60)

        for incident in incidents:

            ambulance = (
                incident.assigned_ambulance
                if incident.assigned_ambulance is not None
                else "None"
            )

            print(
                f"{incident.id:<5}"
                f"{incident.location:<15}"
                f"{incident.priority:<10}"
                f"{incident.status:<12}"
                f"{ambulance}"
            )

    except Exception as error:

        print(
            f"[ERROR] Unable to display incidents: "
            f"{error}"
        )


# ============================================================
# VIEW AVAILABLE AMBULANCES
# ============================================================

def view_available_ambulances(ambulance_manager):
    """Display available ambulances."""

    print("\n" + "-" * 60)
    print("AVAILABLE AMBULANCES")
    print("-" * 60)

    try:

        ambulances = (
            ambulance_manager
            .get_available_ambulances()
        )

        if not ambulances:

            print(
                "No ambulances are currently available."
            )
            return

        for ambulance in ambulances:

            x, y = ambulance.get_location()

            print(
                f"Ambulance {ambulance.id} | "
                f"{ambulance.name} | "
                f"Location: "
                f"({x:.4f}, {y:.4f}) | "
                f"Status: {ambulance.status}"
            )

    except Exception as error:

        print(
            f"[ERROR] Unable to display ambulances: "
            f"{error}"
        )


# ============================================================
# RUN DISPATCH
# ============================================================

def run_dispatch(
    incident_manager,
    ambulance_manager,
    optimizer
):
    """
    Dispatch only NEW incidents.

    This prevents already-assigned incidents from being
    assigned repeatedly if the user selects Run Dispatch
    more than once.
    """

    print("\n" + "-" * 60)
    print("DISPATCH OPTIMISATION")
    print("-" * 60)

    try:

        # Only new incidents need an initial dispatch.
        incidents = (
            incident_manager.get_new_incidents()
        )

        if not incidents:

            print(
                "No new incidents require dispatch."
            )
            return

        available = (
            ambulance_manager
            .get_available_ambulances()
        )

        if not available:

            print(
                "No ambulances are currently available."
            )
            return

        print(
            f"New incidents: {len(incidents)}"
        )

        print(
            f"Available ambulances: "
            f"{len(available)}"
        )

        results = (
            optimizer
            .find_optimal_ambulance_assignments(
                incidents,
                road_condition="normal"
            )
        )

        print("\nAssignment Results:")
        print("-" * 60)

        for result in results:

            incident = result["incident"]
            ambulance = result["ambulance"]

            x, y = (
                optimizer.get_location_coordinates(
                    incident.location
                )
            )

            print(
                f"Incident {incident.id} | "
                f"{incident.location}"
            )

            print(
                f"  Coordinates: "
                f"({x:.4f}, {y:.4f})"
            )

            print(
                f"  Priority: "
                f"{incident.priority}"
            )

            if ambulance is not None:

                print(
                    f"  Ambulance: "
                    f"{ambulance.name}"
                )

                print(
                    f"  Distance: "
                    f"{result['distance']:.4f} degrees"
                )

                print(
                    f"  Travel time: "
                    f"{result['travel_time']:.4f} hours"
                )

                print(
                    f"  Status: "
                    f"{incident.status}"
                )

            else:

                print(
                    "  Ambulance: None"
                )

                print(
                    f"  Result: "
                    f"{result['status']}"
                )

            print("-" * 60)

    except (ValueError, TypeError, RuntimeError) as error:

        print(
            f"\n[ERROR] Dispatch failed: {error}"
        )

    except Exception as error:

        print(
            f"\n[ERROR] Unexpected dispatch error: "
            f"{error}"
        )


# ============================================================
# SAMPLE DATA
# ============================================================

def create_sample_data(
    incident_manager,
    ambulance_manager
):
    """
    Create demonstration data required by I1.
    """

    ambulance_manager.add_multiple_ambulances([
        (
            "Ambulance 1",
            -1.2921,
            36.8219
        ),
        (
            "Ambulance 2",
            -1.3197,
            36.7073
        ),
        (
            "Ambulance 3",
            -1.2765,
            36.8508
        )
    ])

    incident_manager.create_incident(
        "Nairobi",
        "Major road traffic accident",
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
        "Minor vehicle accident",
        "low"
    )


# ============================================================
# MAIN
# ============================================================

def main():
    """Start and run the interactive system."""

    try:

        print("\n" + "=" * 60)
        print("EMERGENCY DISPATCH SYSTEM")
        print("=" * 60)

        # Create managers.
        incident_manager = IncidentManager()
        ambulance_manager = AmbulanceManager()

        # Create demonstration data.
        create_sample_data(
            incident_manager,
            ambulance_manager
        )

        # Create and connect optimizer.
        optimizer = DispatchOptimizer(
            ambulance_manager
        )

        optimizer.set_incident_manager(
            incident_manager
        )

        print("\n[OK] System initialised.")
        print(
            f"[OK] Incidents: "
            f"{incident_manager.get_total_incidents()}"
        )
        print(
            f"[OK] Ambulances: "
            f"{len(ambulance_manager.get_all_ambulances())}"
        )
        print(
            f"[OK] Available ambulances: "
            f"{len(ambulance_manager.get_available_ambulances())}"
        )

        # ----------------------------------------------------
        # Interactive menu
        # ----------------------------------------------------

        while True:

            try:

                display_menu()

                choice = input(
                    "Select an option (1-5): "
                ).strip()

                if choice == "1":

                    report_incident(
                        incident_manager
                    )

                elif choice == "2":

                    view_all_incidents(
                        incident_manager
                    )

                elif choice == "3":

                    view_available_ambulances(
                        ambulance_manager
                    )

                elif choice == "4":

                    run_dispatch(
                        incident_manager,
                        ambulance_manager,
                        optimizer
                    )

                elif choice == "5":

                    print("\n" + "=" * 60)
                    print("SYSTEM SHUTDOWN")
                    print("=" * 60)
                    print(
                        "Thank you for using the "
                        "Emergency Dispatch System."
                    )

                    break

                else:

                    print(
                        "\n[ERROR] Invalid option. "
                        "Please select 1-5."
                    )

            except (EOFError, KeyboardInterrupt):

                print(
                    "\n\nSystem terminated by user."
                )

                break

            except Exception as error:

                print(
                    f"\n[ERROR] Unexpected error: "
                    f"{error}"
                )

                print(
                    "Returning to the main menu..."
                )

    except (EOFError, KeyboardInterrupt):

        print(
            "\n\nSystem terminated by user."
        )

    except Exception as error:

        print(
            f"\n[FATAL ERROR] "
            f"Unable to start the system: {error}"
        )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()