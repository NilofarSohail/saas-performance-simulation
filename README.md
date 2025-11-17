# SaaS Performance Simulation (Multi-Tenant Load Testing)

This project simulates performance testing of a **multi-tenant SaaS application** using:

- **FastAPI** as a simple backend API
- **Apache JMeter** to generate realistic multi-tenant load
- **CSV Data Set Config** to drive different tenants and credentials
- **Python (pandas)** to analyze JMeter results and generate a performance report

It’s designed to mimic what a **Performance Test Engineer** does in a real SaaS environment:
design scenarios, generate traffic, collect metrics, and summarize findings.

---

## 1. Architecture Overview

**Components:**

- `backend_api/main.py`  
  FastAPI app exposing endpoints such as:
  - `POST /api/{tenant_id}/login`
  - `GET  /api/{tenant_id}/dashboard`
  - `POST /api/{tenant_id}/orders`

- `jmeter/CSV Data Set Config.jmx`  
  JMeter test plan:
  - Uses **Thread Group** to simulate multiple users
  - Uses **CSV Data Set Config** with `tenants.csv` to parameterize tenants
  - Calls Login → Dashboard → CreateOrder per user
  - Writes results to `jmeter_results.csv` via **Simple Data Writer**

- `analyze_results.py`  
  Python script that loads `jmeter_results.csv` and produces:
  - Overall success rate
  - Avg / median latency
  - P90 / P95 / P99 latency
  - Breakdown by endpoint (Login, Dashboard, CreateOrder)
  - A text report: `performance_summary.txt`

---

## 2. Project Structure

```text
saas-performance-simulation/
├─ backend_api/
│  ├─ main.py
│  ├─ analyze_results.py
│  ├─ requirements.txt
│  ├─ venv/                 # local virtualenv (optional, not required in Git)
│  └─ jmeter/
│     ├─ data/
│     │  ├─ tenants.csv
│     │  └─ results/
│     │     ├─ jmeter_results.csv
│     │     └─ performance_summary.txt
│     └─ CSV Data Set Config.jmx
└─ README.md
