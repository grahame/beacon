# instructions for Claude

## frontend commands

Within the frontend/ directory:

- deno run build: Build the project
- deno run dev: Launch development webserver
- deno run lint: Run the linter
- deno run preview: Vite preview
- deno run test: Run tests with vitest

We are using deno with vite, configured without a `deno.json` - everything for
config is in `package.json`

We are using reactstrap for UX.

## backend commands

within the root directory:

- source .env_local && uv run beacon serve: start the development webserver

## Code style

- Typescript is used for the frontend (frontend/)
- Python is used for the backend (in the root directory of the project)
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')

## Typescript

- Be sure to typecheck when you’re done making a series of code changes
- We are using deno, not npm: to add npm deps, use the deno add npm: syntax

## Python

- this codebase uses `uv` as the package manager

## Workflow

- Prefer running single tests, and not the whole test suite, for performance
