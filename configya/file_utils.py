import os
import shutil
import tempfile
import uuid
from contextlib import contextmanager
from pathlib import Path


def file_existing_and_readable(filename) -> bool:
    
    sanitized_filename: Path = sanitize_filename(filename)

    return sanitized_filename.is_file()

def sanitize_filename(filename: str, abspath: bool=False) -> Path:

    sanitized: Path = Path(filename).expanduser()

    if abspath:

        return sanitized.absolute()

    else:

        return sanitized


def if_directory_not_existing_then_make(directory: str) -> None:
    """
    If the given directory does not exists, then make it
    If a path is a file then check the parent dir
    :param directory: directory to check or make
    :return: None
    """

    sanitized_directory: Path = sanitize_filename(directory)

    if not sanitized_directory.exists():

        os.makedirs(sanitized_directory)


def if_dir_containing_file_not_existing_then_make(filename: str):
    """
    If the given directory does not exists, then make it
    If basename of path contains a '.' we assume it is a file and check the parent dir
    :param filename: directory to check or make
    :return: None
    """

    sanitized_directory: Path = sanitize_filename(filename)

    if "."  in sanitized_directory.name:
        sanitized_directory = sanitized_directory.parent

    if not sanitized_directory.exists():
        sanitized_directory.mkdir(parents=True)
        

