# FastAPI Industrial Grade Application with Cassandra

A professional, industrial-grade FastAPI application with separated routes and services following enterprise best practices, integrated with Apache Cassandra database.

## 🏗️ Project Structure

```
ADMINDATAGETFROMPY/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py          # Main API router
│   │       └── endpoints/      # API endpoints (routes)
│   │           ├── __init__.py
│   │           ├── health.py
│   │           ├── users.py
│   │           ├── items.py
│   │           ├── sessions.py
│   │           └── games.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Application configuration
│   │   ├── dependencies.py     # Dependency injection
│   │   ├── logging.py          # Logging configuration
│   │   └── database.py         # Cassandra database connection
│   ├── models/                 # SQLAlchemy database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── repositories/           # Data access layer
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   ├── item_repository.py
│   │   ├── session_repository.py
│   │   └── game_repository.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── user.py
│   │   ├── item.py
│   │   ├── session.py
│   │   ├── game.py
│   │   └── contest.py
│   └── services/               # Business logic layer
│       ├── __init__.py
│       ├── health_service.py
│       ├── user_service.py
│       ├── item_service.py
│       ├── session_service.py
│       └── game_service.py
├── logs/                       # Application logs
├── requirements.txt
├── run.py                      # Application runner
├── Dockerfile                  # Container configuration
├── docker-compose.yml          # Multi-service setup
└── README.md
```

## 🚀 Features

- **Clean Architecture**: Separated routes, services, and data access layers
- **Cassandra Integration**: Full integration with Apache Cassandra database
- **Session Management**: Complete session lifecycle management
- **Game Management**: Comprehensive game CRUD operations
- **User Management**: Enhanced user management with mobile/email support
- **Dependency Injection**: Proper service injection using FastAPI dependencies
- **Comprehensive Logging**: Structured logging with file rotation
- **Health Monitoring**: Detailed system health checks
- **Configuration Management**: Environment-based configuration using Pydantic
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Error Handling**: Global exception handling and proper HTTP status codes
- **CORS Support**: Configurable CORS middleware
- **Security**: Trusted host middleware and security headers

## 🛠️ Installation

### Prerequisites

- **Python 3.8+** installed on your system
- **Apache Cassandra** running and accessible
- **Git** for cloning the repository

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ADMINDATAGETFROMPY
   ```

2. **Create virtual environment**

   **On Linux/macOS:**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate
   ```

   **On Windows:**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   venv\Scripts\activate
   ```

   **Alternative for Windows (PowerShell):**
   ```powershell
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   .\venv\Scripts\Activate.ps1
   ```

3. **Verify virtual environment activation**
   
   You should see `(venv)` at the beginning of your command prompt:
   ```bash
   (venv) user@machine:~/ADMINDATAGETFROMPY$
   ```

4. **Upgrade pip (recommended)**
   ```bash
   pip install --upgrade pip
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Setup Cassandra**
   - Ensure Cassandra is running on the configured host
   - The application will automatically create the keyspace and tables

7. **Create environment file**
   ```bash
   # On Linux/macOS
   cp env.example .env
   
   # On Windows
   copy env.example .env
   ```

8. **Verify installation**
   ```bash
   # Check if FastAPI is installed
   python -c "import fastapi; print('FastAPI installed successfully')"
   
   # Check if Cassandra driver is installed
   python -c "import cassandra; print('Cassandra driver installed successfully')"
   ```

### Virtual Environment Management

**To deactivate the virtual environment:**
```bash
deactivate
```

**To reactivate the virtual environment later:**

**On Linux/macOS:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

**To delete and recreate the virtual environment:**
```bash
# Deactivate first
deactivate

# Remove old environment
rm -rf venv  # Linux/macOS
# OR
rmdir /s venv  # Windows

# Create new environment (follow step 2 above)
```

## 🏃‍♂️ Running the Application

### Development Mode
```bash
# Make sure virtual environment is activated
python run.py
```

