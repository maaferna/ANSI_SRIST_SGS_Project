# ANSI SRIST SGS Platform

Modular backend platform built with **Django**, **FastAPI**, **Celery**, and **Nginx**, designed for scalable service orchestration, asynchronous processing, and future AI/ML integrations.

This repository represents the **development baseline** for a production-grade backend architecture, containerized with Docker and orchestrated via Docker Compose.

---

## 🧱 High-Level Architecture

```

```
            ┌───────────────┐
            │   Web Browser  │
            └───────┬───────┘
                    │ HTTP
            ┌───────▼───────┐
            │     NGINX     │
            │   (Gateway)  │
            └───────┬───────┘
      ┌─────────────┴─────────────┐
      │                             │
```

┌────────▼────────┐        ┌─────────▼────────┐
│  Django Backend │        │   FastAPI API    │
│  (Admin / Web)  │        │  (Async / REST) │
│   Gunicorn      │        │    Uvicorn       │
└────────┬────────┘        └─────────┬────────┘
│                             │
└──────────┬───────────┬─────┘
│           │
┌──────▼───┐   ┌──▼────────┐
│  Celery  │   │  Celery   │
│  Worker  │   │   Beat    │
└──────┬───┘   └────┬──────┘
│            │
┌─────▼─────┐  ┌───▼──────┐
│   Redis   │  │ Postgres │
└───────────┘  └──────────┘

```

---

## 🧩 Services Overview

### 1. **Gateway (NGINX)**
- Single entry point for HTTP traffic
- Routes requests to:
  - Django backend (`/`, `/admin`)
  - FastAPI endpoints (`/api`)
- Enables future TLS, rate-limiting, and auth layers

---

### 2. **Django Backend (`backend-web`)**
- Traditional Django project
- Responsibilities:
  - Admin interface
  - Web views (future)
  - Authentication base
- Served with **Gunicorn**
- Static files handled via `collectstatic`

**Port (internal):** `8001`

---

### 3. **FastAPI Service (`api`)**
- Async REST API
- Designed for:
  - Business logic
  - Integrations
  - ML / AI endpoints
- Served with **Uvicorn**

**Port (internal):** `8080`

---

### 4. **Celery Worker**
- Asynchronous task execution
- Uses Redis as broker
- Shares codebase with FastAPI

---

### 5. **Celery Beat**
- Scheduled jobs (cron-like)
- Periodic background tasks

---

### 6. **PostgreSQL**
- Primary relational database
- Shared across Django and FastAPI

---

### 7. **Redis**
- Message broker for Celery
- Cache / ephemeral storage

---

## 📁 Repository Structure

```

.
├── compose.yml
├── compose.override.yml
├── .env
├── .dockerignore
├── infra/
│   ├── nginx/
│   │   └── default.conf
│   └── scripts/
│       ├── entrypoint_api.sh
│       └── entrypoint_web.sh
├── services/
│   ├── api/
│   │   ├── app/
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── backend-web/
│       ├── src/
│       │   ├── manage.py
│       │   └── config/
│       ├── requirements.txt
│       ├── environment.yml
│       └── Dockerfile
├── docs/
└── README.md

````

---

## 🐳 Docker & Compose Design Principles

- **One process per container**
- **One service per responsibility**
- **Shared code, separate lifecycles**
- Infra scripts centralized under `/infra`
- No generated artifacts committed (e.g. `staticfiles/`)

---

## ▶️ Running the Platform (Development)

```bash
docker compose up -d --build
````

### Access points

| Service      | URL                      |
| ------------ | ------------------------ |
| Gateway      | `http://<HOST_IP>/`      |
| Django Admin | `http://<HOST_IP>/admin` |
| FastAPI      | `http://<HOST_IP>/api`   |

---

## 👤 Create Django Superuser

```bash
docker compose exec backend-web \
  micromamba run -n web python manage.py createsuperuser
```

---

## 🧪 Logs & Debugging

```bash
docker compose logs -f backend-web
docker compose logs -f api
docker compose logs -f worker
```

---

## 🛡️ Security Notes (Dev Mode)

* `DEBUG = True`
* `ALLOWED_HOSTS` explicitly configured
* Ports restricted at cloud security-group level
* No secrets committed to repo

---

## 🚀 Roadmap

* Split Django settings (`base / dev / prod`)
* Add authentication between Django ↔ FastAPI
* Add healthchecks
* CI/CD pipeline
* Production static handling (S3 / CDN)
* Observability (Prometheus / Grafana)

---

## 📌 Status

✅ Development baseline stable
⚙️ Infrastructure validated
🧠 Ready for feature development

---

