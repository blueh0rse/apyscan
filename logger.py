import logging


def create_logger():
    """Create logger with file and console handlers, each with a custom format"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # File handler with standard level names
    file_handler = logging.FileHandler("logs/app.log", mode="a", encoding="utf-8")
    file_formatter = logging.Formatter(
        "{asctime} - {levelname} - {message}", style="{", datefmt="%d-%m-%Y %H:%M"
    )
    file_handler.setFormatter(file_formatter)

    # Console handler with custom symbols for levels
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = CustomConsoleFormatter("{levelname} {message}", style="{")
    console_handler.setFormatter(console_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


class CustomConsoleFormatter(logging.Formatter):
    """Custom formatter to replace level names with specific symbols for console output"""

    LEVEL_TO_SYMBOL = {
        "INFO": "[+]",
        "WARNING": "[-]",
        "ERROR": "[!]",
        "DEBUG": "[*]",
        "CRITICAL": "[#]",
    }

    def format(self, record):
        # replace level name with custom symbol for console output
        record.levelname = self.LEVEL_TO_SYMBOL.get(record.levelname, record.levelname)
        return super().format(record)
