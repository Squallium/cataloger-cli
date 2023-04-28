import logging

import fire

from cataloger_cli.managers.photo_manager import PhotoManager
from rich.logging import RichHandler

class CatalogerCli:

    def __init__(self) -> None:
        super().__init__()

        self.photo_manager = PhotoManager()


class MainDefaultTest:

    @staticmethod
    def test():
        print('Hi, test')


FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
logging.getLogger("urllib3").setLevel(logging.WARNING)

log = logging.getLogger("rich")
log.info("Hello, World!")

if __name__ == '__main__':
    fire.Fire(CatalogerCli)
