import os
import shutil
import yaml
import pytest
from nested_diff import diff
from configya.yaml_config import YAMLConfig, BadStructureWarning, BadTypeWarning, NoConfigurationWarning
from configya.file_utils import file_existing_and_readable, sanitize_filename


_test_path = "config_test"
_test_file = "test.yml"
_bak_file  = f"{_test_file}.bak"
_full_path = sanitize_filename(os.path.join(_test_path,_test_file))


def rewrite_config(new_dict):


    with open(_full_path, 'w') as f:

        yaml.dump(new_dict, stream=f, Dumper=yaml.SafeDumper)


def test_create_file(config):

    # we should have a config now
    assert file_existing_and_readable(_full_path)

    print(config)

    #shutil.rmtree(_test_path)

def test_non_existing(config_class):

    with pytest.warns(NoConfigurationWarning):

        config = config_class()

    #shutil.rmtree(_test_path)
    
def test_bad_structure(config, bad_structure, config_class):

    # should create a test

    delattr(config_class, '_inst')
    #print(config)
    rewrite_config(bad_structure)


    with pytest.warns(BadStructureWarning):

        
        new_config = config_class()

    d = diff(new_config._default_structure, new_config._configuration)

    # make sure we have the default config now
    assert "D" not in d

    #shutil.rmtree(_test_path)

def test_bad_type(config, wrong_type_structure, config_class):

    # should create a test

    # this is a singleton so we need to trick it
    delattr(config_class, '_inst')
    #print(config)
    rewrite_config(wrong_type_structure)


    with pytest.warns(BadTypeWarning):

        
        new_config = config_class()

    assert new_config['val2'] == "crap"

    # make sure we have the default config now


    #shutil.rmtree(_test_path)



    
    
    
