# LLM Consulting System

Микросервисная система для консультаций с использованием LLM через Telegram-бота.

## Описание

Проект реализует двухсервисную архитектуру:

- **Auth Service** — регистрация, логин и выдача JWT
- **Bot Service** — Telegram-бот с авторизацией пользователей

Бот:
- принимает JWT от пользователя
- отправляет запрос в очередь (Celery)
- получает ответ от LLM (OpenRouter)
- возвращает результат пользователю

---

## Архитектура


Telegram  
↓  
Bot Service (aiogram)  
↓  
Celery Worker → OpenRouter (LLM)  
↓  
Redis (result backend)  

Auth Service → JWT  
RabbitMQ → очередь задач


---

## Стек технологий

- FastAPI
- Aiogram
- Celery
- RabbitMQ
- Redis
- SQLAlchemy
- Pydantic
- JWT (python-jose)
- Docker / Docker Compose

---

## Запуск проекта

### 1. Клонирование

```bash
git clone https://github.com/Advident/llm_consulting_system_bondarenko_anton.git
cd llm_consulting_system
```

### 2. Настройка .env
bot_service/.env  

BOT_TOKEN=your_telegram_token  
OPENROUTER_API_KEY=your_openrouter_key  
OPENROUTER_MODEL=openai/gpt-4o-mini  

AUTH_SERVICE_URL=http://auth_service:8000  

CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//  
REDIS_URL=redis://redis:6379/0  

### 3. Запуск через Docker
docker compose up --build -d

### 4. Проверка
docker compose ps

Должны быть Up:

* auth_service
* bot_service
* celery_worker
* rabbitmq
* redis

## Доступ:  
* Auth API	http://localhost:8000/docs
* RabbitMQ UI	http://localhost:15672

RabbitMQ:

login: guest  
password: guest  

## Работа с Auth Service  

**Регистрация**
POST /auth/register  

{  
  "email": "test@email.com",  
  "password": "12345678"  
}  

**Логин**  
POST /auth/login  

Ответ:  
{  
  "access_token": "..."  
}  

**Получение пользователя**    
GET /auth/me  
Authorization: Bearer token

## Работа с ботом  
1. Передать токен  
/token JWT 
2. Отправить сообщение  

Бот:

* создаёт задачу Celery
* worker обращается к LLM
* результат возвращается пользователю

## Тесты
**Auth Service**  
* cd auth_service
* uv run pytest

**Bot Service**  
* cd bot_service
* uv run pytest

## Полезные команды
**Перезапуск:**  
docker compose restart

**Пересборка:**  
docker compose up --build -d

**Логи:**  
docker compose logs -f

Возможные проблемы  
**Бот не отвечает:**  
* проверь BOT_TOKEN
* проверь интернет внутри контейнера

**Celery не подключается:**  
* проверь RabbitMQ  
* проверь CELERY_BROKER_URL  

**Не меняется модель LLM**    
пересобери контейнеры:  
* docker compose down  
* docker compose up --build -d  
убедись, что переменная OPENROUTER_MODEL читается внутри контейнера



## Проверка кода
ruff check .

Результат:  

All checks passed!

## Реализовано:
* JWT-аутентификация
* Telegram-бот с авторизацией
* асинхронная обработка через Celery
* интеграция с LLM (OpenRouter)
* Docker-инфраструктура

## Скриншоты:
* Регистрация
![](./screenshots/a_register.png)

* Логин
![](./screenshots/a_login.png)

* /auth/me
![](./screenshots/a_me.png)

* Пример работы бота
![](./screenshots/b_tg.png)

* Работа RabbitMQ
![](./screenshots/b_rabbitmq.png)

* Тест auth_service
![](./screenshots/a_test.png)

* Тест bot_service
![](./screenshots/b_test.png)