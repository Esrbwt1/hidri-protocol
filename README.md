# Hidri Alpha MVP v0.2.0

## 1. Vision: A New Foundation for AI

**Hidri** is a protocol designed to build a new foundation for Artificial Intelligence. Our mission is to decentralize the development of AI, moving it from closed, centralized silos into an open, transparent, and collaborative ecosystem.

In the current paradigm, only large corporations with massive, private datasets can build advanced AI. Hidri shatters this model by creating a global, decentralized network where:

-   **AI models** are sent to data, not the other way around.
-   **User data** remains private and secure on the user's own device.
-   **Providers** of data and computation are fairly rewarded for the value they contribute.
-   **Creators** of AI can have their models trained by a global supercomputer, paying only for the results they need.

This project, the **Hidri Alpha MVP**, is the first working prototype of the Hidri protocol. It is a proof-of-concept that validates the core technical thesis of incentivized, federated machine learning.

## 2. What This MVP Proves

This codebase successfully demonstrates the entire end-to-end workflow of the Hidri protocol in a simulated, local environment.

1.  A **Coordinator** server acts as the central task manager.
2.  A **Creator** can define a real TensorFlow/Keras AI model and submit it for training.
3.  A **Provider** can connect to the network, receive the model, and train it using its own local data, without that data ever being uploaded.
4.  The Provider is **dynamically rewarded** in "Test-HDRI" tokens based on the measurable improvement it provides to the model's accuracy.

## 3. Technology Stack

-   **Language:** Python 3
-   **Protocol Simulation:** FastAPI
-   **Client Interface (CLI):** Typer
-   **Live Dashboard UI:** Rich
-   **Machine Learning Engine:** TensorFlow 2 / Keras

## 4. How to Run This MVP

### Step A: Prerequisites

-   Python 3.10+
-   A terminal or command-line interface

### Step B: Setup

1.  **Clone the project (or download the source code).**

2.  **Create and activate a virtual environment:**
    ```bash
    # Create the environment
    python -m venv venv
    # Activate on macOS/Linux
    source venv/bin/activate
    # Activate on Windows
    venv\Scripts\activate
    ```

3.  **Install the required libraries:**
    ```bash
    pip install "fastapi[all]" "typer[all]" "rich" "tensorflow" "requests"
    ```

4.  **Prepare the sample provider data:**
    ```bash
    python prepare_data.py
    ```

### Step C: Running the Simulation

You will need three separate terminals, all with the virtual environment activated.

1.  **Terminal 1: Start the Coordinator**
    ```bash
    uvicorn coordinator:app --reload
    ```

2.  **Terminal 2: Start the Provider Client**
    ```bash
    python client.py provide
    ```
    *This will open the live provider dashboard.*

3.  **Terminal 3: Start the Creator Client**
    ```bash
    python client.py submit-task
    ```
    *This will submit the ML task to the coordinator.*

4.  **Observe:** Watch as the task is assigned in Terminal 1, the work is performed in Terminal 2 (you'll see the accuracy increase), and the rewards are allocated.

## 5. Next Steps

This MVP is the foundational proof. The next phase of the project will focus on:

-   Replacing the centralized Coordinator with a decentralized system (e.g., smart contracts).
-   Implementing more robust cryptographic checks and balances.
-   Growing the community of developers and providers.

---