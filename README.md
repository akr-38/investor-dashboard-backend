
# Investor Dashboard - Backend API

This repository hosts the backend for the Investor Dashboard, providing RESTful APIs to serve vehicle registration data from a PostgreSQL database. It is built using FastAPI and SQLAlchemy.
This is just a part of the whole investor dashboard project: **[Investor Dashboard Project](https://github.com/akr-38/investors-dashboard-project/blob/main/README.md)**

## ⚙️ Tech Stack

  * **Framework:** FastAPI
  * **Web Server:** Uvicorn
  * **Database ORM:** SQLAlchemy
  * **Database Driver:** `psycopg2-binary`
  * **Migrations:** Alembic
  * **Environment Management:** `python-dotenv`
  * **Data Validation:** Pydantic

-----

## 🛠️ Getting Started

Follow these steps to set up the backend and run the API server.

### Prerequisites

  * **Python 3.9+**
  * **A running PostgreSQL database** (e.g., your Supabase instance) with the data already populated using the [Scraper and Storing](https://github.com/akr-38/investor-dashboard-scraping-and-storing) repository.

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/akr-38/investor-dashboard-backend.git
cd investor-dashboard-backend
```

### Step 2: Set up the Python Environment

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Step 3: Install Dependencies

Install the required Python packages:

```bash
pip install "uvicorn[standard]" fastapi sqlalchemy psycopg2-binary alembic python-dotenv pydantic
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project's root directory and add your database connection string. This is a crucial step to ensure the backend can communicate with the database.

```ini
# .env
DATABASE_URL="postgresql://<user>:<password>@<host>:<port>/<dbname>"
```

### Step 5: Configure Alembic Migrations

Since the database was already created and populated by the scraper repository, you need to tell Alembic that the database is up-to-date.

1.  Copy the migration file from the scraper project: Navigate to `investor-dashboard-scraping-and-storing/migrations/versions/` and copy the migration file (e.g., `<some_id>_initial_tables.py`).

2.  Paste this file into your backend's migration folder: `investor-dashboard-backend/migrations/versions/`.

3.  Stamp the database to mark it as current:

    ```bash
    alembic stamp head
    ```

-----

## ⚡ API Endpoints

The backend exposes several `POST` endpoints to fetch aggregated vehicle registration data. The `Details` model in each endpoint is used to specify the date range, category, or manufacturer for the query.

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/all_categories_all_manufacturers` | `POST` | Aggregates and returns the sum of vehicle registrations across all categories and manufacturers for a given date range. |
| `/all_categories_specific_manufacturer` | `POST` | Finds and aggregates data for a specific company across all vehicle categories. |
| `/specific_category_all_manufacturers` | `POST` | Finds and aggregates data for a specific vehicle category across all manufacturers. |
| `/specific_category_specific_manufacturer` | `POST` | Finds and aggregates data for a specific vehicle category and a specific manufacturer. |

-----

## 🖥️ Running the Server

Once everything is configured, run the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```

The `--reload` flag is useful for development as it automatically reloads the server on code changes. Your API will be available at `http://127.0.0.1:8000`. You can test the endpoints using a tool like Postman or the automatically generated interactive documentation at `http://127.0.0.1:8000/docs`.
