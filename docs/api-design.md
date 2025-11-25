# API Design (Draft)

This document will evolve as we implement the backend in FastAPI.

## Auth

- `POST /api/auth/login`
- `POST /api/auth/logout` (optional, token blacklist if needed)
- `GET /api/auth/me`

## Tenants & Users

- `POST /api/internal/tenants` (internal/admin use)
- `GET /api/internal/tenants`
- `POST /api/internal/users`

## Products

- `GET /api/products`
- `POST /api/products`
- `PUT /api/products/{id}`
- `DELETE /api/products/{id}`
- `POST /api/products/import` (CSV/Excel)

## Customers

- `GET /api/customers`

## Calls

- `GET /api/calls`

## WhatsApp Messages

- `GET /api/messages`

## Automation Settings

- `GET /api/automation-settings`
- `PUT /api/automation-settings`

## Integrations

### WhatsApp

- `POST /api/whatsapp/credentials`
- `GET /api/whatsapp/credentials`
- `POST /api/whatsapp/test-message`

### Telephony

- `POST /api/telephony/credentials`
- `GET /api/telephony/credentials`

## Webhooks

### Telephony

- `POST /webhooks/call-status/{tenantSlug}`

### WhatsApp Cloud

- `GET /webhooks/whatsapp` (verification)
- `POST /webhooks/whatsapp` (events)

We will refine request/response payloads and validation schemas during implementation.
