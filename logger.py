# logger.py
import logging
import os
from logging.handlers import RotatingFileHandler
from config import config


class BotLogger:
    """Продвинутая система логирования для бота"""

    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        """Настройка системы логирования"""
        os.makedirs(os.path.dirname(config.logging.file), exist_ok=True)

        # Форматтер
        formatter = logging.Formatter(config.logging.format)

        # File handler с ротацией
        file_handler = RotatingFileHandler(
            config.logging.file,
            maxBytes=config.logging.max_size_mb * 1024 * 1024,
            backupCount=config.logging.backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Настройка root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, config.logging.level))

        # Удаляем существующие handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Добавляем новые handlers
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

        # Логируем запуск
        self.get_logger(__name__).info("🚀 Система логирования инициализирована")

    def get_logger(self, name: str) -> logging.Logger:
        """Получить логгер с указанным именем"""
        return logging.getLogger(name)


# Глобальный экземпляр логгера
bot_logger = BotLogger()