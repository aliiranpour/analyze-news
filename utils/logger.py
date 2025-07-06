import logging

def get_logger(name: str = __name__) -> logging.Logger:
    """
    ایجاد و بازگرداندن logger با فرمت استاندارد برای پروژه
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
