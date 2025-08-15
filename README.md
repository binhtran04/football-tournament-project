# Football Tournament Manager

A complete microservices-based football tournament management system with React frontend, FastAPI backend services, PostgreSQL databases, and ZeroMQ messaging.

## Architecture Overview

This project demonstrates a microservices architecture with the following components:

- **Frontend**: React + Vite + TypeScript + TailwindCSS
- **Team Service**: FastAPI backend managing teams with PostgreSQL database
- **Tournament Service**: FastAPI backend managing tournaments with PostgreSQL database
- **Messaging**: ZeroMQ pub/sub for inter-service communication
- **Databases**: Separate PostgreSQL instances for each service
- **Orchestration**: Docker Compose for development and testing

## Features

### Team Service

- Create and list teams via REST API
- Publishes `TeamRegistered` events when teams are created
- SQLAlchemy ORM with Alembic migrations
- PostgreSQL database storage

### Tournament Service

- Create and list tournaments via REST API
- Subscribes to `TeamRegistered` events from team-service
- Automatically creates tournament team entries when teams register
- SQLAlchemy ORM with Alembic migrations
- PostgreSQL database storage

### Frontend

- Modern React application with TypeScript
- Team management page (create/list teams)
- Tournament management page (create/list tournaments)
- Responsive design with TailwindCSS
- Form validation and error handling

### Messaging

- ZeroMQ publish-subscribe pattern
- JSON message format with event envelope
- Automatic event handling in background threads

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Running the Application

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd football-tournament-project
   ```

2. **Start all services:**

   ```bash
   docker-compose up --build
   ```

3. **Access the application:**

   - Frontend: http://localhost:5173
   - Team Service API: http://localhost:8001
   - Tournament Service API: http://localhost:8002

4. **Stop the application:**
   ```bash
   docker-compose down
   ```

## Development

### Project Structure

```
project-root/
├── backend/
│   ├── team-service/
│   │   ├── app/
│   │   │   ├── main.py          # FastAPI application
│   │   │   ├── api.py           # REST endpoints
│   │   │   ├── models.py        # SQLAlchemy models
│   │   │   ├── schemas.py       # Pydantic schemas
│   │   │   ├── database.py      # Database configuration
│   │   │   └── events.py        # ZeroMQ publisher
│   │   ├── alembic/             # Database migrations
│   │   ├── tests/               # Unit tests
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── tournament-service/      # Similar structure to team-service
│       ├── app/
│       │   └── events.py        # ZeroMQ subscriber
│       ├── alembic/
│       ├── tests/
│       ├── Dockerfile
│       └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/              # Page components
│   │   ├── tests/              # Frontend tests
│   │   ├── api.ts              # API client
│   │   └── types.ts            # TypeScript types
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── tests/
│   ├── integration_test.sh     # Integration test script
│   └── Dockerfile              # Test runner container
│
├── docker-compose.yml          # Main orchestration
├── docker-compose.test.yml     # Test orchestration
├── Makefile                    # Development commands
├── .env.example               # Environment variables template
└── README.md
```

### Running Tests

#### Backend Unit Tests

**Team Service:**

```bash
# Run in container
docker-compose exec team-service pytest

# Run locally (requires Python 3.11+ and dependencies)
cd backend/team-service
pip install -r requirements.txt
pytest
```

**Tournament Service:**

```bash
# Run in container
docker-compose exec tournament-service pytest

# Run locally
cd backend/tournament-service
pip install -r requirements.txt
pytest
```

#### Frontend Tests

```bash
# Run in container
docker-compose exec frontend npm test

# Run locally (requires Node.js 18+)
cd frontend
npm install
npm test
```

#### Integration Tests

```bash
# Using test compose file
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

# Using Makefile
make integration-test

# Manual execution
./tests/integration_test.sh
```

### Database Migrations

**Team Service:**

```bash
# Create new migration
docker-compose exec team-service alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec team-service alembic upgrade head

# Check migration status
docker-compose exec team-service alembic current
```

**Tournament Service:**

```bash
# Create new migration
docker-compose exec tournament-service alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec tournament-service alembic upgrade head
```

### Development Commands (Makefile)

```bash
make up              # Start all services
make down            # Stop all services
make build           # Build all images
make logs            # View all logs
make clean           # Remove containers and volumes

