# Сервис: Bot Gateway

Этот сервис представляет собой шлюз для Telegram-бота, построенный на FastAPI. Он принимает вебхуки от Telegram, обрабатывает их с помощью aiogram и взаимодействует с другими микросервисами через gRPC для получения необходимой информации. Обнаружение сервисов реализовано с помощью Consul. В качестве веб-сервера используется Nginx для терминирования SSL и проксирования запросов к приложению.

## Структура проекта

-   `.`
    -   `docker-compose.yml`: Файл для оркестрации сервисов с помощью Docker Compose.
    -   `nginx/`: Конфигурация для веб-сервера Nginx.
    -   `bot_gateway/`: Исходный код сервиса `bot_gateway`.
        -   `Dockerfile`: Инструкции для сборки Docker-образа сервиса.
        -   `pyproject.toml`: Определение зависимостей проекта для Poetry.
        -   `src/bot_gateway/`: Основная кодовая база.
            -   `api/`: Модули, связанные с FastAPI и обработкой HTTP-запросов.
            -   `bot/`: Логика самого Telegram-бота (хендлеры и т.д.).
            -   `core/`: Основные настройки и конфигурация.
            -   `grpc_clients/`: Клиенты для взаимодействия с другими сервисами по gRPC.
            -   `main.py`: Точка входа в приложение FastAPI.
        -   `tests/`: Тесты для приложения.

## Технологии

-   **Python 3.10**
-   **FastAPI**: Веб-фреймворк для создания API.
-   **Aiogram 3**: Асинхронный фреймворк для создания Telegram-ботов.
-   **gRPC**: Фреймворк для удаленного вызова процедур.
-   **Consul**: Инструмент для обнаружения сервисов (service discovery).
-   **Docker & Docker Compose**: Контейнеризация и оркестрация.
-   **Nginx**: Веб-сервер и обратный прокси.
-   **Poetry**: Управление зависимостями.

## Настройка и запуск

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/VOVSn/bot_backend_aiogram
    cd bot_backend_aiogram
    ```

2.  **Создайте файл окружения:**
    Создайте файл `.env` в корневой директории проекта и добавьте в него следующие переменные:
    ```env
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
    WEBHOOK_HOST=https://your_domain.com
    ```
    -   `TELEGRAM_BOT_TOKEN`: Токен вашего Telegram-бота.
    -   `WEBHOOK_HOST`: Ваш домен, на который Telegram будет отправлять обновления.

3.  **Настройте Nginx и SSL:**
    -   В файле `nginx/nginx.conf` замените `your_domain.com` на ваш реальный домен.
    -   Для работы HTTPS вам необходимы SSL-сертификаты. `docker-compose.yml` ожидает, что они будут находиться в `/etc/letsencrypt`. Вы можете получить их с помощью Certbot.
    -   При первом запуске для получения сертификатов может потребоваться закомментировать `server` блок для 443 порта в `nginx.conf`, запустить Nginx, получить сертификаты с помощью Certbot, а затем раскомментировать блок и перезапустить Nginx.

4.  **Скомпилируйте Protobuf-файлы (если требуется):**
    Если вы вносите изменения в `.proto` файлы, вам нужно будет пересоздать gRPC-код.
    ```bash
    python -m grpc_tools.protoc -I./bot_gateway/src/bot_gateway/grpc_clients/protos --python_out=./bot_gateway/src/bot_gateway/grpc_clients/protos --pyi_out=./bot_gateway/src/bot_gateway/grpc_clients/protos --grpc_python_out=./bot_gateway/src/bot_gateway/grpc_clients/protos ./bot_gateway/src/bot_gateway/grpc_clients/protos/auth.proto
    ```

5.  **Запустите сервисы:**
    Используйте Docker Compose для сборки и запуска всех контейнеров.
    ```bash
    docker-compose up --build -d
    ```
    Приложение `bot_gateway` автоматически установит вебхук для Telegram при старте.

## API

### Webhook

-   **URL**: `/api/v1/{TELEGRAM_BOT_TOKEN}`
-   **Method**: `POST`
-   **Описание**: Эндпоинт для приема обновлений от Telegram. URL защищен секретным токеном, который передается в заголовке `X-Telegram-Bot-Api-Secret-Token`.

## Взаимодействие с другими сервисами

### Auth Service (gRPC)

Сервис `bot_gateway` использует gRPC для связи с сервисом аутентификации (`auth_service`).

-   **Обнаружение**: Адрес `auth_service` получается динамически из Consul.
-   **Методы**:
    -   `GetUser(user_id)`: Получает информацию о пользователе по его Telegram ID.

