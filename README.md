# 🌐 Universal AI Language Translator

This project is a powerful and scalable text translation application. It features a modern web interface built with HTML, CSS, and JavaScript, and a robust backend powered by Python's FastAPI framework. The core of the translation is handled by the Hugging Face `transformers` library, which allows for high-quality, AI-powered translations between hundreds of languages.

A key feature of this application is its **on-demand model loading**. Instead of loading every language model at startup (which would consume a massive amount of memory), the backend dynamically downloads and caches models only when they are first requested. This makes the application lightweight, fast to start, and infinitely scalable to new languages.

---

### ## 🚀 Features

-   **Universal Translation**: Translate text between hundreds of languages.
-   **Dynamic Model Loading**: The backend only loads language models when they are needed, keeping the application lightweight.
-   **Smart Language Detection**: Automatically detects the source language but also allows for manual override.
-   **Intelligent Fallback**: If a direct translation model isn't available, it defaults to using English as a bridge.
-   **Modern Tech Stack**: Built with a fast and efficient FastAPI backend and a clean, responsive HTML/JS frontend.

---

### ## 🛠️ Technology Stack

-   **Backend**:
    -   Python 3.11.9
    -   FastAPI (for the web server)
    -   Uvicorn (as the ASGI server)
    -   Hugging Face `transformers` (for the translation models)
    -   `langdetect` (for automatic language detection)
-   **Frontend**:
    -   HTML5
    -   CSS3
    -   Vanilla JavaScript

---

### ## ⚙️ How to Run the Project

Follow these steps to get the translator running on your local machine.

#### **1. Set up the Backend**

First, navigate into the `backend` directory from your terminal:
```bash
cd path/to/your/translator-app/backend
```

Create and activate a Python virtual environment. This keeps the project's dependencies isolated.

-   **On Windows**:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```
-   **On macOS / Linux**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

Install all the required Python libraries:
```bash
pip install -r requirements.txt
```

Finally, start the backend server using Uvicorn:
```bash
uvicorn main:app --reload
```
The server will start and be available at `http://127.0.0.1:8000`. Keep this terminal window open.

#### **2. Launch the Frontend**

Navigate to the `frontend` directory in your file explorer and open the `index.html` file in your favorite web browser (like Chrome, Firefox, or Edge).

That's it! The application should now be fully functional.