make test-backend    # Run backend tests
make test-frontend   # Run frontend tests
make integration-test # Run integration tests

make team-logs       # View team service logs
make tournament-logs # View tournament service logs
make db-team         # Connect to team database
make db-tournament   # Connect to tournament database
```

## API Documentation

### Team Service API

**Base URL:** `http://localhost:8001`

- `POST /teams` - Create a team

  ```json
  {
    "name": "Helsinki FC"
  }
  ```

- `GET /teams` - List all teams
- `GET /health` - Health check

### Tournament Service API

**Base URL:** `http://localhost:8002`

- `POST /tournaments` - Create a tournament

  ```json
  {
    "name": "Spring Cup"
  }
  ```

- `GET /tournaments` - List all tournaments
- `GET /tournament-teams` - List tournament team registrations (debug endpoint)
- `GET /health` - Health check

## Event System

### Message Format

All events follow this JSON envelope structure:

```json
{
  "event": "TeamRegistered",
  "payload": {
    "teamId": "uuid-string",
    "name": "Team Name"
  },
  "timestamp": "2024-01-01T10:00:00Z"
}
```

### Event Flow

1. User creates a team via frontend → Team Service API
2. Team Service stores team in database
3. Team Service publishes `TeamRegistered` event via ZeroMQ
4. Tournament Service receives event and creates tournament team entry

## Configuration

### Environment Variables

**Team Service:**

- `DB_USER` - Database username (default: team_user)
- `DB_PASSWORD` - Database password (default: team_password)
- `DB_NAME` - Database name (default: team_db)
- `TEAM_DB_HOST` - Database host (default: team-db)
- `DB_PORT` - Database port (default: 5432)

**Tournament Service:**

- `DB_USER` - Database username (default: tournament_user)
- `DB_PASSWORD` - Database password (default: tournament_password)
- `DB_NAME` - Database name (default: tournament_db)
- `TOURNAMENT_DB_HOST` - Database host (default: tournament-db)
- `DB_PORT` - Database port (default: 5432)

**Frontend:**

- `VITE_TEAM_SERVICE_URL` - Team service URL (default: http://localhost:8001)
- `VITE_TOURNAMENT_SERVICE_URL` - Tournament service URL (default: http://localhost:8002)

## Troubleshooting

### Common Issues

1. **Services not starting:**

   - Check if ports 5173, 8001, 8002 are available
   - Verify Docker daemon is running
   - Check logs: `docker-compose logs [service-name]`

2. **Database connection errors:**

   - Wait for database health checks to pass
   - Check database logs: `docker-compose logs team-db tournament-db`
   - Verify migrations ran: `docker-compose exec team-service alembic current`

3. **ZeroMQ connection issues:**

   - Ensure team-service starts before tournament-service
   - Check service logs for connection errors
   - Verify network connectivity between containers

4. **Frontend API errors:**
   - Check backend service URLs in environment variables
   - Verify CORS configuration in backend services
   - Check browser developer console for network errors

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f team-service
docker-compose logs -f tournament-service
docker-compose logs -f frontend

# Database logs
docker-compose logs -f team-db tournament-db
```

### Debugging

```bash
# Access service shell
docker-compose exec team-service /bin/bash
docker-compose exec tournament-service /bin/bash

# Connect to database
docker-compose exec team-db psql -U team_user -d team_db
docker-compose exec tournament-db psql -U tournament_user -d tournament_db

# Check service health
curl http://localhost:8001/health
curl http://localhost:8002/health
```

## Production Considerations

This is a development/prototype setup. For production deployment, consider:

1. **Security:**

   - Use secrets management for database passwords
   - Configure proper CORS origins
   - Add authentication/authorization
   - Use HTTPS with SSL certificates

2. **Scalability:**

   - Load balancing for services
   - Database connection pooling
   - Message queue persistence
   - Container orchestration (Kubernetes)

3. **Monitoring:**

   - Health check endpoints
   - Metrics collection (Prometheus)
   - Centralized logging (ELK stack)
   - Distributed tracing

4. **Data:**
   - Database backups
   - Data migration strategies
   - Read replicas for scaling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run test suite
5. Submit pull request

## License

This project is for educational purposes.
