# Scalable URL Shortener Service

This project is a full-stack URL shortener built as part of the PromptCloud technical assignment.  
It allows users to convert long URLs into short links, redirect using the short links, and view basic analytics such as click count and creation time.

The application includes a minimal frontend interface, a REST-based backend API, and persistent data storage.

---

## Features

- Generate short URLs for long links
- Redirect short URLs to original URLs
- Optional expiry time for short links
- Optional custom alias support
- Click count analytics for each short URL
- Basic rate limiting to prevent abuse
- Simple, clean frontend UI
- Persistent storage using SQLite

In addition to core requirements, basic rate limiting and custom alias support were implemented as enhancements.

---

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

### Frontend
- HTML
- CSS
- JavaScript (Vanilla)

---

## Project Structure

```text
promptcloud-url-shortener/
├── backend/
│   ├── database/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   └── main.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── DESIGN.md
├── README.md
├── requirements.txt
└── urls.db

```

## Deployment

### 1. Prerequisites

- Python **3.9 - 3.12** (Python 3.13+ is not supported due to SQLAlchemy compatibility)
- pip (Python package manager)
- Any modern web browser (Chrome, Firefox, Edge)

### 2. Clone the Repository

```bash
git clone https://github.com/samridhya004/Scalable-URL-Shortener-Service
cd Scalable-URL-Shortener-Service
```

### 3. Create and Activate Virtual Environment

#### Windows (CMD Prompt)
```bash
python -m venv venv
venv\Scripts\activate
```
#### macOS / Linux (Terminal Prompt)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Backend Server

```bash
uvicorn backend.main:app --reload
```

Once started, the backend will be available at:

#### Backend API:
```bash
http://127.0.0.1:8000
```

#### Swagger API Docs:
```bash
http://127.0.0.1:8000/docs
```

### 6. Run the Frontend

#### Windows 

```bash
start frontend/index.html
```
#### MacOS 

```bash
open frontend/index.html
```

The frontend communicates with the backend running on localhost:8000

---

## API Endpoints Overview

### Create Short URL

```bash
POST /shorten
```

Request Body (JSON):

```json
{
  "long_url": "https://example.com",
  "expiry_minutes": 60,
  "custom_alias": "my-link"
}
```

### Redirect

```bash
GET /{short_code}
```

Redirects to the original URL if valid and not expired.

### Analytics

```bash
GET /stats/{short_code}
```

Returns click count and creation timestamp for the short URL.

---

## Manual Testing

The application can be tested manually using the browser or Swagger UI.

### Create Short URL:
- Open http://127.0.0.1:8000/docs
- Use the `POST /shorten` endpoint
- Provide a valid `long_url`
- Optionally provide `expiry_minutes` and `custom_alias`

### Redirect Test:
- Copy the generated short URL
- Paste it into a browser
- Verify that it redirects to the original URL

### Analytics Test:
- Open `GET /stats/{short_code}`
- Verify that the click count increases after each redirect

---

## Design Decisions

- SQLite is used for simplicity and ease of setup.

- Frontend is intentionally kept minimal as per assignment instructions.

- No authentication is implemented since it was not required.

- Rate limiting is implemented in-memory to prevent excessive requests.

- Detailed architectural decisions are documented in DESIGN.md.

---

## Assumptions & Notes

- The application is intended for local/demo usage.

- Rate limiting resets on server restart.

- Frontend is served separately from the backend.

- Error handling is focused on clarity rather than verbosity.

---

## Author

**Samridhya Khajuria**