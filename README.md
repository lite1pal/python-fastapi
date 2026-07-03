# Customer API

Small FastAPI project with a simple layered structure:

- `routers/` for HTTP endpoints
- `services/` for application logic
- `repositories/` for data access
- `providers/` for external integrations

## Run locally

```bash
.venv/bin/uvicorn main:app --reload
```

Then open:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

The API creates the database schema on startup and seeds a few customers so the list and detail endpoints are useful immediately.

## Run tests

```bash
.venv/bin/python -m unittest discover -s tests
```

## Frontend scaffold

A minimal React + TypeScript client is available in `frontend/`.

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Notes

- Data is stored via SQLAlchemy using `DATABASE_URL`.
- AI and storage integrations are stubbed behind provider interfaces.
- Deleting a customer archives it by setting `status="archived"`.
