# Todo Backend API

A complete backend for a Todo application using FastAPI with JWT authentication and SQLite database.

## Features

- ✅ JWT-based authentication (login + register)
- ✅ User management with secure password hashing
- ✅ User-specific todo CRUD operations
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Pydantic schemas for request/response validation
- ✅ Clean code structure with separation of concerns

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token

### Todos (Requires Authentication)
- `GET /todos` - Get all user's todos
- `POST /todos` - Create a new todo
- `GET /todos/{id}` - Get a specific todo
- `PUT /todos/{id}` - Update a specific todo
- `DELETE /todos/{id}` - Delete a specific todo

### Other
- `GET /` - Welcome message
- `GET /health` - Health check

## Usage Examples

### 1. Register a new user
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### 3. Create a todo (with Bearer token)
```bash
curl -X POST "http://localhost:8000/todos" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Complete project",
    "description": "Finish the todo backend API",
    "completed": false
  }'
```

### 4. Get all todos
```bash
curl -X GET "http://localhost:8000/todos" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Database Models

### User
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email
- `hashed_password`: Bcrypt hashed password
- `created_at`: Timestamp

### Todo
- `id`: Primary key
- `title`: Todo title
- `description`: Optional description
- `completed`: Boolean status
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `user_id`: Foreign key to User

## Security Features

- Password hashing with bcrypt
- JWT tokens for authentication
- User-specific data isolation
- Input validation with Pydantic
- CORS middleware for cross-origin requests

## File Structure

```
Todo-Backend/
├── main.py          # FastAPI app and configuration
├── models.py        # SQLAlchemy database models
├── database.py      # Database configuration
├── schemas.py       # Pydantic request/response models
├── crud.py          # Database operations
├── auth.py          # Authentication utilities
├── routes.py        # API route handlers
├── requirements.txt # Python dependencies
├── .env            # Environment variables
└── README.md       # This file
```

## Environment Variables

Create a `.env` file with:

```
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./todo.db
HOST=0.0.0.0
PORT=8000
```

## Production Deployment

For production deployment:

1. Change the `SECRET_KEY` to a strong random string
2. Use a production database (PostgreSQL, MySQL, etc.)
3. Set up proper CORS origins instead of allowing all (`*`)
4. Use environment variables for all configuration
5. Set up proper logging
6. Use a production ASGI server like Gunicorn with Uvicorn workers