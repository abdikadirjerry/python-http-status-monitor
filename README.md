# Python HTTP Status Monitor (`python-http-status-monitor`)

A zero-dependency Python web application and REST API that monitors HTTP endpoints, measures response latency, computes system availability KPIs, and serves an interactive web dashboard.

## Features

- **Live HTTP Probing:** Measures response status codes and millisecond latency using `urllib.request`.
- **REST API + Web UI:** Built on Python's `http.server` with clean JSON endpoints (`GET`, `POST`, `DELETE`).
- **Zero External Dependencies:** Runs immediately with standard Python 3.

## Quick Start

```bash
python3 run.py
```
