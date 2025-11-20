# Rideasy Backend API

FastAPI backend server for handling ride requests, user management, and real-time updates.

## Features

- **User Management**: Registration, authentication, and profile management
- **Ride Management**: Create, update, cancel, and track rides
- **Real-time Updates**: WebSocket support for live ride status updates
- **Driver Matching**: Automatic driver matching for ride requests
- **JWT Authentication**: Secure token-based authentication

## Setup

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (for PostgreSQL)
- PostgreSQL 12+ (optional, if not using Docker)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL database using Docker Compose (Recommended):

```bash
# Start PostgreSQL container
cd backend
docker-compose up -d

# Verify it's running
docker-compose ps

# The database 'rideasy' will be created automatically
```

**Important:** If you have a local PostgreSQL installation (e.g., Homebrew), stop it first to avoid port conflicts:
```bash
# Stop local PostgreSQL (macOS Homebrew)
brew services stop postgresql@14

# Or for other versions
brew services stop postgresql
```

**Alternative: Local PostgreSQL (macOS Homebrew):**
```bash
# Create database (uses your system username)
createdb rideasy
```

**Alternative: Local PostgreSQL (Linux):**
```bash
# Create database
createdb rideasy

# Or using psql
psql -U postgres
CREATE DATABASE rideasy;
```

3. Create a `.env` file:
```bash
cp .env.example .env
```

4. Update `.env` with your configuration:
   - **Set a strong `SECRET_KEY`** for JWT token signing (see below for generation methods)
   - Configure `DATABASE_URL` (optional - defaults to Docker Compose config):
     
     **Docker Compose (default - no need to set if using docker-compose):**
     ```
     DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/rideasy
     ```
     
     **macOS (Homebrew) - usually no password needed:**
     ```
     DATABASE_URL=postgresql+asyncpg://your_username@localhost:5432/rideasy
     ```
     
     **Note:** If using Docker Compose, you don't need to set `DATABASE_URL` - it's already configured as the default.

### Generating SECRET_KEY

The `SECRET_KEY` is used to sign and verify JWT tokens. **Never commit this to version control** and use a strong, random value.

**Option 1: Using Python (Recommended)**
```bash
python generate_secret_key.py
```

**Option 2: Using OpenSSL**
```bash
openssl rand -hex 32
```

**Option 3: Using Python directly**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Option 4: Using Python interactive shell**
```python
import secrets
secrets.token_hex(32)
```

Copy the generated key and add it to your `.env` file:
```
SECRET_KEY=your-generated-secret-key-here
```

**Important Security Notes:**
- Use a different `SECRET_KEY` for production vs development
- Never share or commit your `SECRET_KEY` to version control
- If your `SECRET_KEY` is compromised, regenerate it immediately (users will need to re-login)

5. Run the server:
```bash
python run.py
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

**Note**: The database tables will be created automatically on first run.

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Authentication (`/api/auth`)
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get access token
- `GET /api/auth/me` - Get current user info

### Users (`/api/users`)
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update current user profile
- `PUT /api/users/driver/availability` - Update driver availability status
- `GET /api/users/{user_id}` - Get user by ID

### Rides (`/api/rides`)
- `POST /api/rides` - Create a new ride request
- `GET /api/rides` - Get user's rides (filtered by status)
- `GET /api/rides/available` - Get available rides (drivers only)
- `GET /api/rides/{ride_id}` - Get ride details
- `PUT /api/rides/{ride_id}` - Update ride status
- `POST /api/rides/{ride_id}/accept` - Accept a ride (drivers only)
- `POST /api/rides/{ride_id}/cancel` - Cancel a ride

### WebSocket (`/ws`)
- `WS /ws/ride-updates?token={jwt_token}` - Connect for real-time ride updates

## WebSocket Usage

Connect to the WebSocket endpoint with your JWT token:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/ride-updates?token=YOUR_JWT_TOKEN');

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (message.type === 'ride_update') {
    // Handle ride update
    console.log('Ride updated:', message.data);
  }
};
```

## Database

The application uses PostgreSQL (configured via `DATABASE_URL` in `.env`). The database tables will be created automatically on first run.

### Database Connection String Format

```
postgresql+asyncpg://username:password@host:port/database_name
```

Example:
```
postgresql+asyncpg://postgres:postgres@localhost:5432/rideasy
```

### Models
- **User**: User accounts with rider/driver modes
- **Location**: Pickup and destination locations
- **Ride**: Ride requests and their status

### Docker Compose Commands

**Start PostgreSQL:**
```bash
cd backend
docker-compose up -d
```

**Stop PostgreSQL:**
```bash
docker-compose down
```

**Stop and remove data (fresh start):**
```bash
docker-compose down -v
```

**View logs:**
```bash
docker-compose logs -f postgres
```

**Check status:**
```bash
docker-compose ps
```

**Connect to PostgreSQL directly:**
```bash
docker-compose exec postgres psql -U postgres -d rideasy
```

### Troubleshooting

**Port Conflict Error:**
If you get connection errors, you might have a local PostgreSQL instance running that conflicts with Docker:
```bash
# Check what's using port 5432
lsof -i :5432

# Stop local PostgreSQL (macOS Homebrew)
brew services stop postgresql@14

# Or check and stop any PostgreSQL service
brew services list | grep postgresql
```

**Role "postgres" does not exist:**
This usually means you're connecting to a local PostgreSQL instance instead of Docker. Stop the local service and ensure Docker Compose is running.

## Authentication

All endpoints except `/api/auth/register` and `/api/auth/login` require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer YOUR_JWT_TOKEN
```

## Ride Status Flow

1. **SEARCHING**: Ride created, looking for driver
2. **MATCHED**: Driver assigned, on the way
3. **DRIVER_ARRIVING**: Driver near pickup location
4. **IN_PROGRESS**: Ride in progress
5. **COMPLETED**: Ride completed
6. **CANCELLED**: Ride cancelled
