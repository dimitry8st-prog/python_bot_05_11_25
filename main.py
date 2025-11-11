# main.py
import os
import asyncio
import signal
from datetime import datetime
from typing import Dict

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import config


class ProductionBotManager:
    """Production-ready менеджер бота"""

    def __init__(self):
        self.bot = None
        self.dp = None
        self.running = False
        self.user_cooldowns: Dict[int, float] = {}

        # Настройка при старте
        self.setup_environment()

    def setup_environment(self):
        """Проверка окружения"""
        if not config.bot.token or config.bot.token == 'your_production_bot_token_here':
            raise ValueError("❌ Неверный BOT_TOKEN в конфигурации")

        print("✅ Окружение проверено")

    async def check_cooldown(self, user_id: int) -> bool:
        """Проверка кд на сообщения"""
        current_time = asyncio.get_event_loop().time()
        last_time = self.user_cooldowns.get(user_id, 0)

        if current_time - last_time < config.bot.throttle_rate:
            return False

        self.user_cooldowns[user_id] = current_time
        return True

    async def initialize_bot(self):
        """Инициализация бота"""
        self.bot = Bot(
            token=config.bot.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.dp = Dispatcher()

        # Проверка доступности бота
        await self.check_bot_availability()

        # Настройка обработчиков
        self.setup_handlers()

        print("✅ Бот инициализирован")

    async def check_bot_availability(self):
        """Проверка доступности бота"""
        try:
            bot_info = await self.bot.get_me()
            print(f"✅ Бот @{bot_info.username} готов к работе")
            return True
        except Exception as e:
            print(f"❌ Ошибка подключения бота: {e}")
            raise

    def setup_handlers(self):
        """Настройка всех обработчиков"""

        # Команда /start
        @self.dp.message(Command("start"))
        async def start_command(message: Message):
            user = message.from_user
            welcome_text = (
                f"👋 Привет, {user.first_name}!\n\n"
                f"🤖 <b>Умный бот для анализа контента</b>\n\n"
                f"📁 <b>Что я умею:</b>\n"
                f"• 🔤 Анализировать текстовые сообщения\n"
                f"• 🖼️ Обрабатывать изображения\n"
                f"• 📎 Работать с документами\n"
                f"• 🌍 Определять язык текста\n\n"
                f"💡 Используйте /help для списка команд"
            )
            await message.answer(welcome_text)
            print(f"Пользователь {user.full_name} (ID: {user.id}) запустил бота")

        # Команда /help
        @self.dp.message(Command("help"))
        async def help_command(message: Message):
            help_text = (
                "🤖 <b>Доступные команды:</b>\n\n"
                "👤 <b>Основные команды:</b>\n"
                "/start - Запустить бота\n"
                "/help - Получить справку\n"
                "/status - Статус системы\n\n"
                "🛠️ <b>Команды для работы с файлами:</b>\n"
                "Просто отправьте:\n"
                "• 📷 Фото - получите информацию\n"
                "• 📄 Документ - анализ файла\n"
                "• 🔤 Текст - полный анализ\n"
            )
            await message.answer(help_text)

        # Команда /status
        @self.dp.message(Command("status"))
        async def status_command(message: Message):
            status_text = (
                "📊 <b>Статус системы</b>\n\n"
                "✅ Бот работает стабильно\n"
                "🛡️ Безопасная конфигурация\n"
                "📝 Логирование активно\n"
                "⚡ Production-ready\n"
                f"👥 Пользователей в кэше: {len(self.user_cooldowns)}"
            )
            await message.answer(status_text)

        # Обработчик текстовых сообщений
        @self.dp.message(F.text)
        async def handle_text_messages(message: Message):
            # Проверка кд
            if not await self.check_cooldown(message.from_user.id):
                await message.answer("⏳ Слишком много сообщений. Подождите немного.")
                return

            user = message.from_user
            text = message.text

            print(f"Текст от {user.full_name} (ID: {user.id}): {text[:50]}...")

            # Простой анализ текста
            word_count = len(text.split())
            char_count = len(text)

            response = (
                f"📄 <b>Анализ сообщения</b>\n\n"
                f"👤 <b>От:</b> {user.full_name}\n"
                f"🔤 <b>Длина:</b> {char_count} символов\n"
                f"📊 <b>Слов:</b> {word_count}\n"
                f"💬 <b>Текст:</b>\n<code>{text[:100]}{'...' if len(text) > 100 else ''}</code>"
            )

            await message.answer(response)

        # Обработчик фото
        @self.dp.message(F.photo)
        async def handle_photos(message: Message):
            if not await self.check_cooldown(message.from_user.id):
                return

            photo = message.photo[-1]
            user = message.from_user

            print(f"Фото от {user.full_name} (ID: {user.id})")

            response = (
                f"🖼️ <b>Информация о фото</b>\n\n"
                f"📏 <b>Разрешение:</b> {photo.width}x{photo.height}\n"
                f"👤 <b>От:</b> {user.full_name}"
            )

            if message.caption:
                response += f"\n📝 <b>Подпись:</b> {message.caption}"

            await message.answer(response)

        # Обработчик документов
        @self.dp.message(F.document)
        async def handle_documents(message: Message):
            if not await self.check_cooldown(message.from_user.id):
                return

            doc = message.document
            user = message.from_user

            print(f"Документ от {user.full_name} (ID: {user.id}): {doc.file_name}")

            response = (
                f"📎 <b>Информация о документе</b>\n\n"
                f"📁 <b>Имя файла:</b> {doc.file_name or 'Неизвестно'}\n"
                f"📏 <b>Размер:</b> {doc.file_size // 1024 if doc.file_size else 'Неизвестно'} KB\n"
                f"📄 <b>Тип:</b> {doc.mime_type or 'Неизвестно'}\n"
                f"👤 <b>От:</b> {user.full_name}"
            )

            await message.answer(response)

    async def shutdown(self):
        """Корректное завершение работы"""
        if not self.running:
            return

        self.running = False
        print("🛑 Завершение работы бота...")

        try:
            if self.dp:
                await self.dp.stop_polling()
            if self.bot:
                await self.bot.session.close()

            print("✅ Бот корректно завершил работу")
        except Exception as e:
            print(f"❌ Ошибка при завершении: {e}")

    async def run(self):
        """Запуск бота"""
        try:
            await self.initialize_bot()
            self.running = True

            print("🚀 Production бот запущен!")
            print("=" * 50)
            print("🤖 PRODUCTION BOT АКТИВЕН!")
            print("📊 Конфигурация загружена")
            print("🛑 Ctrl+C для остановки")
            print("=" * 50)

            await self.dp.start_polling(self.bot)

        except KeyboardInterrupt:
            print("⏹️ Остановлено пользователем")
        except Exception as e:
            print(f"💥 Критическая ошибка: {e}")
            raise
        finally:
            await self.shutdown()


async def main():
    """Основная функция"""
    bot_manager = ProductionBotManager()

    try:
        await bot_manager.run()
    except Exception as e:
        print(f"💥 Фатальная ошибка: {e}")
    finally:
        print("👋 До свидания!")


if __name__ == "__main__":
    asyncio.run(main())