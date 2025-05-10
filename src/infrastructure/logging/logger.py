import logging
from logging import StreamHandler, Formatter, FileHandler

def setup_logging(
    level: str = "INFO",
    log_to_file: bool = False,
    logfile: str = "app.log"
):
    fmt = "%(asctime)s %(levelname)-8s [%(name)s:%(lineno)d] %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    console = StreamHandler()
    console.setFormatter(Formatter(fmt, datefmt))
    root.addHandler(console)

    if log_to_file:
        fileh = FileHandler(logfile)
        fileh.setFormatter(Formatter(fmt, datefmt))
        root.addHandler(fileh)
