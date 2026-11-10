# Student Accommodation Reports

Python runs locally in `.venv`; PostgreSQL 16 runs in Docker.

## Run

Requires Python 3.9+ and Docker Compose. From `python-practice`, with Docker running:

Create `.env` with `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`.
Put `students.json` and `rooms.json` in `data/`.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
./run.sh --format json
```

Next launches: `./run.sh`. Use `--format xml` for XML.
Menu: `1` load data, `2–5` reports, `0` exit. Results: `output/`.

## Index

`sql/indexes.sql` is applied automatically by `run.sh`:

```sql
CREATE INDEX IF NOT EXISTS idx_students_room
    ON students (room);
```

The index targets `students.room`, the join key used by the reports.
Alternatives to evaluate separately include `(room, birthday)`, `(room, sex)`,
and a covering index with the report columns.

Recorded local measurements:

| Metric | Before | After |
| --- | --- | --- |
| Planning buffers | `shared hit=60 dirtied=1` | `shared hit=29 read=4` |
| Planning time | 0.906 ms | 0.346 ms |
| Execution time | 6.000 ms | 2.143 ms |

These measurements describe one local comparison. Evaluate each report with
`EXPLAIN (ANALYZE, BUFFERS)` and repeated runs; index benefits depend on the query
and data.
