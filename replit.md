# Contact Book

A small Python console app for managing contacts with JSON file persistence.

## Run & Operate

- `python3 contact_book.py` — run the contact book
- `pnpm --filter @workspace/api-server run dev` — run the API server (port 5000)
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- Required env: `DATABASE_URL` — Postgres connection string

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- API: Express 5
- DB: PostgreSQL + Drizzle ORM
- Validation: Zod (`zod/v4`), `drizzle-zod`
- API codegen: Orval (from OpenAPI spec)
- Build: esbuild (CJS bundle)

## Where things live

- `contact_book.py` — CLI and JSON storage logic
- `contacts.json` — created automatically when the first contact is saved

## Architecture decisions

- Contacts use a human-readable JSON array so the saved data is easy to inspect or back up.
- Writes use a temporary file and atomic replacement to avoid leaving a partially written contacts file.

## Product

The app supports adding contacts with a name, phone, and email; searching all contact fields; deleting with confirmation; and listing the complete contact book.

## User preferences

_Populate as you build — explicit user instructions worth remembering across sessions._

## Gotchas

_Populate as you build — sharp edges, "always run X before Y" rules._

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
