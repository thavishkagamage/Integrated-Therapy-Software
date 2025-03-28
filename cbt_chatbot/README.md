### If you have completed these instructions before:
1. Launch the React client and python server from one terminal
    ```bash
    npm run dev
    ```

    - Your terminal `cwd` must be in the `/front-end` directory. Use `--prefix` to run from any other directory

      ```bash
      npm --prefix ./path/to/front-end/ run dev
      ```

    - To run from  the root of the project

      ```bash
      npm --prefix ./cbt_chatbot/front-end/ run dev
      ```


## Startup Instructions

This section provides detailed instructions for setting up and running the Integrated Therapy Software project. Follow these steps to install the necessary dependencies, initialize the Django application, and start both the backend and frontend servers.

### Prerequisites

1. **Install Python**
    - Download Python 3.13 [HERE](https://www.python.org/downloads/release/python-3130/)
2. **Install Node.js**
    - Download Node.js [HERE](https://nodejs.org/en/download/prebuilt-installer)

### Backend Setup

1. **Install Python Dependencies:**
    ```bash
    pip install Django
    pip install openAI
    ```

2. **Initialize Django Application:**
    ```bash
    python manage.py startapp chatbot
    ```

3. **Run the Django Development Server:**
    ```bash
    python manage.py runserver
    ```

### Frontend Setup

1. **Create a second terminal**
    Hit the + button on the terminal

2. **Navigate to the Frontend Directory:**
    ```bash
    cd front-end
    ```

3. **Install JavaScript Dependencies:**
    ```bash
    npm install
    ```

4. **Start the Frontend Development Server:**
    ```bash
    npm start
    ```

By following these steps, you will have both the backend and frontend servers running, allowing you to work on the Integrated Therapy Software project.

### Shortened:

- pip install Django
- pip install openAI
- python manage.py startapp chatbot
- python manage.py runserver
---
- cd chatbot_frontend
- npm install
- npm start



###
https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#download-for-windows
