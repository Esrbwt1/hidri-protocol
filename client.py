# client.py (Version 2.1)

import typer
import requests
import time
import random
import os
import numpy as np
import tensorflow as tf
from rich.console import Console
from rich.table import Table
from rich.live import Live

# --- Setup ---
app = typer.Typer()
console = Console()
COORDINATOR_URL = "http://127.0.0.1:8000"
STATE = {
    "provider_id": f"provider_{random.randint(100, 999)}",
    "status": "Starting...", "tasks_completed": 0, "current_task": "None",
    "test_hdri_earned": 0.0, "last_accuracy": "N/A",
}

# --- UI Helper ---
def generate_dashboard() -> Table:
    # ... (This function is unchanged)
    table = Table(title=f"Hidri Alpha Provider Client v2.1 (ID: {STATE['provider_id']})")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("Status", STATE["status"])
    table.add_row("Current Task ID", STATE["current_task"])
    table.add_row("Last Known Model Accuracy", STATE["last_accuracy"])
    table.add_row("Tasks Completed", str(STATE["tasks_completed"]))
    table.add_row("Test-HDRI Earned", f"{STATE['test_hdri_earned']:.2f}")
    table.add_row("[bold green]Privacy Guarantee[/bold green]", "Your local data is being used for training ON THIS DEVICE ONLY.")
    return table

# --- ML Helpers ---
def create_simple_model():
    # ... (This function is unchanged)
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10)
    ])
    return model

def load_local_data():
    # ... (This function is unchanged)
    images, labels = [], []
    data_dir = os.path.join("local_data", "digit_7")
    if not os.path.exists(data_dir): return None, None
    for filename in os.listdir(data_dir):
        img_path = os.path.join(data_dir, filename)
        img = tf.keras.preprocessing.image.load_img(img_path, color_mode='grayscale', target_size=(28, 28))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        images.append(img_array)
        labels.append(7)
    return np.array(images), np.array(labels)

# --- Main Command ---
@app.command()
def provide():
    """Puts the client into 'Provider' mode for real ML tasks."""
    console.rule("[bold blue]Hidri Provider Client Initializing...[/bold blue]")
    # 1. Register with the coordinator
    try:
        requests.post(f"{COORDINATOR_URL}/register_provider", json={"provider_id": STATE['provider_id'], "address": "local"}).raise_for_status()
        STATE['status'] = 'Registered & Idle'
        console.print(f"✅ Successfully registered with coordinator as [bold]{STATE['provider_id']}[/bold]")
    except requests.exceptions.RequestException as e:
        console.print(f"❌ [FATAL] Could not register with coordinator. Is it running? Aborting.")
        console.print(f"    Error: {e}")
        return

    # 2. Load local data
    console.print("💾 Loading local provider data...")
    local_images, local_labels = load_local_data()
    if local_images is None:
        console.print("❌ [FATAL] No local data found. Run `python prepare_data.py` first. Aborting.")
        return
    local_images = local_images / 255.0
    console.print(f"    Found {len(local_images)} images.")

    # 3. Main Provider Loop
    console.rule("[bold blue]Starting Main Loop - Listening for Tasks[/bold blue]")
    with Live(generate_dashboard(), screen=True, redirect_stderr=False, refresh_per_second=4) as live:
        while True:
            try:
                # Ask for a task
                response = requests.get(f"{COORDINATOR_URL}/get_task/{STATE['provider_id']}")
                task = response.json()

                if "task_id" in task:
                    # Task received, begin processing
                    process_task(task, local_images, local_labels)
                else:
                    # No tasks available
                    STATE['status'] = 'Idle - No tasks available.'
                    live.update(generate_dashboard())
                    time.sleep(5)

            except requests.exceptions.RequestException:
                STATE['status'] = "[bold red]Error: Connection to coordinator lost.[/bold red]"
                live.update(generate_dashboard())
                time.sleep(10)
            except KeyboardInterrupt:
                console.rule("[bold yellow]Shutdown signal received. Exiting.[/bold yellow]")
                break

def process_task(task, local_images, local_labels):
    """The core logic for handling a single ML task."""
    task_id = task['task_id']
    details = task['task_details']
    STATE['current_task'] = task_id
    STATE['status'] = f"🏗️ Reconstructing model for {task_id}"

    # Reconstruct and compile the model from the creator's definition
    model = tf.keras.models.model_from_json(details['model_json'])
    model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
    
    # Evaluate accuracy BEFORE training
    _, acc_before = model.evaluate(local_images, local_labels, verbose=0)
    STATE['last_accuracy'] = f"{acc_before:.2%}"
    STATE['status'] = f"💪 Training {task_id} on local data..."

    # DO THE REAL WORK
    model.fit(local_images, local_labels, epochs=details['epochs'], verbose=0)

    # Evaluate accuracy AFTER training
    _, acc_after = model.evaluate(local_images, local_labels, verbose=0)
    STATE['last_accuracy'] = f"✅ {acc_after:.2%}"
    
    # Submit the result
    STATE['status'] = f"✉️ Submitting result for {task_id}..."
    result_data = {"task_id": task_id, "provider_id": STATE['provider_id'], "accuracy_before": acc_before, "accuracy_after": acc_after}
    requests.post(f"{COORDINATOR_URL}/submit_result", json=result_data)

    # Update state
    STATE['tasks_completed'] += 1
    new_balance = requests.get(f"{COORDINATOR_URL}/ledger").json()['hidri_alpha_ledger'][STATE['provider_id']]
    STATE['test_hdri_earned'] = new_balance
    STATE['current_task'] = "None"

# --- Creator Command ---
@app.command()
def submit_task():
    """Simulates a Creator submitting a real ML task."""
    console.rule("[bold blue]Creator Client: Submitting Task[/bold blue]")
    model = create_simple_model()
    task_data = {"creator_id": "creator_007", "model_json": model.to_json(), "epochs": 5}
    try:
        response = requests.post(f"{COORDINATOR_URL}/submit_task", json=task_data)
        response.raise_for_status()
        console.print("✅ [SUCCESS] ML Task submitted successfully!")
        console.print(f"   Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        console.print(f"❌ [FAILURE] Could not submit task to coordinator. Error: {e}")

if __name__ == "__main__":
    app()