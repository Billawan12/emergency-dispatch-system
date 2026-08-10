# 🚑 Emergency Response and Dispatch System

## SWE4040A: Software Construction and Development – Group Project

---

## 📌 Project Overview

The **Emergency Response and Dispatch System** is a simple emergency incident management and ambulance dispatch application developed for the **SWE4040A: Software Construction and Development** course at **United States International University (USIU)**.

The system allows users to report emergency incidents, manage incidents and ambulances, and automatically assign available ambulances to incidents using a **greedy search algorithm based on Search-Based Software Engineering (SBSE)**.

---

## 👥 Group Members

| Name                 | Student ID |
| -------------------- | ---------: |
| Dlamini Silindinkosi |     669235 |
| Silas Claude         |     668922 |
| Shema Manasseh       |     668852 |
| Elie Banga           |     668344 |
| Madut Chan           |     671336 |
| Sharmake Muhamed     |     668595 |
| Kipkorir Kibet       |     669747 |
| Zakaria Idris        |     666797 |
| Akonkwa Lwambwa      |     672390 |

---

## 🛠️ Features

* **Incident Reporting** – Record emergency incidents with location, description, and priority.
* **Incident Management** – View, update, and manage reported incidents.
* **Ambulance Management** – Add and track ambulance locations and availability.
* **SBSE Dispatch Optimisation** – Assign the nearest available ambulance to incidents based on priority and distance.
* **Location Mapping** – Convert predefined locations into geographic coordinates.
* **Travel Time Estimation** – Estimate travel time using road-condition-based speeds.
* **Input Validation** – Validate user input and system states.
* **Command-Line Interface** – Simple interactive menu for system operation.

---

## 🏗️ System Architecture

The system uses a simple layered architecture consisting of a **User Interface Layer**, **Business Logic Layer**, and **Data Layer**.

```text
┌──────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                     │
│                  Command-Line Interface                     │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                     │
│                                                              │
│   ┌──────────────┐   ┌──────────────┐   ┌───────────────┐  │
│   │   Incident   │   │  Ambulance   │   │    Dispatch   │  │
│   │   Manager    │◄─►│   Manager    │◄─►│   Optimizer   │  │
│   └──────────────┘   └──────────────┘   │     (SBSE)    │  │
│                                         └───────────────┘  │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                       DATA LAYER                             │
│               Python lists for system data                  │
└──────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```text
emergency-dispatch-system/
│
├── incident_module.py      # Incident class and manager
├── ambulance_module.py      # Ambulance class and manager
├── dispatch_module.py       # SBSE dispatch optimiser
├── main.py                  # Main program and user interface
└── README.md                # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.7 or higher

No external Python packages are required.

### Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/YOUR_USERNAME/emergency-dispatch-system.git
cd emergency-dispatch-system
```

### Running the System

Run the main program:

```bash
python main.py
```

The main menu provides the following options:

```text
============================================================
              EMERGENCY DISPATCH SYSTEM
============================================================
1. Report a new incident
2. View all incidents
3. View available ambulances
4. Run dispatch
5. Exit
============================================================
Select an option (1-5):
```

---

## 📊 Dispatch Process

The dispatch optimiser uses a greedy search approach:

1. Incidents are ordered by priority.
2. Available ambulances are identified.
3. The distance between each ambulance and incident is calculated.
4. The nearest available ambulance is selected.
5. The selected ambulance is marked as busy.
6. Incidents without an available ambulance remain unassigned.

---

## 📍 Location Mapping

The system uses predefined coordinates for selected locations:

| Location  | Latitude | Longitude |
| --------- | -------: | --------: |
| Nairobi   |  -1.2921 |   36.8219 |
| Karen     |  -1.3197 |   36.7073 |
| Eastleigh |  -1.2765 |   36.8508 |
| Mombasa   |  -4.0435 |   39.6682 |
| Kampala   |   0.3476 |   32.5825 |

---

## 🧪 Sample Data

### Ambulances

| Ambulance   | Location  |
| ----------- | --------- |
| Ambulance 1 | Nairobi   |
| Ambulance 2 | Karen     |
| Ambulance 3 | Eastleigh |

### Incidents

| ID | Location  | Priority |
| -: | --------- | -------- |
|  1 | Nairobi   | High     |
|  2 | Karen     | Medium   |
|  3 | Eastleigh | High     |
|  4 | Langata   | Low      |

---

## 📚 Technologies Used

| Technology   | Purpose                              |
| ------------ | ------------------------------------ |
| **Python 3** | Programming language                 |
| **ChatGPT**  | Generative AI development assistance |
| **Git**      | Version control                      |
| **GitHub**   | Repository and collaboration         |

---

## 🎯 Future Improvements

* Real-time GPS and geocoding
* Database storage
* Web-based user interface
* User authentication
* Real-time ambulance tracking
* Advanced SBSE optimisation techniques
* Integration with emergency communication systems

---

## 📄 License

This project was developed for educational purposes as part of the **SWE4040A: Software Construction and Development** course at **United States International University (USIU)**.
