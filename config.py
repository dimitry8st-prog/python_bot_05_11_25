# config.py
import os
from dataclasses import dataclass, field
from typing import List
from dotenv import load_dotenv

load_dotenv()


@dataclass
class DatabaseConfig:
    """Конфигурация базы данных"""
    url: str = "sqlite:///bot.db"
    echo: bool = False


@dataclass
class LoggingConfig:
    """Конфигурация логирования"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: str = "logs/bot.log"
    max_size_mb: int = 10
    backup_count: int = 5


@dataclass
class BotConfig:
    """Конфигурация бота"""
    token: str
    admin_ids: List[int]
    allowed_user_ids: List[int] = None
    throttle_rate: float = 0.5

    def __post_init__(self):
        if self.allowed_user_ids is None:
            self.allowed_user_ids = []




@dataclass
class Config:
    bot: BotConfig = field(default_factory=BotConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)

    @classmethod
    def load(cls):
        """Загрузка конфигурации из переменных окружения"""
        admin_ids = [int(x.strip()) for x in os.getenv('ADMIN_IDS', '').split(',') if x.strip()]
        allowed_users = [int(x.strip()) for x in os.getenv('ALLOWED_USER_IDS', '').split(',') if x.strip()]

        return cls(
            bot=BotConfig(
                token=os.getenv('BOT_TOKEN'),
                admin_ids=admin_ids,
                allowed_user_ids=allowed_users,
                throttle_rate=float(os.getenv('THROTTLE_RATE', '0.5'))
            ),
            database=DatabaseConfig(
                url=os.getenv('DATABASE_URL', 'sqlite:///bot.db'),
                echo=os.getenv('DATABASE_ECHO', 'False').lower() == 'true'
            ),
            logging=LoggingConfig(
                level=os.getenv('LOG_LEVEL', 'INFO'),
                file=os.getenv('LOG_FILE', 'logs/bot.log'),
                max_size_mb=int(os.getenv('LOG_MAX_SIZE_MB', '10')),
                backup_count=int(os.getenv('LOG_BACKUP_COUNT', '5'))
            )
        )


# Глобальный экземпляр конфигурации
config = Config.load()