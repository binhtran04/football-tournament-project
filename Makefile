.PHONY: help up down build logs clean test-backend test-frontend integration-test team-logs tournament-logs db-team db-tournament

# Default target
help:
	@echo "Football Tournament Manager - Development Commands"
	@echo ""
	@echo "🚀 Application:"
	@echo "  make up              - Start all services"
	@echo "  make down            - Stop all services"
	@echo "  make build           - Build all images"
	@echo "  make logs            - View all logs"
	@echo "  make clean           - Remove containers and volumes"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  make test-all           - Run all tests (backend unit + frontend + integration)"
	@echo "  make test-backend-unit  - Run backend unit tests (services must be DOWN)"
	@echo "  make test-frontend      - Run frontend tests (starts frontend if needed)"
	@echo "  make test-integration   - Run integration tests (services must be UP)"
	@echo ""
	@echo "🔍 Debugging:"
	@echo "  make team-logs       - View team service logs"
	@echo "  make tournament-logs - View tournament service logs"
	@echo "  make db-team         - Connect to team database"
	@echo "  make db-tournament   - Connect to tournament database"
	@echo ""
	@echo "🗄️ Database:"
	@echo "  make migrate-team    - Run team service migrations"
	@echo "  make migrate-tournament - Run tournament service migrations"

# Main application commands
up:
	@echo "🚀 Starting all services..."
	docker-compose up -d --build

down:
	@echo "🛑 Stopping all services..."
	docker-compose down

build:
	@echo "🔨 Building all images..."
	docker-compose build

logs:
	@echo "📋 Viewing all logs..."
	docker-compose logs -f

clean:
	@echo "🧹 Cleaning up containers and volumes..."
	docker-compose down -v
	docker system prune -f

# Test commands
test-all: test-backend-unit test-frontend test-integration

# Unit tests (run with services DOWN)
test-backend-unit: 
	@echo "🧪 Running backend unit tests (ensure services are stopped)..."
	@if [ "$$(docker-compose ps -q)" ]; then \
		echo "⚠️  Services are running. Stop them first with 'make down'"; \
		exit 1; \
	fi
	@make test-team-unit test-tournament-unit

test-team-unit:
	@echo "🧪 Running team service unit tests..."
	docker-compose run --rm --no-deps team-service sh -c "cd /app && PYTHONPATH=/app pytest -v"

test-tournament-unit:
	@echo "🧪 Running tournament service unit tests..."
	docker-compose run --rm --no-deps tournament-service sh -c "cd /app && PYTHONPATH=/app pytest -v"

# Frontend tests (run with services UP)
test-frontend:
	@echo "🧪 Running frontend tests..."
	@if [ ! "$$(docker-compose ps -q frontend)" ]; then \
		echo "🚀 Starting frontend service for testing..."; \
		docker-compose up -d frontend; \
		sleep 3; \
	fi
	docker-compose exec -T frontend npm test

integration-test-compose:
	@echo "🧪 Running integration tests with docker-compose..."
	docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

# Service-specific logs
team-logs:
	@echo "📋 Viewing team service logs..."
	docker-compose logs -f team-service

tournament-logs:
	@echo "📋 Viewing tournament service logs..."
	docker-compose logs -f tournament-service

frontend-logs:
	@echo "📋 Viewing frontend logs..."
	docker-compose logs -f frontend

db-logs:
	@echo "📋 Viewing database logs..."
	docker-compose logs -f team-db tournament-db

# Database connections
db-team:
	@echo "🗄️  Connecting to team database..."
	docker-compose exec team-db psql -U team_user -d team_db

db-tournament:
	@echo "🗄️  Connecting to tournament database..."
	docker-compose exec tournament-db psql -U tournament_user -d tournament_db

# Database migrations
migrate-team:
	@echo "🔄 Running team service migrations..."
	docker-compose exec team-service alembic upgrade head

migrate-tournament:
	@echo "🔄 Running tournament service migrations..."
	docker-compose exec tournament-service alembic upgrade head

# Development helpers
shell-team:
	@echo "🐚 Opening team service shell..."
	docker-compose exec team-service /bin/bash

shell-tournament:
	@echo "🐚 Opening tournament service shell..."
	docker-compose exec tournament-service /bin/bash

shell-frontend:
	@echo "🐚 Opening frontend shell..."
	docker-compose exec frontend /bin/bash

# Health checks
health:
	@echo "🏥 Checking service health..."
	@echo "Team Service:"
	@curl -s http://localhost:8001/health || echo "❌ Team service not responding"
	@echo ""
	@echo "Tournament Service:"
	@curl -s http://localhost:8002/health || echo "❌ Tournament service not responding"
	@echo ""
	@echo "Frontend:"
	@curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost:5173 || echo "❌ Frontend not responding"

# Reset everything
reset:
	@echo "🔄 Resetting everything..."
	docker-compose down -v
	docker system prune -f --volumes
	docker-compose up -d --build

# Show service status
status:
	@echo "📊 Service Status:"
	docker-compose ps