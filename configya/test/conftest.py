import os
import shutil
import pytest
from configya.yaml_config import YAMLConfig

from pathlib import Path


_test_path = Path("config_test")
_test_file = "test.yml"

def rm_tree(pth):
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()


@pytest.fixture(scope="session")
def structure():

    structure = {}

    structure["val1"] = 1.0
    structure["val2"] = "crap"
    structure["sub1"] = {"val1": 5.0, "x2": "crap"}
    structure["sub2"] = {"sub3": {"y": 4.0}}

    return structure


@pytest.fixture(scope="function")
def config_class(structure):
    class MyConfig(YAMLConfig):

        def __init__(self):
            super(MyConfig, self).__init__(
                structure=structure, config_path=_test_path, config_name=_test_file
        )

    return MyConfig


@pytest.fixture(scope="function")
def config(config_class):
    my_config = config_class()

    yield my_config

    rm_tree(_test_path)

@pytest.fixture(scope="function")
def bad_structure():

    bad_structure = {}

    bad_structure["val1"] = 10.0
#    bad_structure["val2"] = "crap"
    bad_structure["sub1"] = {"val1": 5.0, "x2": "crap"}
    bad_structure["sub2"] = {"sub3": {"y": 4.0}, 'what': 4}
    bad_structure["val3"] = 'i should not be here'

    return bad_structure
    

@pytest.fixture(scope="session")
def wrong_type_structure():

    wrong_type_structure = {}

    wrong_type_structure["val1"] = 1.0
    wrong_type_structure["val2"] = 9
    wrong_type_structure["sub1"] = {"val1": 5.0, "x2": "crap"}
    wrong_type_structure["sub2"] = {"sub3": {"y": 4.0}}

    return wrong_type_structure

