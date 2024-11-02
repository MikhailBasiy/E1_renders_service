import pathlib
import shutil

import logging
from datetime import datetime


logging.basicConfig(
    level="DEBUG", 
    filename=f"logs/card_conf_{datetime.now().strftime('%m-%d_%H-%M')}.log", 
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
    encoding='utf-8')


def delete_dir_contents(dir_path: pathlib.Path) -> None:
    logging.info("Запущено удаление файлов в директориях")
    for path in dir_path.glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
    logging.info(f"Директория {dir_path} не содержит файлов и папок")
    return


def get_dir_ready(dir_name: str) -> pathlib.Path:
    dir_path = pathlib.Path(dir_name)
    dir_path.mkdir(exist_ok=True)
    delete_dir_contents(dir_path)
    return dir_path