.PHONY: up down test migrate createsuperuser check clean

up:
	docker compose -f docker-compose-simple.yml up -d

down:
	docker compose -f docker-compose-simple.yml down

logs:
	docker compose -f docker-compose-simple.yml logs -f

status:
	docker compose -f docker-compose-simple.yml ps

test:
	docker compose -f docker-compose-simple.yml exec web python -m pytest tests/ -v

migrate:
	docker compose -f docker-compose-simple.yml exec web python manage.py migrate

createsuperuser:
	docker compose -f docker-compose-simple.yml exec web python manage.py createsuperuser

check:
	@echo "=== API Status ==="
	@curl -s http://localhost:8000/api/rooms/ | python -m json.tool || echo "API не отвечает"

db-shell:
	docker compose -f docker-compose-simple.yml exec db psql -U postgres -d hotel_db

shell:
	docker compose -f docker-compose-simple.yml exec web python manage.py shell

clean:
	docker compose -f docker-compose-simple.yml down -v
	docker system prune -f

full-test: up
	@sleep 5
	@docker compose -f docker-compose-simple.yml exec web python -m pytest tests/ -v
	@curl -s http://localhost:8000/api/rooms/ | python -m json.tool
