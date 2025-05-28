# Feature Flags Backend Service (Practice Project)

This repository is a **practice project** to demonstrate my ability to design and implement a backend service for managing feature flags, including support for flag dependencies, audit logging, and Dockerized deployment.

## What is a Feature Flag?
A **feature flag** (or feature toggle) is a software development technique that allows teams to enable or disable features in a system without deploying new code. Feature flags make it possible to:
- Gradually roll out new features
- Perform A/B testing
- Instantly disable problematic features
- Manage dependencies between features

## Project Highlights
- **Create, toggle, and view feature flags**
- **Support for dependencies**: A flag can only be enabled if all its dependencies are enabled
- **Circular dependency detection**
- **Audit log**: Every operation is tracked with timestamp, reason, and actor
- **REST API** built with Django and Django REST Framework
- **PostgreSQL** as the database
- **Fully Dockerized** with `docker-compose`
- **Automated tests** with `pytest` and `pytest-django`

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Setup
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   ```
2. Create a `.env` file in the project root (see `.env.example` or below):
   ```env
   DJANGO_SECRET_KEY=your-secret-key
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=*
   POSTGRES_DB=featureflagsdb
   POSTGRES_USER=featureflagsuser
   POSTGRES_PASSWORD=featureflagspassword
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   ```
3. Build and start the services:
   ```bash
   docker-compose up --build
   ```
4. The API will be available at [http://localhost:8000/api/flags/](http://localhost:8000/api/flags/)

### Running Tests
To run all automated tests:
```bash
docker-compose run web pytest
```

### API Endpoints
- `POST /api/flags/` — Create a feature flag (with dependencies)
- `POST /api/flags/<id>/toggle/` — Toggle a flag (enable/disable, with dependency validation)
- `GET /api/flags/` — List all flags and their status
- `GET /api/flags/<id>/` — Get flag details
- `GET /api/flags/<id>/audit/` — Get audit log for a flag

### Admin Access
To create a superuser for the Django admin:
```bash
docker-compose run web python manage.py createsuperuser
```

## License
This project is for practice and demonstration purposes only. 