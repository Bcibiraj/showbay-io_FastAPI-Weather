# FastAPI Weather Assessment

A RESTful API built using **FastAPI**, **SQLAlchemy**, and **PostgreSQL** that fetches real-time weather data from a third-party API (OpenWeatherMap) and stores it in a database. The project includes robust CRUD operations, validation, error handling, and automated testing with Pytest.

---

## 1️ Problem Understanding & Assumptions

###  Interpretation

The objective is to build a backend service that:
- Fetches weather data from an external API.
- Persists that data in a database.
- Exposes CRUD APIs to manage the stored records.
- Includes unit and integration tests using Pytest.

###  Use Case
**Weather Data Management System**  
A backend service that allows users to store and manage weather details for a given city using real-time external data.

###  Assumptions (Mandatory)
1. **External API Reliability**  
   - The OpenWeatherMap API is assumed to be available most of the time.
   - If the API is unavailable, the system returns a `503 Service Unavailable`.

2. **Authentication**  
   - No user authentication or authorization is required as it was not specified in the assessment.

3. **City Uniqueness**  
   - Multiple records can exist for the same city at different timestamps.

4. **Weather Data Structure**  
   - API response format is assumed to contain:
     - `main.temp`, `main.humidity`
     - `weather[0].main`
     - `wind.speed`

5. **Update Behavior**  
   - Partial updates are allowed using PUT with only modified fields.

6. **Database Constraints**  
   - Data integrity is ensured via SQLAlchemy schema definitions.

---

## 2️ Design Decisions

###  Database Schema
**Table: `weather`**
| Column      | Type      | Description |
|------------|-----------|-------------|
| id         | Integer   | Primary key |
| city       | String    | Indexed, city name |
| temperature| Float     | Temperature in Celsius |
| humidity   | Float     | Humidity percentage |
| weather    | String    | Weather condition |
| speed      | String    | Wind speed |
| timestamp  | DateTime  | Record creation time |

**Indexes:**  
- `city` field indexed for faster lookup.

---

### Project Structure
app/
│── main.py # FastAPI app & routes
│── models.py # SQLAlchemy models
│── schemas.py # Pydantic schemas
│── crud.py # Database operations
│── database.py # DB connection
│── external.py # External API integration
tests/
│── test_unit.py
│── test_integration.py
│── conftest.py


**Architecture Style:** Layered Architecture  
- API Layer → Business Logic (CRUD) → Database  
- External API layer is isolated in `external.py`.

---

### Validation Logic
- Input validation using **Pydantic schemas**:
- City must have at least 2 characters.
- Business logic validation:
- Record existence checked before update/delete.
- Partial updates supported using `exclude_unset=True`.

---

###  External API Design
- Uses **OpenWeatherMap API**.
- Authentication via API Key stored in environment variables.
- Timeout configured (`5 seconds`).
- Error handling:
- Network/API failure → `503 Service Unavailable`.

---

## 3️ Solution Approach

###  Data Flow
1. **Client Request** → `/weather` with city name.
2. **FastAPI Controller** receives request.
3. **External API Call** → `fetch_weather(city)`.
4. **CRUD Layer** processes and stores data.
5. **Database** commits record.
6. **Response Model** returns stored record.

---

## 4️ Error Handling Strategy

###  Handled Scenarios
|      Scenario      |             Handling                  |
|--------------------|---------------------------------------|
|External API failure | Returns `503 Weather API unavailable` |
|Record not found     | Returns `404 Weather record not found`|
|DB session errors    | Managed by dependency injection       |
|Invalid input        | Automatically handled by Pydantic     |

FastAPI's built-in exception handling is used along with custom HTTPException messages.

---

## 5️ How to Run the Project

###  Setup Instructions

#### 1. Clone the Repository
```bash
git clone <repo-url>
cd fastapi-weather

2. Create Virtual Environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Environment Variables
Create a .env file:

DATABASE_URL=postgresql://postgres:123@localhost:5432/fastapi-weather
WEATHER_API_KEY=your_api_key_here

5. Run the Server
uvicorn app.main:app --reload

API Endpoints
| Method | Endpoint        | Description           |
| ------ | --------------- | --------------------- |
| POST   | `/weather`      | Fetch & store weather |
| GET    | `/weather/{id}` | Retrieve record       |
| PUT    | `/weather/{id}` | Update record         |
| DELETE | `/weather/{id}` | Delete record         |

Testing

Unit Tests
    -CRUD operations tested with a FakeDB.
    -External API mocked using AsyncMock.

Integration Tests
    -API endpoints tested using FastAPI TestClient.
    -Database overridden with SQLite test database.

Run tests:
    pytest

Trade-offs, Limitations & Improvements

Trade-offs
    -No authentication implemented to keep scope minimal.
    -SQLite used for testing instead of PostgreSQL.

Limitations
    -No caching for repeated city queries. 
    -No pagination or filtering.

Improvements  
    -Add authentication (JWT)
    -Add caching (Redis).
    -Implement background tasks for scheduled weather updates.
    -Dockerize application.     
