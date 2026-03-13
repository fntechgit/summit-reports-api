# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django + Graphene (GraphQL) read-only reporting API for OpenStack/OpenInfra summit data. It connects to an external MySQL database (`openstack_db`) and exposes a single GraphQL endpoint at `/reports`. Authentication is handled via OAuth2 token introspection against an IDP.

## Common Commands

```bash
# Local dev with Docker (recommended)
docker compose up -d                    # Start all services (app, MySQL, Redis)
./start_local_server.sh                 # Migrate + start + shell into container

# Without Docker
docker compose exec app python manage.py runserver 0.0.0.0:8003
docker compose exec app python manage.py migrate --database=openstack_db

# Tests (require openstack_db connection)
docker compose exec app python manage.py test reports_api.reports.tests.openapi_test_case

# Dependencies
pip install -r requirements.txt
```

## Architecture

### Database Design

- **Two databases**: `default` (SQLite in-memory, unused) and `openstack_db` (external MySQL with the actual summit data)
- **Read-only**: `DBRouter` (`reports_api/db_router.py`) routes all `reports` app reads to `openstack_db` and blocks writes/migrations
- All models use `managed = False` — they map to existing MySQL tables, not Django-managed schema
- Redis is used for caching (token info and GraphQL query results via `graphene_django_extras`)

### Request Flow

1. `TokenValidationMiddleware` (`reports_api/authentication.py`) validates OAuth2 bearer tokens by introspecting against the IDP, with Redis caching
2. Single URL route `/reports` serves GraphQL via `GraphQLView` with GraphiQL enabled
3. Root schema (`reports_api/schema.py`) delegates to `reports_api/reports/schema.py` which defines all queries

### Key Modules

- **`reports_api/reports/schema.py`** — All GraphQL types (`*Node`), list types (`*ListType`), serializer types (`*ModelType`), custom resolvers, and the `Query` class. This is the largest file and the main entry point for report logic.
- **`reports_api/reports/filters/model_filters.py`** — `django_filters` FilterSets for all queryable entities (speakers, presentations, events, attendees, metrics, etc.). Complex filters use subqueries and annotations.
- **`reports_api/reports/models/`** — Django models mapping to existing MySQL tables. Organized into subdirectories: `registration/`, `rsvp/`, `extra_questions/`.
- **`reports_api/reports/serializers/model_serializers.py`** — DRF serializers used by `DjangoSerializerType` for Speaker, Presentation, Attendee, etc.

### GraphQL Patterns

- Uses `graphene-django-extras` for pagination (`LimitOffsetGraphqlPagination`), list types, and serializer types
- Custom `DjangoListObjectField` subclasses (`SpeakerModelDjangoListObjectField`, `AttendeeModelDjangoListObjectField`) override `list_resolver` to inject annotations for filtering
- Raw SQL queries are used for metric aggregation (`getUniqueMetrics` in schema.py)
- `SubqueryCount` / `SubQueryCount` / `SubQueryAvg` are custom Subquery helpers used in filters and schema

### OpenAPI Documentation

- Uses `drf-spectacular` for OpenAPI 3.1 schema generation
- Endpoints: `/openapi` (schema), `/api/docs` (Swagger UI), `/api/redoc` (ReDoc)
- These paths are exempt from OAuth2 in `TokenValidationMiddleware.EXEMPT_PATHS`
- `openapi_hooks.py` tags paths as Public/Private and strips security from `/api/public/` paths
- `UNAUTHENTICATED_USER` is set to `None` in `REST_FRAMEWORK` because `django.contrib.auth` is not installed — DRF's default `AnonymousUser` would fail without it
- Tests: `reports_api/reports/tests/openapi_test_case.py`

### Environment Variables

Configured via `.env` file (see `.env.template`). Key vars: `DB_OPENSTACK_*` (database), `REDIS_*` (cache), `RS_CLIENT_*` + `IDP_*` (OAuth2), `SECRET_KEY`.
