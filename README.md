# Automotive Workshop Management System

A full-stack workshop management application built with Flask as part of my DevOps portfolio.

## Features

- Vehicle Management
- Job Management
- SQLite Database
- Docker
- GitHub Actions (Coming Soon)
- AWS Deployment (Coming Soon)

## Tech Stack

- Python
- Flask
- SQLAlchemy
- SQLite
- HTML
- CSS
- Bootstrap
- Docker

## Roadmap

- [x] Flask setup
- [x] Vehicle listing
- [x] Vehicle CRUD
- [x] Job Management
- [X] Docker
- [ ] GitHub Actions
- [ ] AWS Deployment
- [ ] Nginx
- [ ] Terraform

## Local Development Setup

Follow these steps to run the application locally using Docker.

### 1. Prerequisites
Ensure you have [Docker](https://docker.com) and Docker Compose installed.

### 2. Environment Configuration
Create a `.env` file in the root directory:
```text
DATABASE_URL=sqlite:////app/instance/workshop.db
DB_FILE_PATH=./instance/workshop.db
```

### 3. Spin up the Container
Build and start the application services:
```bash
docker compose up --build
```
The application will be accessible at `http://localhost:5000`.

### 4. Persistence Verification
Your database is mapped via volumes to your local directory as `workshop.db`. Data will persist even if the container is destroyed or rebuilt.
