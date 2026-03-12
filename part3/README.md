# HBnB Evolution - Part 2: Business Logic & API

## Introduction
This project is the second part of the HBnB Evolution series (Airbnb clone). The goal is to implement the **Business Logic** and the **API endpoints** of the application.

We have built a backend using **Flask** and **Flask-RESTx** that handles:
- **Users**: Registration and profile management.
- **Places**: Creation and listing of rental places.
- **Reviews**: Posting and reading reviews for places.
- **Amenities**: Managing features like Wi-Fi, Pool, etc.

## Architecture
The application follows a strict **3-Tier Architecture** to separate concerns:

1.  **Presentation Layer (`app/api/v1/`)**:
    - Handles HTTP requests (GET, POST, PUT, DELETE).
    - Validates input data using Data Transfer Objects (DTOs) via Flask-RESTx.
    - Communicates *only* with the Facade.

2.  **Business Logic Layer (`app/services/`)**:
    - Implemented using the **Facade Pattern** (`HBnBFacade`).
    - Acts as the central manager. It receives calls from the API, applies business rules (e.g., "Does this user exist?"), and interacts with the repository.

3.  **Persistence Layer (`app/persistence/`)**:
    - Currently implemented as an **In-Memory Repository**.
    - Stores objects (Users, Places, Reviews) in Python dictionaries/lists during the application runtime.
    - Designed to be easily swapped for a SQL database in future parts.

## Project Structure
```text
.
├── app/
│   ├── api/v1/          # API Endpoints (Presentation Layer)
│   │   ├── users.py
│   │   ├── places.py
│   │   ├── reviews.py
│   │   └── amenities.py
│   ├── models/          # Business Objects (User, Place, Review...)
│   ├── services/        # Business Logic (Facade)
│   └── persistence/     # Data Storage (Repository)
├── run.py               # Application entry point
├── config.py            # Configuration settings
└── requirements.txt     # Python dependencies