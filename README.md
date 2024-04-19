# Trusted Secrets API

## Описание проекта

Trusted Secrets API - это HTTP сервис для создания и управления одноразовыми секретами, который позволяет пользователям безопасно делиться конфиденциальной информацией через одноразовые ссылки. Сервис разработан для обеспечения высокой степени безопасности и простоты использования через JSON API, без необходимости пользовательского интерфейса.

## Основные функции

- **Генерация секрета**: Пользователи могут отправить секретную информацию и кодовую фразу (пароль) на сервер, который в ответ предоставляет уникальный ключ для доступа к секрету. Если ключ доступа или пароль будут потеряны то восстановить доступ никак невозможно.
- **Время жизни секрета**: По умолчанию время жизни секрета 7 суток. Можно указать необходимое время жизни в секундах при добавлении секрета.
- **Все секреты зашифрованы**: Никто не сможет узнать секрет если был использован пароль при его создании. Пароль нигде не хранится.
- **Получение секрета**: Секрет может быть получен по уникальному ключу, предоставленному при его создании, при условии, что предоставлена правильная кодовая фраза (если она была установлена).

## Технологический стек

- **Язык**: Python
- **Веб-фреймворк**: FastAPI
- **База данных**: MongoDB + Motor
- **Шифрование**: Cryptography Fernet
- **Тестирование**: Pytest
- **Контейнеризация**: Docker и Docker Compose

## Как запустить проект

### Зависимости

```bash
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Конфигурация

В `.env` файле создать переменные среды:
```bash
KEY=cVlnT...
SALT=RTW...
```
Настройки для доступа к базе данных используются "по умолчанию" если не указано иное в переменных `MO_HOST`, `MO_USER`, `MO_PASS` и `MO_PORT` соответственно.
Для случайного формирования ключа и соли можно (и нужно) воспользоваться скриптом `generate_salt_and_key.py`

### Запуск в контейнере

Приложение может запускаться как в контейнере докера, так и в локальном виртуальном окружении. Для запуска в контейнере:

```bash
docker-compose up
```

### Локальный запуск 

Для локального запуска приложения нужно убедиться в том, что запущена база данных. Например, предварительно запустить только контейнер с базой. 

```bash
docker-compose up -d mongo
uvicorn src.main:app --reload
```

## API Endpoinds

### /generate

Сохраняет секрет в базе данных приложения. Пароль, переданный при создании секрета, используется один раз только для шифрования и потом не сохраняется.

### /secrets/{secret_key}

По одноразовой ссылке позволяет один раз получить доступ к секрету. После получения секрет сразу и насовсем удаляется из базы дынных.

## Тестирование

Для запуска тестов из корня приложения выполнить `pytest`. База данных при этом должна быть запущена.
Тестирование не затрагивает уже находящихся в базе данных документов.
```bash
docker-compose up -d mongo
pytest
```