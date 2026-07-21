# AERIS

AERIS is an AI-powered Urban Air Quality Intelligence Platform for smart cities.

## Project Foundation

This repository currently contains the foundational architecture for:
- FastAPI backend
- Next.js frontend
- PostgreSQL + PostGIS configuration
- Docker-based local deployment
- Modular folder structure for future agent-based intelligence services

## Structure

```text
backend/
  app/
    api/
      routes/
    core/
    db/
    models/
    schemas/
    services/
      agents/
    main.py
  requirements.txt
  .env.example

frontend/
  app/
    (dashboard)/
  components/
    dashboard/
    layout/
  hooks/
  lib/
  services/
  package.json

Dockerfile
Dockerfile
docker-compose.yml
```

## Next Step

The foundation is ready for review. No business logic has been implemented yet.
