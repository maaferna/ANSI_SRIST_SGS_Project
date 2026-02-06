# CSIRT AI Platform – Architecture

## 1. Overview

This project implements a **modular, cloud-native security intelligence platform** designed to ingest, analyze, and triage cybersecurity events from the **CSIRT / ANCI MISP API**, enriched and prioritized using **Large Language Models (LLMs)**.

The platform is designed to be:

* **Scalable** (future ML / GPU workloads)
* **Isolated** (no interference with existing production LLM services)
* **Cloud-ready** (Huawei Cloud ECS, Docker-based)
* **Extensible** (future LangGraph, PyTorch, CUDA, vector databases)

The architecture follows **industry best practices** for microservices, separation of concerns, and secure internal networking.

---

## 2. High-Level Architecture

```
                    ┌─────────────────────────┐
                    │        Web Browser        │
                    └───────────┬─────────────┘
                                │
                                ▼
                     ┌────────────────────────┐
                     │        NGINX Gateway     │
                     │   (Single Public Entry) │
                     └───────────┬────────────┘
                         ┌────────┴─────────┐
                         ▼                  ▼
            ┌──────────────────┐   ┌──────────────────┐
            │   Django Web App  │   │   FastAPI Service │
            │  (UI / Orchestration) │ │ (CSIRT + LLM API)│
            └──────────┬───────┘   └──────────┬───────┘
                       │                      │
                       ▼                      ▼
              ┌────────────────┐     ┌─────────────────────┐
              │   PostgreSQL    │     │   External LLM API   │
              │ (Structured DB)│     │ (vLLM – separate     │
              └────────────────┘     │  Docker project)     │
                                      └─────────────────────┘
```

---

## 3. Separation of Responsibilities

### 3.1 Django (Web / Orchestration Layer)

**Purpose**

* Primary web application
* User authentication and authorization
* Dashboard rendering and reporting
* Workflow orchestration (what to analyze, when, and how)
* Persistent storage of analysis results

**Key Responsibilities**

* Render templates and dashboards
* Trigger analysis jobs via FastAPI
* Store normalized events and AI results
* Manage user access and roles

**Technology**

* Django 5.x
* Gunicorn
* PostgreSQL
* Micromamba + pip (future-ready for ML dependencies)

---

### 3.2 FastAPI (Microservice / Intelligence Layer)

**Purpose**

* Stateless API microservice
* Integration with CSIRT / ANCI MISP API
* Communication with LLM inference service
* Event normalization, enrichment, and triage

**Key Responsibilities**

* Fetch events and IOCs from CSIRT API
* Normalize raw threat intelligence data
* Call LLM endpoints for semantic analysis
* Return structured JSON results to Django
* Run asynchronous/background tasks (Celery)

**Technology**

* FastAPI
* Uvicorn
* httpx (async HTTP)
* Celery + Redis

---

### 3.3 LLM Inference (External, Isolated)

**Important Design Decision**
The LLM inference service (vLLM) is **not part of this Docker Compose project**.

**Reasons**

* It is owned and operated by another team
* It is already in production
* Zero risk of interference or downtime
* Clear ownership and responsibility boundaries

**Integration Model**

* Consumed as an **external OpenAI-compatible API**
* Accessed via **private IP / internal network**
* No shared Docker networks or volumes

---

## 4. Deployment Model (Huawei Cloud)

### 4.1 Compute

* **Huawei Cloud ECS (AC2)**
* Docker + Docker Compose
* Separate ECS or same VPC for LLM host

### 4.2 Networking

* Only **NGINX (80/443)** is publicly exposed
* All internal services communicate via Docker bridge network
* LLM access restricted via Security Groups (private subnet only)

### 4.3 Security

* No direct public exposure of FastAPI or Django ports
* Environment variables for secrets
* Ready for Huawei KMS / Secrets Manager integration
* Internal service-to-service communication only

---

## 5. Container Strategy

This project uses **one Docker Compose project** that is fully isolated from other Compose stacks.

### Services

| Service   | Role                               |
| --------- | ---------------------------------- |
| `gateway` | Reverse proxy, single public entry |
| `web`     | Django application                 |
| `api`     | FastAPI microservice               |
| `worker`  | Celery async worker                |
| `beat`    | Celery scheduler                   |
| `db`      | PostgreSQL                         |
| `redis`   | Message broker / cache             |

**Design Principle**

> Containers are environments.
> No Python virtualenvs are used inside containers.

---

## 6. Dependency Management Strategy

### Why Micromamba in Django?

The Django service uses **micromamba** to prepare for:

* PyTorch
* CUDA bindings
* LangGraph
* Advanced ML tooling

This allows:

* Deterministic builds
* Future GPU-enabled extensions
* Hybrid Conda + pip dependency resolution

FastAPI remains **pip-only** to stay lightweight and fast.

---

## 7. Data Flow Example (End-to-End)

1. User accesses dashboard via browser
2. Django triggers `/api/csirt/events/latest`
3. FastAPI fetches data from CSIRT API
4. FastAPI sends event text to LLM API
5. LLM returns structured analysis
6. FastAPI returns enriched JSON to Django
7. Django stores results and renders UI

---

## 8. Scalability & Future Extensions

This architecture supports:

* Adding a **dedicated GPU ML worker** (PyTorch/CUDA)
* LangGraph multi-agent workflows
* Vector databases (Qdrant / FAISS)
* Horizontal scaling of FastAPI workers
* Migration to managed Huawei services (RDS, OBS)

**No refactor required** to add these capabilities.

---

## 9. Why This Architecture Is “Production-Grade”

* Clear ownership boundaries
* Zero coupling with existing production LLM services
* Secure by default (minimal exposed surface)
* Cloud-native and vendor-agnostic
* Designed for growth, not demos

---

## 10. Summary

This project follows **real industry patterns** used in:

* SOC automation platforms
* Threat intelligence pipelines
* AI-assisted security operations

It balances **practicality today** with **scalability tomorrow**, without compromising operational safety.

---
