import logging
from app.shell.runner import run
from app.consts import shellhn_consts


def main():
    logging.basicConfig(filename=shellhn_consts.LOG_FILE_PATH, level=logging.INFO, format=shellhn_consts.FORMAT, datefmt=shellhn_consts.DATE_FMT)
    logging.info(shellhn_consts.STARTED)
    run()
    logging.info(shellhn_consts.FINISHED)


if __name__ == "__main__":
    main()
