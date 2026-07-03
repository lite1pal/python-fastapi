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

## Notes

- Data is currently stored in memory.
- AI and storage integrations are stubbed behind provider interfaces.
- Deleting a customer archives it by setting `status="archived"`.
