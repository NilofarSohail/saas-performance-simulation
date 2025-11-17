from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import time

app = FastAPI()

TENANTS = ["tenant_a", "tenant_b", "tenant_c"]

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/{tenant_id}/login")
def login(tenant_id: str, req: LoginRequest):
    if tenant_id not in TENANTS:
        raise HTTPException(status_code=404, detail="Tenant not found")

    # Simulate latency differences per tenant
    time.sleep(random.uniform(0.05, 0.2))

    return {"tenant": tenant_id, "status": "logged_in"}

@app.get("/api/{tenant_id}/dashboard")
def dashboard(tenant_id: str):
    if tenant_id not in TENANTS:
        raise HTTPException(status_code=404, detail="Tenant not found")

    time.sleep(random.uniform(0.1, 0.3))
    return {"tenant": tenant_id, "metrics": "some_metrics"}

@app.post("/api/{tenant_id}/orders")
def create_order(tenant_id: str):
    if tenant_id not in TENANTS:
        raise HTTPException(status_code=404, detail="Tenant not found")

    # Random error simulation (5% failure)
    if random.random() < 0.05:
        raise HTTPException(status_code=500, detail="Order processing error")

    time.sleep(random.uniform(0.1, 0.4))
    return {"tenant": tenant_id, "order_status": "created"}
