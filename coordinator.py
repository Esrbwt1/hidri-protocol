# coordinator.py (Version 2.1)

# --- 1. Imports ---
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

# --- 2. Application Setup ---
app = FastAPI(
    title="Hidri Alpha Coordinator v2.1",
    description="The central nervous system for the Hidri Alpha MVP, now with hardened code and comments for public release.",
    version="0.2.1"
)

# --- 3. In-Memory State (The Project's 'Single Source of Truth') ---
# For the MVP, we use simple Python dictionaries to manage the state of the network.
# This is a stand-in for a future decentralized system (e.g., blockchain smart contracts).
# All this data is ephemeral and will reset when the server restarts.
PROVIDERS: Dict[str, Any] = {}
TASKS: Dict[str, Any] = {}
TASK_QUEUE: List[str] = []
LEDGER: Dict[str, float] = {}
TASK_ID_COUNTER = 0

# --- 4. Pydantic Data Models (Our API's 'Language') ---
# These models enforce a strict data structure for our API. If a client sends
# data that doesn't match this structure, FastAPI automatically rejects it.
class ProviderInfo(BaseModel):
    provider_id: str
    address: str

class Task(BaseModel):
    creator_id: str
    model_json: str
    epochs: int

class TaskResult(BaseModel):
    task_id: str
    provider_id: str
    accuracy_before: float
    accuracy_after: float

# --- 5. API Endpoints (The 'Doors' to our Server) ---

@app.get("/")
def read_root():
    """A simple endpoint to confirm the server is running."""
    return {"message": "Hidri Alpha Coordinator is online and operational."}

@app.post("/register_provider", status_code=200)
def register_provider(info: ProviderInfo):
    """Endpoint for a Provider client to announce its availability to the network."""
    provider_id = info.provider_id
    PROVIDERS[provider_id] = info.dict()
    if provider_id not in LEDGER:
        LEDGER[provider_id] = 0.0
        print(f"✅ [REGISTRATION] New provider '{provider_id}' registered. Ledger created.")
    else:
        print(f"✅ [REGISTRATION] Known provider '{provider_id}' re-registered.")
    return {"message": f"Provider {provider_id} registered successfully."}

@app.post("/submit_task", status_code=201)
def submit_task(task: Task):
    """Endpoint for a Creator client to submit a new training task."""
    global TASK_ID_COUNTER
    TASK_ID_COUNTER += 1
    task_id = f"task_{TASK_ID_COUNTER:03d}"
    TASKS[task_id] = task.dict()
    TASK_QUEUE.append(task_id)
    print(f"📥 [TASK SUBMITTED] Task '{task_id}' from '{task.creator_id}' received and queued.")
    return {"message": "ML task submitted successfully.", "task_id": task_id}

@app.get("/get_task/{provider_id}")
def get_task(provider_id: str):
    """Endpoint for a Provider to request a task from the queue."""
    if provider_id not in PROVIDERS:
        raise HTTPException(status_code=404, detail="Provider not registered. Please register first.")
    if not TASK_QUEUE:
        return {"message": "No tasks currently available."}
    
    task_id = TASK_QUEUE.pop(0)
    task_details = TASKS[task_id]
    print(f"📤 [TASK ASSIGNED] Assigning ML task '{task_id}' to provider '{provider_id}'.")
    return {"task_id": task_id, "task_details": task_details}

@app.post("/submit_result", status_code=200)
def submit_result(result: TaskResult):
    """Endpoint for a Provider to submit results and be rewarded."""
    provider_id = result.provider_id
    if provider_id not in LEDGER:
        raise HTTPException(status_code=404, detail="Provider not registered.")
    
    improvement = result.accuracy_after - result.accuracy_before
    # The dynamic reward function: a base reward plus a bonus for performance.
    reward = 5.0 + (improvement * 100)
    LEDGER[provider_id] += reward
    
    print(f"📝 [RESULT RECEIVED] Result for '{result.task_id}' from '{provider_id}'.")
    print(f"    - Accuracy Improvement: {improvement:.2%}")
    print(f"    - Awarding {reward:.2f} Test-HDRI. New Balance: {LEDGER[provider_id]:.2f}")
    
    return {"message": "Result processed and dynamic reward allocated."}

@app.get("/ledger")
def get_ledger():
    """An admin endpoint to view the current state of all provider rewards."""
    return {"hidri_alpha_ledger": LEDGER}