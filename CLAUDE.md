# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

LaboralSalud SF — Django app for occupational-medicine absenteeism control and
analysis (employee absences, medical visits/turnos, ART accident reporting,
reports). Multi-tenant by `empresa` (company); users log in against a
specific empresa.

**Stack is legacy and fixed: Python 2.7, Django 1.11.** Do not suggest
Python 3 syntax, f-strings, or Django 2+ APIs — they will not run. Code uses
`unicode()`, `<>` for `!=`, `__unicode__`, `django.core.urlresolvers`
(pre-`django.urls`), and old-style `url()` routing, all of which are correct
here, not bugs to "fix".

## Commands

Local dev runs via Docker Compose against a MariaDB container (no sqlite in
practice, despite the `.sqlite`/`.sqlite3` files sitting in the repo root —
those are stale artifacts).

```bash
# Start local stack (app + mariadb + adminer), mounts source for live reload
docker compose -f docker-compose.local.yml up

# Django management commands (run inside the container, or locally with
# DJANGO_SETTINGS_MODULE=laboralsalud.local and a reachable MySQL/MariaDB)
python manage.py runserver 0.0.0.0:8000
python manage.py migrate
python manage.py collectstatic --noinput

# Tests (Django TestCase, per-app tests.py or tests/ package)
python manage.py test
python manage.py test entidades
python manage.py test entidades.tests.test_models.TestEmpleadoModel
```

`manage.py` hardcodes `DJANGO_SETTINGS_MODULE=laboralsalud.local` — override
the env var if you need a different settings module (see below).

Performance smoke tests: `performance_tests/locust.py` (Locust). Browser
regression tests: `SeleniumTests/LABORALSALUD.side` (Selenium IDE).

## Settings modules

`laboralsalud/` has several settings files layered on `settings.py` (base) —
pick the right one for the context, they are not interchangeable:

- `settings.py` — base config shared by all environments (installed apps,
  middleware, templates, i18n/l10n for `es-AR`). No `DATABASES` here.
- `local.py` — local Docker Compose dev (MySQL via env vars, debug toolbar).
- `dev.py` — legacy dev environment on Opalstack.
- `prod.py` — current production (Docker + Dokploy), reads DB creds from env
  via `python-decouple`, has `CONN_MAX_AGE` pooling.
- `production.py` / `opal.py` / `opal_prueba.py` — older/alternate
  Opalstack-hosted deployments with hardcoded paths; mostly historical.

Env vars are read with `decouple.config` and sourced from `.env` (see
`.env.example.py` for the full list: `DB_*`, `SECRET_KEY`,
`SESSION_COOKIE_NAME`, `EMAIL_*`, `GUNICORN_*`, `STATIC_ROOT`, `MEDIA_ROOT`).

## Deployment

Two deployment paths exist simultaneously — know which one a change targets:

1. **Opalstack (legacy, `.github/workflows/main.yml`)**: on push to `master`,
   GitHub Actions SSHes into the Opalstack host, `git pull`s, runs
   `collectstatic`, and restarts Apache directly on the host (no containers).
2. **Docker/Dokploy (current)**: `Dockerfile` (Python 2.7-slim base, patched
   to pull Debian Buster packages from `archive.debian.org` since Buster is
   EOL) + `docker-entrypoint.sh`, which inspects `ENV`/`DEBUG`/`GUNICORN_WSGI`
   to decide between `wsgi_dev.py` and `wsgi.py`, waits for the DB via `nc`,
   optionally runs `collectstatic`/`migrate`, then execs `gunicorn`.
   `docker-compose.yml` (prod), `docker-compose.dev.yml`,
   `docker-compose.static.yml`, and `docker-compose.db.yml` cover different
   slices of this; `docker-compose.local.yml` is the one for local dev.

## Architecture

Django apps, each owning its own `models.py` / `views.py` / `urls.py` /
`forms.py` / `managers.py` / `admin.py`, wired together under
`laboralsalud/urls.py`:

- **`entidades`** — the core domain: companies (`ent_empresa`), employees
  (`ent_empleado`), medical professionals, ART (worker's comp insurers),
  cargos/especialidades. Most other apps import from `entidades.models`.
- **`ausentismos`** — absence records (`aus_*` models: patología,
  diagnóstico, ausencia), the main business object being tracked.
- **`usuarios`** — custom user layer on top of `django.contrib.auth.User`.
  `UsuUsuario` is the "real" user record (Spanish-named legacy table,
  `usu_*` db tables); `UserProfile` links it 1:1 to Django's `User`.
  Authentication is custom — see below.
- **`reportes`** — reporting/aggregation views over `entidades`/`ausentismos`
  data; `reportes.managers` (e.g. `CasasCentrales`, `Sucursales`) is imported
  by `entidades.models`, so watch for import-order/circularity when touching
  either.
- **`general`** — shared cross-app concerns: turnos (appointments/shift
  scheduling), calendar helpers, base64/validators utilities, and
  `laboralsalud/utilidades.py`'s `TIPO_*` choice tuples used across models.
  `general.urls` is the catch-all included last in the root URLconf.
  `general` imports `entidades.models` — the reverse dependency does not
  exist, keep it that way.
- **`modal`** — a small vendored/adapted `django-modal` app providing
  AJAX modal CRUD views (`AjaxCreateView`, `AjaxUpdateView`,
  `AjaxDeleteView`) built on `django-crispy-forms` + Bootstrap 3; used by
  other apps' views for inline create/edit/delete without a full page load.

**Auth**: login is not Django's default. `usuarios.authentication.UsuarioBackend`
checks credentials against `UsuUsuario` (legacy table, hashed via
`django.contrib.auth.hashers`), also validates the selected `empresa` via
`usuarios.utilidades.tiene_empresa`, and lazily creates a shadow
`django.contrib.auth.User` + `UserProfile` on first successful login so the
rest of Django's auth/session machinery still works. `laboralsalud/views.py`
holds the `login`/`logout`/`volverHome` views wired at the project root;
`volverHome` is also `handler404`/`handler500`, so any unhandled error
redirects home/login instead of showing a normal error page.

**Templates**: single shared `templates/` at repo root (not per-app),
namespaced by subdirectory per app (`templates/entidades/`,
`templates/ausentismos/`, etc.), plus `APP_DIRS` template loading.

**Static files**: `static/` is the source tree (vendored JS/CSS: Bootstrap,
DataTables, jQuery UI, django-debug-toolbar assets, etc.);
`staticfiles/` is the `collectstatic` output — don't hand-edit it.

## Known repo quirks (do not "fix" without being asked)

- Compiled `.pyc` files are checked into git alongside `.py` sources despite
  `.gitignore` excluding `*.pyc` (pre-existing tracked files aren't affected
  by a later ignore rule). Editing a `.py` file will leave its `.pyc`
  looking stale/modified in `git status` — that's expected, not something to
  clean up as part of an unrelated change.
- `laboralsalud.sqlite` / `laboralsalud.sqlite3` in the repo root are stale;
  the app runs against MySQL/MariaDB in every real environment.
- Multiple overlapping settings/docker-compose files exist for old
  deployment targets (Opalstack) alongside the current one (Dokploy). When
  changing settings, check which file(s) the active deployment path
  actually uses before editing all of them.
