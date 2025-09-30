.PHONY: help build run test clean deploy

help:
	@echo "Available commands:"
	@echo "  build     - Build Docker images"
	@echo "  run       - Run development environment"
	@echo "  test      - Run tests"
	@echo "  clean     - Clean Docker resources"
	@echo "  deploy    - Deploy to Kubernetes"

build:
	docker-compose -f docker-compose.dev.yml build

run:
	docker-compose -f docker-compose.dev.yml up -d

test:
	cd backend && pytest
	cd frontend && npm test -- --watchAll=false

clean:
	docker-compose -f docker-compose.dev.yml down -v
	docker system prune -f

deploy:
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/
