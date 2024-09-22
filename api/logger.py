import logging
# Make one log on every process with the configuration for debugging.
import colorlog


def get_logger_by_name(name: str):
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
    )
    # Create a custom logger
    logger = colorlog.getLogger(name)

    # Set level of logging
    logger.setLevel(logging.DEBUG)  # Set to lowest level needed

    # Create handlers
    c_handler = logging.StreamHandler()  # This outputs to sys.stdout
    # f_handler = logging.handlers.RotatingFileHandler(
    #     f"/tmp/{name}.log",
    #     maxBytes=1024 * 1024 * 1024,  # 1GB
    #     backupCount=1
    # )
    c_handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s:%(name)s:%(message)s'))
    # Create formatters and add it to handlers
    c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    # f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    c_handler.setFormatter(c_format)
    # f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    return logger
