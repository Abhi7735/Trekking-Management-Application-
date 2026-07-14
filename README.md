# Trekking Management Application

## Project Overview

The Trekking Management Application is a Flask-based web application for managing trekking journeys, bookings, coordinator approval, and user roles in a single platform. It is designed to simplify trip administration for directors, coordinators, and customers.

## Objectives

This project helps users to:
- manage trekking journeys and seat availability
- allow customers to browse and book trips
- let coordinators update assigned journeys
- give directors control over user authorization and trip management

## Key Features

- Role-based login for directors, coordinators, and customers
- Director dashboard to create journeys and manage users
- Coordinator dashboard to update journey status and slots
- Customer dashboard to search and book journeys
- Secure password hashing using pbkdf2:sha256
- SQLite database support using Flask-SQLAlchemy
- Responsive web interface with Bootstrap-based styling

## Technology Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML/CSS
- Jinja2 templates

## Project Structure

```text
Trekking management application _24f2000448/
├── app.py
├── requirements.txt
├── controllers/
│   ├── auth_ctrl.py
│   ├── coordinator_ctrl.py
│   ├── customer_ctrl.py
│   └── director_ctrl.py
├── models/
│   └── schemas.py
├── static/
│   └── theme.css
├── templates/
│   ├── base.html
│   ├── coordinator_dash.html
│   ├── customer_dash.html
│   ├── director_dash.html
│   ├── edit_journey.html
│   ├── layout.html
│   ├── login.html
│   └── register.html
└── TMA.sqlite
```

## Installation and Setup

1. Open the project folder in a terminal.
2. Create and activate a virtual environment if needed.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python app.py
```

5. Open the browser at:

```text
http://127.0.0.1:8113
```

## Default Demo Accounts

The application creates demo accounts automatically on first run:

- Director: director / director
- Customer: gamma_customer / password123
- Coordinator: gamma_coord / password123

## How the Application Works

- Users log in through the authentication system.
- Directors can create journeys and approve coordinators.
- Coordinators can update assigned trekking journeys.
- Customers can search available trips and make bookings.
- Bookings reduce the available slots in real time.

## Notes for Submission

For a compact project submission, keep the project archive small by excluding:
- virtual environment folders
- Python cache folders
- temporary files

This project is suitable for packaging into a compressed archive within the requested size limit when unnecessary files are removed.

## Conclusion

This project demonstrates a complete lightweight web application for trekking management with role-based access, database integration, and a user-friendly dashboard experience..
