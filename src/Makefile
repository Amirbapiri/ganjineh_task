build:
	docker compose -f docker-compose.dev.yml build -d --remove-orphans

vbuild:
	docker compose -f docker-compose.dev.yml up --build --remove-orphans

up:
	docker compose -f docker-compose.dev.yml up -d

vup:
	docker compose -f docker-compose.dev.yml up

down:
	docker compose -f docker-compose.dev.yml down

down-v:
	docker compose -f docker-compose.dev.yml down -v

makemigrations:
	docker compose -f docker-compose.dev.yml run --rm django python manage.py makemigrations

migrate:
	docker compose -f docker-compose.dev.yml run --rm django python manage.py migrate

superuser:
	docker compose -f docker-compose.dev.yml run --rm django python manage.py createsuperuser

collectstatic:
	docker compose -f docker-compose.dev.yml run --rm django python manage.py collectstatic --no-input --clear

