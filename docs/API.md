# API Documentation

## Overview

The Crop Disease Detection System is primarily a server-rendered web application. The main interaction is through HTML forms and page navigation. This document describes the endpoints available.

## Base URL

```
http://127.0.0.1:5000
```

## Authentication

Most routes require authentication. Users must log in via `/login`. Session-based authentication is used (Flask-Login).

Admin routes require `user_type = 'admin'`.

## Endpoints

### Public

#### GET /
Landing page. No authentication required.

#### GET /register
Registration form.

#### POST /register
Create new user.

| Field | Type | Required |
|-------|------|----------|
| full_name | string | No |
| email | string | Yes |
| password | string | Yes |
| phone | string | No |
| location | string | No |

#### GET /login
Login form.

#### POST /login
Authenticate user.

| Field | Type | Required |
|-------|------|----------|
| email | string | Yes |
| password | string | Yes |

### Authenticated (Farmer)

#### GET /dashboard
User dashboard with stats and recent predictions.

#### GET /upload
Upload form for leaf image.

#### POST /upload
Upload leaf image and run prediction.

| Field | Type | Required |
|-------|------|----------|
| file | file (image) | Yes |

Allowed: JPG, PNG. Max 5MB.

Redirects to `/results/<prediction_id>` on success.

#### GET /results/<prediction_id>
View prediction result with treatment recommendations.

#### GET /history
List user's past predictions.

#### POST /feedback/<prediction_id>
Submit feedback for a prediction.

| Field | Type | Required |
|-------|------|----------|
| accuracy_rating | int (1-5) | No |
| feedback | string | No |

### Admin

#### GET /admin
Admin dashboard (user count, prediction count, model metrics).

#### GET /admin/metrics
Model metrics and confusion matrix.

#### GET /admin/predictions?page=1
Paginated list of all predictions.

#### GET /admin/users
List all users.

#### GET /admin/diseases
List all diseases in knowledge base.

#### GET /admin/diseases/add
Form to add new disease.

#### POST /admin/diseases/add
Create disease.

#### GET /admin/diseases/edit/<id>
Edit disease form.

#### POST /admin/diseases/edit/<id>
Update disease.

#### POST /admin/diseases/delete/<id>
Delete disease.

## Response Formats

HTML responses use Jinja2 templates. Flash messages indicate success/error.

For future REST API extension, consider JSON responses with structure:

```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message"
}
```
