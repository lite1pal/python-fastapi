# Frontend Scaffold

Minimal React + TypeScript + Vite client for the FastAPI backend in this repo.

## Setup

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Default API target:

- `VITE_API_URL=http://127.0.0.1:8000`
- `VITE_API_TOKEN=admin-token`

## Typed API workflow

`src/api/types.ts` is the stable wrapper the app imports from.
`src/api/generated.ts` is the file meant to be replaced from OpenAPI.

To refresh the generated types after the FastAPI app is running locally:

```bash
npm run generate:types
```

That command rewrites `src/api/generated.ts` from `/openapi.json` while the rest
of the frontend keeps importing from `src/api/types.ts`.
