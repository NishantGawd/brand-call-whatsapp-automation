# Brand Call → WhatsApp Automation System

This repository contains a production-grade, multi-tenant system that connects
phone call events from telephony providers to WhatsApp follow-up flows for
clothing brands and similar businesses.

The system:

- Receives incoming **call status webhooks** from telephony providers.
- Normalizes and stores call & customer data in a **PostgreSQL** database.
- Uses **automation rules** to trigger post-call WhatsApp messages:
  - Thank-you messages.
  - Catalog / product messages.
- Exposes a **dashboard** for each brand (tenant) to:
  - Configure WhatsApp + telephony credentials.
  - Upload and manage products.
  - Enable/disable and tune automation.
  - View calls, messages, and basic analytics.
- Provides a **desktop app** (Electron) that wraps the web dashboard.

## Tech Stack (Locked In)

- Backend API: **FastAPI** (Python 3.11+)
- ORM & migrations: **SQLAlchemy + Alembic**
- Database: **PostgreSQL**
- Queue & jobs: **Celery**
- Broker & cache: **Redis**
- Frontend: **Next.js** (TypeScript, App Router)
- Desktop: **Electron**
- Containerization: **Docker + docker-compose**
- Package manager (frontend & desktop): **npm**

## Repository Structure

```text
backend/   # FastAPI backend API (multi-tenant, webhooks, business logic)
worker/    # Celery worker (job queue for post-call WhatsApp, retries)
frontend/  # Next.js frontend dashboard (multi-tenant UI, setup wizard)
desktop/   # Electron desktop wrapper for the frontend
infra/     # Docker, environment definitions, deployment scripts
docs/      # Architecture and API docs
scripts/   # Helper scripts (format, lint, setup)
.vscode/   # Recommended editor settings
