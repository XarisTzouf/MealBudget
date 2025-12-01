# MealBudget - Thesis Project

**Vibe Coding Effectiveness Study Case Study**

MealBudget is a full-stack web application designed to generate optimized weekly meal plans based on user-defined budgets and nutritional goals. It utilizes a constraint satisfaction algorithm to select meals while adhering to cost and calorie limits.

---

## 🛠 Tech Stack

### Backend
* **Language:** Python 3.10+
* **Framework:** FastAPI
* **Database:** SQLite (with SQLAlchemy ORM)
* **Optimization:** Custom constraint satisfaction algorithm (Budget & Macros)

### Frontend
* **Framework:** Flutter (Web)
* **State Management:** Riverpod
* **Navigation:** GoRouter
* **HTTP Client:** Dio
* **Charts:** Fl_Chart

---

## 🚀 How to Run the Project

### Part 1: Backend Setup (Python)

1.  Open a terminal and navigate to the backend folder:
    ```powershell
    cd MealbudgetBackend
    ```

2.  Create a virtual environment (if not already created):
    ```powershell
    python -m venv .venv
    ```

3.  Activate the virtual environment:
    ```powershell
    .\.venv\Scripts\activate
    ```

4.  Install required dependencies:
    ```powershell
    pip install -r requirements.txt
    ```

5.  **Initialize & Seed the Database:**
    *(This script creates the database schema and populates it with sample food data like Breakfast, Main, Snacks)*
    ```powershell
    python seed.py
    ```

6.  **Start the Server:**
    *(Runs on port 8010 to avoid conflicts)*
    ```powershell
    .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8010

    ```
    > The Backend is now running at: `http://127.0.0.1:8010`

---

### Part 2: Frontend Setup (Flutter)

1.  Open a **new** terminal window and navigate to the frontend folder:
    ```powershell
    cd mealbudget_frontend
    ```

2.  Install Flutter dependencies:
    ```powershell
    flutter pub get
    ```

3.  **Run the Web App:**
    ```powershell
    flutter run -d web-server
    ```

4.  Open the URL provided in the terminal (usually `http://localhost:xxxx`) in your Chrome browser.

---

##  Testing the Optimization

1.  Click **"Let's Start"** on the Home Page.
2.  Enter your parameters (e.g., **Budget: 80€**, **Calories: 2200**).
3.  Click **"Generate Plan"**.
4.  The system will calculate a weekly schedule including Breakfast, Lunch, and Dinner within your budget.