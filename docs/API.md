# API

The optional synthetic-only API can be started locally with `uvicorn study_sentinel.api:app --host 127.0.0.1 --port 8000`.

`GET /health`: status and mode.

`POST /demo/summary`: JSON `{"n":300,"seed":42}`. Returns participant count, synthetic aggregate means, and per-item missing counts. No participant rows are returned. Validation uses Pydantic. Do not run this toy API as an exposed service.
