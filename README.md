🤖 Telegram Bot - Умный анализатор контента
Производственный Telegram бот для анализа текстов, изображений и документов с системой контроля доступа и продвинутым логированием.

https://img.shields.io/badge/Python-3.8+-blue.svg
https://img.shields.io/badge/Aiogram-3.x-green.svg
https://img.shields.io/badge/License-MIT-yellow.svg

✨ Возможности
🔤 Анализ текстовых сообщений - определение языка, подсчет символов, слов и строк

🖼️ Обработка изображений - информация о размере, разрешении и метаданных

📎 Работа с документами - анализ файлов различных форматов

🛡️ Система контроля доступа - разделение прав пользователей и администраторов

📊 Продвинутое логирование - ротация логов, разные уровни детализации

⚡ Production-ready - конфигурация через переменные окружения, graceful shutdown

🔒 Безопасность - проверка прав доступа, rate limiting

🚀 Быстрый старт
Предварительные требования
Python 3.8 или выше

Telegram Bot Token от @BotFather

Установка
Клонируйте репозиторий:

bash
git clone https://github.com/your-username/python_bot_05_11_25.git
cd python_bot_05_11_25
Создайте виртуальное окружение:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
Установите зависимости:

bash
pip install -r requirements.txt
Настройте конфигурацию:

bash
cp .env.example .env
# Отредактируйте .env файл, добавив ваш BOT_TOKEN
Настройка BotFather
Отправьте следующие команды @BotFather:

text
/setdescription
Умный бот для анализа контента и файлов с поддержкой текста, изображений и документов.

/setcommands
start - Запустить бота
help - Получить помощь
status - Статус системы
stats - Статистика (админы)
broadcast - Рассылка (админы)
analyze - Анализ текста
Запуск бота
bash
python main.py
⚙️ Конфигурация
Файл .env
env
# Обязательные настройки
BOT_TOKEN=your_telegram_bot_token_here

# Администраторы (через запятую)
ADMIN_IDS=123456789,987654321

# Разрешенные пользователи (оставьте пустым для публичного доступа)
ALLOWED_USER_IDS=111111111,222222222

# Дополнительные настройки
THROTTLE_RATE=0.5
DATABASE_URL=sqlite:///bot.db
LOG_LEVEL=INFO
Структура проекта
text
python_bot_05_11_25/
├── main.py              # Основной файл бота
├── config.py            # Конфигурация приложения
├── auth.py              # Система аутентификации
├── logger.py            # Продвинутое логирование
├── requirements.txt     # Зависимости проекта
├── .env                 # Переменные окружения (не в репозитории)
├── tests/               # Тесты
│   ├── test_bot.py
│   └── conftest.py
├── logs/                # Логи приложения
└── reports/             # Отчеты тестирования
🎯 Использование
Основные команды
/start - Запустить бота и получить приветствие

/help - Получить список всех команд

/status - Показать статус системы

/analyze [текст] - Проанализировать текст

Работа с контентом
Текстовые сообщения:

text
Пользователь: Привет! Это тестовое сообщение для анализа.

Бот:
📄 Анализ сообщения

👤 От: UserName
🔤 Длина: 45 символов
🌍 Язык: русский
📊 Слов: 6
📈 Строк: 1
Изображения:

text
🖼️ Информация о фото

📏 Размер: 245 KB
📐 Разрешение: 1200x800
🆔 File ID: AgACAx...
👤 От: UserName
📝 Подпись: Моя фотография
Документы:

text
📎 Информация о документе

📁 Имя файла: document.pdf
📏 Размер: 1024 KB
📄 MIME тип: application/pdf
🆔 File ID: BQACAx...
👤 От: UserName
👑 Административные функции
Команды для администраторов
/stats - Статистика использования бота

/broadcast [сообщение] - Рассылка сообщения пользователям

/users - Список активных пользователей

Настройка прав доступа
Добавьте ID администраторов в переменную ADMIN_IDS в .env файле:

env
ADMIN_IDS=123456789,987654321
🧪 Тестирование
Запуск тестов
bash
# Установите тестовые зависимости
pip install pytest pytest-html pytest-asyncio

# Запустите тесты с HTML отчетом
python run_tests.py

# Или напрямую через pytest
pytest tests/ --html=reports/report.html -v
Структура тестов
tests/test_bot.py - Unit-тесты основных функций

tests/test_auth.py - Тесты системы аутентификации

tests/test_handlers.py - Тесты обработчиков сообщений

📊 Логирование
Бот использует многоуровневое логирование с ротацией файлов:

Уровни: DEBUG, INFO, WARNING, ERROR, CRITICAL

Ротация: автоматическая при достижении 10MB

Хранение: до 5 архивных файлов

Пример настройки логирования в .env:

env
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
LOG_MAX_SIZE_MB=10
LOG_BACKUP_COUNT=5
🐛 Диагностика проблем
Частые проблемы
Бот не запускается:

Проверьте правильность BOT_TOKEN

Убедитесь, что все зависимости установлены

Проверьте права на запись в директорию logs/

Ошибки доступа:

Добавьте ваш ID в ADMIN_IDS или ALLOWED_USER_IDS

Проверьте настройки прав в .env файле

Проблемы с логированием:

Убедитесь, что директория logs/ существует

Проверьте права на запись

Логи
Логи сохраняются в logs/bot.log. Для отладки установите LOG_LEVEL=DEBUG в .env файле.

🔧 Разработка
Добавление новых команд
Добавьте обработчик в main.py:

python
@self.dp.message(Command("newcommand"))
@auth_manager.auth_required
async def new_command(message: Message):
    await message.answer("Новая команда!")
Обновите команды в BotFather

Добавление обработчиков контента
python
@self.dp.message(F.video)
@auth_manager.auth_required
async def handle_videos(message: Message):
    # Обработка видео
    pass
📈 Мониторинг
Статистика
Бот собирает базовую статистику:

Количество активных пользователей

Частота сообщений

Ошибки и исключения

Health checks
Используйте команду /status для проверки состояния системы.

🤝 Участие в разработке
Мы приветствуем вклад в развитие проекта!

Форкните репозиторий

Создайте ветку для функции (git checkout -b feature/amazing-feature)

Закоммитьте изменения (git commit -m 'Add amazing feature')

Запушьте в ветку (git push origin feature/amazing-feature)

Откройте Pull Request

Требования к коду
Соответствие PEP8

Наличие тестов для новой функциональности

Обновление документации

Проверка через pytest перед PR

📄 Лицензия
Этот проект распространяется под лицензией MIT. Подробнее см. в файле LICENSE.

🔗 Полезные ссылки
Aiogram документация

Telegram Bot API

Python Telegram Bot

👨‍💻 Авторы
Ваше Имя - GitHub
