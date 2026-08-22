# 🌍 GlobeTrotter

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![Bootstrap 5](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A modern, feature-rich travel itinerary planner and smart budget tracker built for seamless trip organization.**

---

## ✨ Key Features

*   **🔒 Secure User Authentication:** Robust session management powered by `Flask-Login` and secure password hashing.
*   **🗺️ Multi-City Trip Builder:** Plan multi-destination adventures with dynamic stop sequencing and automated date tracking.
*   **💰 Real-Time Budget Tracking:** Automatic expense computation against custom budget limits with instant visual **over-budget warning alerts**.
*   **🔍 Advanced Activity Search & Filtering:** Filter available activities instantly by category, maximum cost, and destination city.
*   **📋 Itinerary Cloning ("Copy Trip"):** Discover community inspiration and clone public itineraries straight into your personal profile with a single click.
*   **📅 Chronological Trip Timeline:** View all stops and activities organized in an intuitive, time-sequenced layout.
*   **🖨️ One-Click PDF Export:** Clean, clutter-free print mode optimized for saving itineraries directly as professional PDF travel reports.
*   **🎒 Smart Packing Checklist:** Dynamically generates custom packing lists tailored to destination regions and activity profiles.

---

## 🛠️ Tech Stack & Why We Chose It

| Technology | Purpose | Why We Used It |
| :--- | :--- | :--- |
| **Python & Flask** | Backend Web Framework | Lightweight, fast to set up for hackathons, and gives explicit control over routing and server-side logic without heavy boilerplate. |
| **Flask-SQLAlchemy** | Database ORM | Provides an elegant, Pythonic interface to manage relational database schemas and queries seamlessly. |
| **Flask-Login** | Session Management | Handles user authentication states out-of-the-box, saving hours of custom security configuration. |
| **SQLite** | Database | Zero-configuration setup, file-based, and ideal for rapid local development and deployment. |
| **Bootstrap 5 & Jinja2** | Frontend & Templating | Enables rapid UI prototyping with responsive components and clean server-side rendering without complex frontend build tools. |

---

## 🚀 Installation & Quick Start Guide

Follow these steps to set up and run the project locally on your machine:

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/globetrotter.git](https://github.com/your-username/globetrotter.git)
cd globetrotter

2. Create and Activate a Virtual Environment
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS / Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Initialize and Run the Application

python app.py

GlobeTrotter/
│
├── app.py                  # Main Flask application and route definitions
├── models.py               # Database schemas and SQLAlchemy models
├── requirements.txt        # Project python dependencies
├── README.md               # Project documentation
│
└── templates/              # Jinja2 HTML templates
    ├── base.html
    ├── login.html
    ├── signup.html
    ├── dashboard.html
    ├── create_trip.html
    ├── itinerary_builder.html
    ├── budget.html
    ├── activity_search.html
    ├── export_trip.html
    ├── packing_list.html
    └── timeline.html

🔮 Future Upgrades & Roadmap
Note: For hackathon demonstration purposes, certain live integrations are currently static or simulated, but they can absolutely be implemented for production scale.

🌤️ Live Weather API Integration: Fetch real-time weather forecasts for destination cities dynamically based on trip travel dates.

🤝 Real-Time Collaboration: Introduce WebSockets for multi-user simultaneous trip editing (like Google Docs for travel planning).

💳 Direct Booking & Payment Gateway: Integrate Stripe or Razorpay APIs to book flights, hotels, and activities straight from the itinerary builder.

🤖 AI Recommendation Engine: Leverage advanced LLMs to auto-generate personalized day-by-day travel itineraries based on user preferences.

💡 Hackathon Note
Built with high performance and zero bloatware in mind, ensuring rapid deployment and a flawless user experience under tight hackathon deadlines.