To complete your **Junior DevOps Engineer** assignment for **ACEest Fitness & Gym**, you need a professional `README.md` that explains the transition from the legacy desktop logic into a modern, containerized **Flask** application.

Copy and paste the following content into a file named `README.md` in your GitHub repository root.

---

# ACEest Fitness & Gym – DevOps Infrastructure

## 📌 Project Overview
This repository contains the containerized **Flask Web API** for **ACEest Fitness & Gym**. As part of the DevOps transition, the original Python desktop application was refactored into a scalable web service. 

This project demonstrates a full **CI/CD Lifecycle**, utilizing **GitHub Actions** for automated testing and **Jenkins** for build orchestration, ensuring that every code change is verified and deployable.

---

## 🛠 Local Setup and Execution

### Prerequisites
* **Python 3.9+**
* **Docker Desktop** (to run via container)

### 1. Manual Installation (Development Mode)
1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/aceest-fitness-devops.git
    cd aceest-fitness-devops
    ```
2.  **Set up Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the App:**
    ```bash
    python app.py
    ```
    *The API will be available at `http://localhost:5000`.*

### 2. Docker Execution (Production Mode)
To ensure environmental consistency, run the application using the provided Dockerfile:
```bash
# Build the image
docker build -t aceest-fitness-app .

# Run the container
docker run -p 5000:5000 aceest-fitness-app
```

---

## 🧪 Automated Testing
We use **Pytest** to ensure application stability before deployment.

### How to Run Tests Manually:
Ensure your virtual environment is active, then run:
```bash
pytest test_app.py -v
```
**Test Coverage Includes:**
* **API Health:** Verifying the `/status` endpoint returns a `200 OK`.
* **Database Integrity:** Ensuring the SQLite database initializes and retrieves member data without errors.
* **Environmental Check:** Confirming the app runs "headless" (without GUI/Tkinter dependencies).

---

## ⚙️ CI/CD Integration Logic
The ACEest Fitness pipeline follows the **"Shift Left"** testing principle—identifying bugs as early as possible in the development cycle.

### 1. GitHub Actions (The Quality Gate)
Configured in `.github/workflows/main.yml`, this pipeline triggers on every **Push** or **Pull Request**.
* **Build & Lint:** Installs dependencies and checks for syntax errors.
* **Automated Testing:** Runs the Pytest suite in a headless Linux container.
* **Docker Assembly:** Verifies that the Docker image builds successfully.
* **Result:** If any stage fails, the code is blocked from merging to the main branch.

### 2. Jenkins (The Build Orchestrator)
The **Jenkins** environment handles the final assembly and delivery on the local build server.
* **Trigger:** Jenkins monitors the repository and triggers a build once GitHub Actions reports a "Success."
* **Action:** It pulls the verified code, builds the production-grade Docker image using `python:3.9-slim` for maximum efficiency, and prepares it for deployment.
<img width="1895" height="945" alt="image" src="https://github.com/user-attachments/assets/1fbbbd33-6aee-4142-b135-cbc367807e00" />
