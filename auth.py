from functools import wraps
from aiogram import types
from aiogram.exceptions import TelegramForbiddenError
from config import config
from logger import bot_logger

logger = bot_logger.get_logger(__name__)


class AuthManager:
    """Менеджер аутентификации и авторизации"""

    def __init__(self):
        self.admin_ids = set(config.bot.admin_ids)
        self.allowed_user_ids = set(config.bot.allowed_user_ids)
        self.is_public = len(self.allowed_user_ids) == 0

    def is_admin(self, user_id: int) -> bool:
        """Проверяет, является ли пользователь администратором"""
        return user_id in self.admin_ids

    def is_user_allowed(self, user_id: int) -> bool:
        """Проверяет, разрешен ли доступ пользователю"""
        if self.is_public:
            return True
        return user_id in self.allowed_user_ids or user_id in self.admin_ids

    def admin_required(self, func):
        """Декоратор для проверки прав администратора"""

        @wraps(func)
        async def wrapper(message: types.Message, *args, **kwargs):
            user_id = message.from_user.id

            if not self.is_admin(user_id):
                logger.warning(f"Попытка доступа к админ-команде от пользователя {user_id}")
                await message.answer("❌ У вас нет прав для выполнения этой команды.")
                return

            return await func(message, *args, **kwargs)

        return wrapper

    def auth_required(self, func):
        """Декоратор для проверки авторизации пользователя"""

        @wraps(func)
        async def wrapper(message: types.Message, *args, **kwargs):
            user_id = message.from_user.id

            if not self.is_user_allowed(user_id):
                logger.warning(f"Попытка доступа от неавторизованного пользователя {user_id}")
                await message.answer("❌ Доступ запрещен. Обратитесь к администратору.")
                return

            return await func(message, *args, **kwargs)

        return wrapper


# Глобальный экземпляр менеджера аутентификации
auth_manager = AuthManager()