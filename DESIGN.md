# Design Document – Scalable URL Shortener Service

## 1. Overview

This project implements a full-stack URL shortener service that converts long URLs into compact, unique short links using a REST API. When a short link is accessed, the system redirects the user to the original URL and records usage metrics such as click count. A minimal frontend is provided to interact with the service.

The system is designed to be simple, modular, and easy to extend while meeting the functional and technical constraints mentioned in the assignment.

---

## 2. Algorithm Choice

### Short Code Generation

The short URL is generated using an alphanumeric Base62 character set:

A random string of fixed length (6 characters) is generated for each new URL. This approach provides:
- A large address space (62⁶ combinations)
- Short, human-readable URLs
- Constant-time generation

Instead of hashing the full URL (for example using MD5 or SHA), a random Base62 identifier is used. This keeps the generated URLs shorter and more readable, while uniqueness is still guaranteed through database constraints and collision checks.

### Collision Handling

To handle potential collisions:
- The `short_code` column is marked as **UNIQUE** in the database.
- Before insertion, the system checks whether the generated short code already exists.
- In the rare case of a collision detected at the database level, a new code can be generated and retried.
This ensures correctness without significantly impacting performance.

---

## 3. Database Design

### Database Choice

SQLite is used for simplicity and ease of setup. It satisfies the requirement of persistent storage and is sufficient for a prototype-level system.

### Schema Design

The core table stores URL mappings with the following fields:
- `id`: Primary key
- `original_url`: The full URL provided by the user
- `short_code`: Unique identifier used in the shortened URL (indexed)
- `clicks`: Number of times the short URL was accessed
- `created_at`: Timestamp when the record was created
- `expires_at`: Optional expiration timestamp

An index on `short_code` ensures fast lookup during redirection and analytics retrieval.

---

## 4. Backend Architecture

The backend is built using FastAPI and follows a modular structure:
- **Routes** handle HTTP requests and responses
- **Models** define database schemas
- **Database layer** manages sessions and persistence
- **Utilities** handle validation logic

### API Endpoints
- `POST /shorten`: Validates input, generates a short URL, and stores it
- `GET /{shortCode}`: Redirects to the original URL and increments click count
- `GET /stats/{shortCode}`: Returns analytics data for a short URL

Standard HTTP status codes are used for error handling (400, 404, 410, 429).

---

## 5. Frontend Design

The frontend is intentionally minimal and lightweight:
- Plain HTML, CSS, and JavaScript
- Input fields for long URL, optional expiry, and custom alias
- Displays generated short URL with copy-to-clipboard functionality
- Shows basic analytics (click count and creation time)

The frontend communicates with the backend using fetch-based REST calls.

---

## 6. Scalability Considerations

If this system were to scale to millions of requests per day, the following improvements could be applied:
- Replace SQLite with a distributed database (PostgreSQL, DynamoDB)
- Introduce caching (Redis) for frequently accessed short URLs
- Use load balancers to distribute traffic across multiple backend instances
- Apply database sharding based on short code hash ranges
- Add asynchronous logging for analytics updates

The current architecture allows these changes without major refactoring.

---

## 7. Summary

This project demonstrates a complete URL shortener system with backend APIs, persistent storage, analytics tracking, and a functional frontend. The design emphasizes clarity, correctness, and extensibility while staying within the scope of the assignment.
