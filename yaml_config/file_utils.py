import os
import shutil
import tempfile
import uuid
from contextlib import contextmanager


def file_existing_and_readable(filename):
    sanitized_filename = sanitize_filename(filename)

    if os.path.exists(sanitized_filename):

        # Try to open it

        try:

            with open(sanitized_filename):

                pass

        except:

            return False

        else:

            return True

    else:

        return False


def path_exists_and_is_directory(path):
    sanitized_path = sanitize_filename(path, abspath=True)

    if os.path.exists(sanitized_path):

        if os.path.isdir(path):

            return True

        else:

            return False

    else:

        return False


def sanitize_filename(filename, abspath=False):
    sanitized = os.path.expandvars(os.path.expanduser(filename))

    if abspath:

        return os.path.abspath(sanitized)

    else:

        return sanitized


def if_directory_not_existing_then_make(directory):
    """
    If the given directory does not exists, then make it
    If a path is a file then check the parent dir
    :param directory: directory to check or make
    :return: None
    """

    sanitized_directory = sanitize_filename(directory)

    if not os.path.exists(sanitized_directory):

        os.makedirs(sanitized_directory)


def if_dir_containing_file_not_existing_then_make(filename):
    """
    If the given directory does not exists, then make it
    If basename of path contains a '.' we assume it is a file and check the parent dir
    :param filename: directory to check or make
    :return: None
    """

    sanitized_directory = sanitize_filename(filename)

    if "." in os.path.basename(sanitized_directory):
        sanitized_directory = os.path.dirname(sanitized_directory)

    if not os.path.exists(sanitized_directory):
        os.makedirs(sanitized_directory)

