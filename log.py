import logging
from logging.handlers import RotatingFileHandler
import consts


def get_main_logger():
    logger = logging.getLogger()
    log_formatter = logging.Formatter("[%(levelname)s] %(asctime)s > %(message)s")
    logger.setLevel(logging.WARNING)

    main_log_file_handler = RotatingFileHandler(f"{consts.logs_dir}/main.log",
                                                maxBytes=consts.logs_rotating_size,
                                                backupCount=consts.logs_backup_count)
    main_log_file_handler.setFormatter(log_formatter)
    main_log_file_handler.setLevel(logging.WARNING)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.WARNING)

    logger.addHandler(main_log_file_handler)
    logger.addHandler(console_handler)

    return logger


def get_messages_logger():
    logger = logging.getLogger('bot_messages')
    log_formatter = logging.Formatter("[%(levelname)s] %(asctime)s > %(message)s")

    actions_log_file_handler = RotatingFileHandler(f"{consts.logs_dir}/messages.log",
                                                   maxBytes=consts.logs_rotating_size,
                                                   backupCount=consts.logs_backup_count)
    actions_log_file_handler.setFormatter(log_formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(actions_log_file_handler)
    return logger


def get_inline_mode_logger():
    logger = logging.getLogger('bot_inline_queries')
    log_formatter = logging.Formatter("[%(levelname)s] %(asctime)s > %(message)s")

    actions_log_file_handler = RotatingFileHandler(f"{consts.logs_dir}/inline_queries.log",
                                                   maxBytes=consts.logs_rotating_size,
                                                   backupCount=consts.logs_backup_count)
    actions_log_file_handler.setFormatter(log_formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(actions_log_file_handler)
    return logger


def setup_sqlalchemy_logger():
    log_formatter = logging.Formatter("[%(levelname)s] %(asctime)s > %(message)s")
    # DB
    logger_sqlalchemy = logging.getLogger('sqlalchemy.engine')
    logger_sqlalchemy.setLevel(logging.INFO)
    sqlalchemy_log_file_handler = RotatingFileHandler(f"{consts.logs_dir}/sqlalchemy.log",
                                                      maxBytes=consts.logs_rotating_size,
                                                      backupCount=consts.logs_backup_count)
    sqlalchemy_log_file_handler.setFormatter(log_formatter)
    logger_sqlalchemy.addHandler(sqlalchemy_log_file_handler)
    # logger_sqlalchemy.addHandler(console_handler)
    return True
