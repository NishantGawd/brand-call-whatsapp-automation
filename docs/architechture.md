# System Architecture

## Overview

This system connects telephony call events to WhatsApp follow-up automation
for multiple clothing brands (tenants).

Core components:

- **Backend API (FastAPI)**
  - Multi-tenant aware (every request is scoped by tenant).
  - REST/JSON APIs for:
    - Managing tenants, users.
    - Managing products, customers, calls, WhatsApp messages.
    - Tenant-specific settings (WhatsApp & telephony credentials, automation rules).
  - Webhook endpoints:
    - Telephony call status webhooks.
    - WhatsApp Cloud webhooks (message status & inbound messages).

- **Worker (Celery)**
  - Python-based Celery worker processes background jobs.
  - Uses Redis as broker and (optionally) result backend.
  - Job types:
    - Post-call WhatsApp follow-ups.
    - Retry logic for failed sends.
    - Potentially scheduled tasks and clean-up jobs.

- **Frontend (Next.js)**
  - Tenant dashboard:
    - First-time setup wizard.
    - Product management.
    - Call & WhatsApp logs.
    - Settings & automation toggles.
  - Authentication (tenant users log into their own workspace).

- **Desktop App (Electron)**
  - Wraps the frontend in a desktop shell.
  - Allows clothing brands to use the system as a native-looking desktop app.

- **Infrastructure**
  - PostgreSQL for persistent data.
  - Redis for queues and caching.
  - Docker and docker-compose for local and production deployments.

## Service Responsibilities

### Backend API (FastAPI)

- HTTP API for frontend & desktop client.
- Authentication & authorization.
- Tenant scoping:
  - Each user belongs to a tenant.
  - All data is associated with a tenant.
- Database access via SQLAlchemy ORM.
- Validation of incoming data and webhooks using Pydantic models.

### Worker (Celery)

- Subscribes to queues (Redis).
- Encapsulates business processes that must be:
  - Reliable.
  - Retryable.
  - Not blocked by HTTP response times.
- Examples:
  - On `CALL_COMPLETED`, enqueue a job to send WhatsApp follow-up.
  - On WhatsApp send failure, retry with exponential backoff.

### Frontend

- Presents business-friendly UI to brand owners and staff.
- Provides:
  - Setup wizards.
  - Data tables with pagination and filtering.
  - Configuration forms for integrations.
  - Dashboards with key metrics.

### Desktop (Electron)

- Loads the hosted frontend application URL.
- Provides OS-level integrations (tray, notifications, shortcuts) where useful.

## Ports (Planned Defaults)

- Backend API: `http://localhost:8000`
- Worker: no HTTP port (internal), may expose metrics later.
- Frontend: `http://localhost:3000`
- Desktop: local app that wraps `http://localhost:3000` or a production URL.
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

These may be overridden by environment variables in `docker-compose`.

## Data Flow (High-Level)

1. **Call happens** on telephony provider.
2. Provider sends **call status webhook** (call completed) → Backend.
3. Backend:
   - Normalizes call data.
   - Resolves customer identity (phone number).
   - Stores call + customer.
   - Enqueues a "post-call WhatsApp" job into Redis via Celery.
4. Worker (Celery):
   - Consumes the job.
   - Checks tenant automation settings and rules.
   - Sends WhatsApp template message(s) using WhatsApp Cloud API.
   - Stores WhatsApp message logs.
5. Frontend:
   - Reads from the API to show calls, messages, and automations.
   - Allows brand owners to configure templates & rules.

More detailed sequence diagrams and ERDs will be added as we implement specific flows.
