# Rideasy - Ride-Sharing Application

A full-stack ride-sharing application with FastAPI backend and SwiftUI iOS app.

## Project Structure

```
N3Studio/
├── Rideasy/             # Main Rideasy project directory
│   ├── backend/         # FastAPI backend server
│   │   ├── app/        # Application code
│   │   ├── main.py     # FastAPI entry point
│   │   ├── requirements.txt # Python dependencies
│   │   └── docker-compose.yml # PostgreSQL setup
│   │
│   └── ios/            # iOS SwiftUI application
│       ├── Rideasy/     # Main app code
│       │   ├── Models/  # Data models
│       │   ├── Views/   # SwiftUI views
│       │   ├── Services/ # API services
│       │   └── ViewModels/ # View models
│       └── Rideasy.xcodeproj # Xcode project
│
├── LICENSE
├── README.md
└── .gitignore
```

## Features

- **Backend (FastAPI)**:
  - User authentication (JWT)
  - Ride request management
  - Real-time updates via WebSocket
  - Driver matching algorithm
  - PostgreSQL database

- **iOS App (SwiftUI)**:
  - User registration and login
  - Rider and Driver modes
  - Real-time ride tracking
  - Map integration
  - Ride request management

## Quick Start

### Backend Setup

1. Navigate to backend directory:
```bash
cd Rideasy/backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start PostgreSQL with Docker:
```bash
docker-compose up -d
```

4. Generate SECRET_KEY:
```bash
python generate_secret_key.py
```

5. Create `.env` file:
```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/rideasy
SECRET_KEY=your-generated-secret-key-here
```

6. Run the server:
```bash
python run.py
```

The API will be available at `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### iOS App Setup

1. Open `Rideasy/ios/Rideasy.xcodeproj` in Xcode
2. Update API base URL in `Rideasy/ios/Rideasy/Services/APIConfig.swift` if needed:
   - For Simulator: `http://localhost:8000/api`
   - For physical device: Use your computer's IP address
3. Build and run the app

## Development

### Backend API Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user
- `POST /api/rides` - Create ride request
- `GET /api/rides` - Get user's rides
- `GET /api/rides/available` - Get available rides (drivers)
- `POST /api/rides/{ride_id}/accept` - Accept ride (drivers)
- `WS /ws/ride-updates` - WebSocket for real-time updates

### Database

The application uses PostgreSQL. Tables are created automatically on first run.

To reset the database:
```bash
cd Rideasy/backend
docker-compose down -v
docker-compose up -d
```

## Technology Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, WebSocket
- **iOS**: SwiftUI, Combine, MapKit
- **Database**: PostgreSQL (Docker)

## License

See LICENSE file for details.
