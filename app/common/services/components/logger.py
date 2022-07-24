import logging
import logging.handlers


def get_logger(
        loglevel=logging.INFO,
        filename="logger.log",
        is_rotate=False,
        rotate_max_bytes=100000000,
        rotate_backup_count=10
):
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(process)d '
        '%(pathname)s:%(lineno)d:%(funcName)s %(message)s'
    )
    logger = logging.getLogger("__main__")
    logger.setLevel(loglevel)
    handler1 = logging.StreamHandler()
    handler1.setFormatter(formatter)
    if is_rotate:
        handler2 = logging.handlers.RotatingFileHandler(
            filename=filename,
            maxBytes=rotate_max_bytes,
            backupCount=rotate_backup_count,
            encoding="utf-8-sig"
        )
    else:
        handler2 = logging.FileHandler(
            filename=filename,
            encoding="utf-8-sig"
        )
    handler2.setFormatter(formatter)
    # 2つのhandlerを追加
    logger.addHandler(handler1)
    logger.addHandler(handler2)
    return logger
