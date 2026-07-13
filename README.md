# Trekking Management Application

## Project Overview

The Trekking Management Application is a Flask-based web system developed by Abinash Mohanty starting 1 July 2026. It addresses the need for managing trekking journeys, user bookings, coordinator authorization, and administrative control in a unified platform.

### Problem Statement

Trekking operators often rely on manual spreadsheets or separate systems to manage trip schedules, seat availability, staff assignments, and customer bookings. This creates operational inefficiencies, poor visibility, and limited control over coordinator verification, booking status, and user management.

This project solves that problem by providing:
- role-based access for directors, coordinators, and customers
- journey creation and assignment workflows
- coordinator authorization and user moderation
- ticket booking with seat availability tracking
- journey search and customer ticket display

## Features

- Multi-role authentication: director, coordinator, customer
- Director dashboard for journey creation and user moderation
- Coordinator dashboard for assigned journey updates
- Customer dashboard for journey search and booking
- Secure password hashing with `pbkdf2:sha256`
- SQLite database storage with SQLAlchemy ORM
- Responsive UI layout using Bootstrap Morph theme

## Technology Stack

- Python
- Flask
- Flask-SQLAlchemy
- Jinja2 templates
- SQLite
- HTML/CSS
- Bootstrap Morph theme

## Repository Structure

```text
Trekking management application _24f2000448/
├── app.py
├── models/
│   └── schemas.py
├── controllers/
│   ├── auth_ctrl.py
│   ├── director_ctrl.py
│   ├── coordinator_ctrl.py
│   └── customer_ctrl.py
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── director_dash.html
│   ├── coordinator_dash.html
│   └── customer_dash.html
├── static/
│   └── theme.css
├── requirements.txt
├── TMA.sqlite
└── TREMAP_Project_Report.pdf
```

## Application Components

### `app.py`

- Main Flask entry point
- Configures the SQLite database at `TMA.sqlite`
- Sets the Flask `SECRET_KEY`
- Initializes SQLAlchemy
- Registers Blueprints for auth, customer, coordinator, and director
- Seeds default demo accounts on first start
- Runs the web server on port `8113`

### `models/schemas.py`

Defines the core data models:
- `Account`
- `Journey`
- `Ticket`

The models encode relationships between users, trips, and bookings.

### `controllers/auth_ctrl.py`

Handles authentication routes:
- `/auth/login`
- `/auth/register`
- `/auth/logout`

Customer registrations are auto-authorized, while coordinators require director approval.

### `controllers/director_ctrl.py`

Handles director functionality:
- dashboard view
- journey creation
- coordinator authorization
- user banning and deletion

### `controllers/coordinator_ctrl.py`

Handles coordinator functionality:
- view assigned journeys
- update journey status
- modify available slot counts

### `controllers/customer_ctrl.py`

Handles customer functionality:
- browse scheduled journeys
- search journeys by location
- book tickets
- view personal bookings

## Database Models

### `Account`

Fields:
- `aid`
- `username`
- `passkey`
- `role_level`
- `authorized`
- `is_active`

Methods:
- `set_pass()`
- `check_pass()`

### `Journey`

Fields:
- `jid`
- `title`
- `location`
- `difficulty`
- `total_slots`
- `available_slots`
- `start_date`
- `end_date`
- `status`
- `assigned_to`

### `Ticket`

Fields:
- `tid`
- `customer_id`
- `journey_id`
- `booked_on`

## Default Demo Accounts

The app seeds demo accounts on first startup:

- Director: `director` / `director`
- Customer: `gamma_customer` / `password123`
- Coordinator: `gamma_coord` / `password123`

## Setup Instructions

1. Activate the virtual environment:

```bash
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

4. Open the browser:

```text
http://127.0.0.1:8113
```

## Usage Guide

- Log in via `/auth/login`
- Register via `/auth/register`
- Director manages journeys and users
- Coordinators update assigned journeys
- Customers search and book journeys

## Notes

- Role-based access is enforced through session role checks.
- Coordinators must be authorized before login.
- Booking reduces available slots immediately.
- The app is designed for a lightweight, SQLite-backed deployment.

## Future Improvements

- stronger validation and error handling
- prevent duplicate bookings at the database level
- add password reset and email support
- improve user interface and mobile responsiveness
- add automated tests for routes and database models