### Production Mode
```bash
# Make sure virtual environment is activated
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Using Docker
```bash
docker-compose up --build
```

## 📚 API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 🔧 Configuration

The application uses environment variables for configuration. Key settings:

```env
# Project Info
PROJECT_NAME=FastAPI Industrial App
VERSION=1.0.0

# Server Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true

# Security
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Cassandra Configuration
CASSANDRA_HOST=172.31.4.229
CASSANDRA_USERNAME=cassandra
CASSANDRA_PASSWORD=cassandra
CASSANDRA_KEYSPACE=myapp
CASSANDRA_PORT=9042

# Logging
LOG_LEVEL=INFO
```

## 🏗️ Architecture Overview

### Layer Separation

1. **API Layer** (`app/api/`): HTTP endpoints and request/response handling
2. **Service Layer** (`app/services/`): Business logic and orchestration
3. **Repository Layer** (`app/repositories/`): Data access and persistence
4. **Model Layer** (`app/models/`): Database models and ORM
5. **Schema Layer** (`app/schemas/`): Data validation and serialization

### Dependency Flow

```
API Endpoint → Service → Repository → Cassandra
     ↓           ↓          ↓
  Request    Business   Data Access
  Validation   Logic     Operations
```

## 📊 Database Schema

The application automatically creates the following Cassandra tables:

- **users**: User management with mobile/email support
- **sessions**: Session management with device tracking
- **games**: Game catalog with categories and metadata
- **contests**: Contest management
- **server_announcements**: System announcements
- **game_updates**: Game update tracking
- **otp_store**: OTP management
- **league_joins**: League participation tracking

## 🧪 Testing

Run tests using pytest:

```bash
# Make sure virtual environment is activated
pytest
```

## 📊 Monitoring

### Health Checks

- **Basic Health**: `GET /health`
- **Detailed Health**: `GET /api/v1/health/detailed`

### Logging

Logs are written to:
- Console output
- `logs/app.log` (application logs)
- `logs/error.log` (error logs only)

## 🔒 Security Features

- CORS middleware configuration
- Trusted host validation
- Global exception handling
- Request/response logging
- Security headers
- Session token validation

## 🚀 Production Deployment

For production deployment:

1. Set `RELOAD=false`
2. Configure proper `SECRET_KEY`
3. Set up proper Cassandra cluster
4. Configure logging levels
5. Set up reverse proxy (nginx)
6. Use proper WSGI server (gunicorn)

## 📝 API Endpoints

### Users
- `GET /api/v1/users/` - List all users
- `GET /api/v1/users/{user_id}` - Get user by ID
- `GET /api/v1/users/mobile/{mobile_no}` - Get user by mobile
- `GET /api/v1/users/email/{email}` - Get user by email
- `POST /api/v1/users/` - Create new user
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### Sessions
- `GET /api/v1/sessions/` - Get user sessions
- `GET /api/v1/sessions/active` - Get active session
- `POST /api/v1/sessions/` - Create new session
- `PUT /api/v1/sessions/` - Update session
- `DELETE /api/v1/sessions/` - Deactivate session
- `POST /api/v1/sessions/refresh` - Refresh session
- `POST /api/v1/sessions/validate` - Validate session

### Games
- `GET /api/v1/games/` - List all games
- `GET /api/v1/games/active` - List active games
- `GET /api/v1/games/featured` - List featured games
- `GET /api/v1/games/category/{category}` - Games by category
- `GET /api/v1/games/{game_id}` - Get game by ID
- `POST /api/v1/games/` - Create new game
- `PUT /api/v1/games/{game_id}` - Update game
- `DELETE /api/v1/games/{game_id}` - Delete game
- `POST /api/v1/games/{game_id}/toggle-status` - Toggle game status
- `POST /api/v1/games/{game_id}/toggle-featured` - Toggle featured status

### Items
- `GET /api/v1/items/` - List all items
- `GET /api/v1/items/{item_id}` - Get item by ID
- `POST /api/v1/items/` - Create new item
- `PUT /api/v1/items/{item_id}` - Update item
- `DELETE /api/v1/items/{item_id}` - Delete item

### Health
- `GET /health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed system health

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. 