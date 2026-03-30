# Habit Tracker System Design

## High-Level Architecture

- **Frontend:** React (served via AWS S3 + CloudFront)
- **Backend:** FastAPI (deployed on AWS ECS, Lambda, or EC2)
- **Database:** PostgreSQL (AWS RDS)
- **Authentication:** JWT-based (optionally AWS Cognito)
- **Storage:** AWS S3 (for user-uploaded files, if needed)
- **CI/CD:** GitHub Actions or AWS CodePipeline
- **Monitoring & Logging:** AWS CloudWatch, Sentry, etc.

### Diagram (Text)

```
[React Frontend] <---> [FastAPI Backend] <---> [PostgreSQL DB]
        |                      |                     |
        |                      |                     |
    [AWS S3]           [Authentication]         [AWS RDS]
        |                      |
   [CloudFront]           [CloudWatch]
```

### Diagram (Pictorial)

```mermaid
graph TD
    A[React Frontend (S3/CloudFront)] -->|HTTPS| B(FastAPI Backend)
    B -->|SQL| C[PostgreSQL (AWS RDS)]
    B -->|Auth| D[JWT / Cognito]
    B -->|File Upload| E[AWS S3]
    B -->|Monitoring| F[AWS CloudWatch]
    B -->|CI/CD| G[GitHub Actions / CodePipeline]
```

## API Structure

- `POST   /auth/register` — Register new user
- `POST   /auth/login` — User login, returns JWT
- `GET    /habits/` — List habits
- `POST   /habits/` — Create habit
- `GET    /habits/{habit_id}` — Retrieve habit
- `PUT    /habits/{habit_id}` — Update habit
- `DELETE /habits/{habit_id}` — Delete habit
- `POST   /habits/{habit_id}/track` — Track habit completion
- `GET    /users/me` — Get current user profile

## Database Schema

### users
- id (PK)
- email (unique)
- hashed_password
- created_at
- updated_at

### habits
- id (PK)
- user_id (FK to users.id)
- name
- description
- created_at
- updated_at

### habit_tracking
- id (PK)
- habit_id (FK to habits.id)
- date
- completed (bool)
- note
