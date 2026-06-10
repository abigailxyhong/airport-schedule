# ✈ Airport Schedule Analysis Dashboard

An interactive airport analytics dashboard built with **Dash**, **FastAPI**, and **Plotly** for exploring flight schedules, passenger capacity, and operational demand patterns.

This project was developed as part of the BreezE Summer Intern task.

---

# Features

## Overview Dashboard

Provides a daily operational summary for a selected date:

- Total Flights
- Top Airline
- Top Destination

Line Chart:

- Flights per hour

---

## Flight Volume Analysis

Interactive analysis of flight activity with filters for:

- Date range
- Airline
- Destination

Visualisations:

- Flights per Hour (Bar Chart)
- Flights per Day (Line Chart)

Used to identify:

- Peak operating periods
- Airline activity
- Route demand patterns

---

## Capacity Analysis

Visualises seat capacity throughout the day.

Features:

- Date selection
- Seats offered per hour
- Capacity peak identification

Visualisation:

- Seats Per Hour (Line Chart)

---

## Technology Stack

| Layer | Technology |
|---------|------------|
| Frontend | Dash |
| Components | Dash Mantine Components |
| Charts | Plotly |
| Backend API | FastAPI |
| Data Processing | Pandas |
| Package Management | pip |
| Containerisation | Docker |
| Orchestration | Docker Compose |

---

# Project Structure

```text
airport-schedule/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
│
├── pages/
│   ├── overview.py
│   ├── volume.py
│   └── capacity.py
│
├── components/
│   ├── layout.py
│   └── navbar.py
|
├── assets/
│   └── styles.css
|
├── api/
│   ├── main.py
│   └── analytics.py
│   └── data_loader.py
│
├── data/
│   └── sample_flight_schedule.csv
│
└── README.md
```

---

# Local Setup

## 1. Clone Repository

```bash
git clone <repository-url>
cd airport-schedule
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / Mac

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

Using pip:

```bash
pip install -r requirements.txt
```

or using uv:

```bash
uv sync
```

---

## 4. Configure Environment Variables

Create a file called:

```text
.env
```

Example:

```env
API_URL=http://localhost:8000
```

---

## 5. Start FastAPI Backend

```bash
uvicorn api.main:app --reload
```

Backend will run at:

```text
http://localhost:8000
```

---

## 6. Start Dash Frontend

Open a second terminal:

```bash
python app.py
```

Dashboard will run at:

```text
http://localhost:8050
```

---

# Running with Docker

## Prerequisites

Install Docker Desktop:

https://www.docker.com/products/docker-desktop/

Verify installation:

```bash
docker --version
docker compose version
```

---

# Build Docker Image

From the project root:

```bash
docker build -t airport-dashboard .
```

---

# Run Docker Container

```bash
docker run -p 8050:8050 airport-dashboard
```

Dashboard:

```text
http://localhost:8050
```

---

# Docker Compose

Docker Compose is recommended because it simplifies startup and environment management.

---

## docker-compose.yml

Example:

```yaml
services:
  dashboard:
    build: .
    ports:
      - "8050:8050"
    env_file:
      - .env
```

---

## Start Application

```bash
docker compose up --build
```

---

## Run in Background

```bash
docker compose up -d
```

---

## Stop Application

```bash
docker compose down
```

---

# API Endpoints

The dashboard consumes data from a FastAPI backend.

Example endpoints:

```text
GET /analytics/flights-per-hour

GET /analytics/flights-per-day

GET /analytics/flights-per-airline

GET /analytics/flights-per-destination

GET /analytics/seats-per-hour

GET /analytics/summary-day-flights

GET /analytics/date-range
```

---


# Future Improvements

Potential enhancements include:

- Passenger demand estimation using load factors
- Route performance analysis
- Airline market share visualisations
- Interactive maps
- PostgreSQL database integration
- Authentication and user roles
- Automated testing with Pytest
- CI/CD deployment pipeline using GitHub Actions

---

# Author

Abi

Developed as part of the BreezE Summer Intern development task.