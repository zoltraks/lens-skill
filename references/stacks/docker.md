# Docker And Compose Baseline

## Purpose

> **Scope:** Checkable constraints for Dockerfiles and Compose deployments
> **Key items:** base-image pinning, USER instruction, .dockerignore, healthchecks, secret
> handling, Compose env model

This file distills the Docker best-practices guide, the docker-node best practices, the OWASP
Docker cheat sheet, and the Compose file reference listed in `references/source-catalog.md`
into constraints an audit can verify from repository source.

Snapshot date: 2026-09-30.

Feeds `assessment/deployment-review.md`, `assessment/security-review.md`, and
`assessment/dependency-review.md`, and `assessment/baseline-conformance.md` for containerized
subjects.

## Dockerfile Rules

From https://docs.docker.com/build/building/best-practices/ and
https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md.

- Pin base images by digest or immutable tag (`node:24-alpine` is a moving tag. `@sha256:... `
  is pinned). `latest` or bare `node` in a shipped Dockerfile is a reproducibility finding.
- Multi-stage builds separate build tools from the runtime image. A final stage that still
  carries compilers/package managers is a size-and-surface observation.
- `USER` must be set to a non-root account (`node` in node images). Containers default to
  root, which is a hardening finding.
- `COPY` only what the image needs and `.dockerignore` must exist, excluding `.git`,
  `node_modules`, `*.env*`, and secret material - an absent `.dockerignore` is a defect for
  Node images.
- Package installs pin versions where the manager supports it (`apk add --no-cache`,
  `apt-get install -y --no-install-recommends`, `npm ci` over `npm install` for apps).
- One process per container: `ENTRYPOINT`/`CMD` runs the app directly. Shell wrappers that
  swallow signals break graceful shutdown (PID 1 signal handling).
- `EXPOSE`, `HEALTHCHECK`, and a defined stop signal are the operability surface. Missing
  healthchecks on services with orchestrated restarts is an observation.
- Secret material never enters via `COPY` or build args. BuildKit `--secret` mounts or
  runtime env injection are the sanctioned channels - `ENV` carrying credentials is a finding
  because image layers leak.

## OWASP Docker Hardening

From https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html.

- Do not run the docker daemon socket inside containers (`/var/run/docker.sock` mounts are
  root-equivalent findings).
- Drop capabilities (`--cap-drop=ALL`) and add only what's needed. `privileged: true` or
  `--privileged` is a critical finding.
- `read_only`/`read-only` root filesystems where writable paths aren't needed. Tmpfs mounts
  for scratch.
- Resource limits (`memory`, `cpus`, `pids_limit`) bound container resource exhaustion.
- Logging driver configured so container crashes don't lose diagnostics. No
  `logging: driver: none` on production services.

## Compose Semantics

From https://docs.docker.com/compose/compose-file/.

- `environment:` values in `docker-compose.yml` are baked into container config in plaintext.
  secrets belong in `env_file` (gitignored), `secrets:` blocks, or the orchestrator's store -
  literals in `environment:` are a finding class.
- `depends_on` without `condition: service_healthy` does not wait for readiness.
  healthchecks close that gap.
- `ports` publishes to the host. `expose` is internal-only - services that should stay
  internal and publish `ports:` widen the surface.
- Named volumes (`volumes:` top-level) persist data. Bind mounts of source code
  (`./src:/app`) in a production compose file signal dev leakage.
- `restart: unless-stopped`/`always` expresses restart policy. Its absence on services that
  must self-heal is an operational observation.
- Compose `version:` top-level key is obsolete in Compose v2 and ignored - its presence is
  cosmetic drift, not a defect.

## Live Check

When web fetch is available, spot-check one Dockerfile rule against the Docker best-practices
page and one field name against the Compose reference.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
