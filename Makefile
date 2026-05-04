.PHONY: run dev build up down

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8080

dev:
	uvicorn app.main:app --reload --port 8080

build:
	docker build -t zambom-gateway .

up:
	docker-compose up -d

down:
	docker-compose down
