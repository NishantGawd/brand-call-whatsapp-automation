# Setup Notes (Development Environment)

## Prerequisites

- Python 3.11+
- Node.js 20 LTS
- npm
- Git
- Docker Desktop

## Repository Structure Overview

See `README.md` for high-level folder structure.

## Dev Environments (Planned)

We will maintain separate environments via `.env` files and docker-compose:

- `.env.development` (for local development)
- `.env.production` (for production)

Each service (`backend`, `worker`, `frontend`, `desktop`) will use its own
environment variables, loaded via standard patterns (e.g., `python-dotenv` for
Python, `next.config.js` for Next.js).

## Next Steps

- Phase 1: Define UX flows and screens.
- Phase 2: Initialize FastAPI backend with SQLAlchemy, Pydantic, and database wiring.
- Phase 3: Initialize Next.js frontend with TypeScript and basic auth layout.

This file will be updated with exact commands as we implement each phase.
