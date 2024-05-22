# Ganjineh Task
===

## Description

This project is designed to determine the most profitable period for buying and selling a token based on its price over the past year. The primary functionality revolves around identifying the date range within which the highest profit can be achieved.

## User Types

The application supports three types of users:

1. **Regular User**:
   - Needs to register and log in.
   - Limited to 10 credits per day.
   - Can only use the API for BTC.

2. **Subscribed User**:
   - Two types of subscriptions, each with its limitations:
     - **First Subscription**:
       - Requests access to more tokens.
       - After admin approval, can access more tokens but the daily limit remains 10 credits.
     - **Second Subscription**:
       - Requests for daily credit increase.
       - After admin approval, daily credits are increased.
       - Alternatively, can request a monthly limit increase, which after admin approval, grants a higher daily limit for the specified period.

3. **Admin User**:
   - Can upload token data files.
   - Approves or rejects subscription requests.

## Features

- **Profit Calculation**:
  - Determines the range with the most profit within a given date range.
  - Regular users can query up to one month; subscribed users can query longer periods.
  
- **Credit Management**:
  - Credits are deducted based on the token:
    - BTC: 1 credit per request
    - ETH: 2 credits per request
    - TRX: 3 credits per request
  - Notifications are sent when credits run out or when a subscription is approved.

- **File Upload**:
  - Admins can upload token data files.
  - Data is processed asynchronously using Celery to prevent blocking operations.

- **Notifications**:
  - Real-time notifications using WebSockets and Django Channels.
  - Custom signals manage notification triggers for credit exhaustion and subscription approvals.

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Authentication**: JWT
- **Asynchronous Task Queue**: Celery with Redis as the broker
- **WebSocket**: Django Channels
- **Containerization**: Docker, Docker Compose
- **Database**: PostgreSQL
- **Caching**: Redis
- **API Documentation**: To be set up using Swagger

## How to Run

1. **Clone the repository**:
    ```bash
    git clone https://github.com/amirbapiri/ganjineh_task.git
    cd ganjineh_task
    ```

2. **Build and run the containers**:
    ```bash
    make build
    ```

3. **Create a superuser**:
    ```bash
    make superuser
    ```

## Makefile Commands

```makefile
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
