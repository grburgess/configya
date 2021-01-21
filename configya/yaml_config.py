import os
import yaml
import warnings
from nested_diff import diff
import configya.file_utils as file_utils
from pathlib import Path

# from yaml_config.differ import differ
import json


class BadStructureWarning(RuntimeWarning):
    pass


class BadTypeWarning(RuntimeWarning):
    pass


class NoConfigurationWarning(RuntimeWarning):
    pass


class SingletonMeta(type):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_inst"):
            obj = super(SingletonMeta, cls).__call__(*args, **kwargs)
            cls._inst = obj
        return cls._inst


class YAMLConfig(object, metaclass=SingletonMeta):
    def __init__(self, structure: dict, config_path: str, config_name: str):

        assert isinstance(structure, dict), "the structure must be in the form of dict"

        self._default_structure: str = structure

        self._config_path: Path = file_utils.sanitize_filename(config_path)

        file_utils.if_dir_containing_file_not_existing_then_make(self._config_path)

        self._config_name: str = config_name
        self._full_path: Path = self._config_path / self._config_name

        if not self._is_existing():

            self._configuration = self._default_structure

        else:
            # now try to read
            self._read_config()

    def _read_config(self) -> None:
        """
        read the default config

        :returns: 
        :rtype: 

        """

        with self._full_path.open("r") as f:
            user_config_dict = yaml.load(f, Loader=yaml.SafeLoader)

            if user_config_dict is not None:
            
                self._check_if_corrupt(user_config_dict)

            else:

                self._configuration = self._default_structure
                
    def _is_existing(self) -> bool:
        """
        
        is if the file is there, if not write

        :returns: 
        :rtype: 

        """

        if not file_utils.file_existing_and_readable(self._full_path):

            warnings.warn(
                f"No configuration file found! Making one in {self._full_path}",
                NoConfigurationWarning,
            )

            self._write_default_config()

            return False

        else:

            return True

    def _check_if_corrupt(self, user_config_dict: dict) -> bool:
        """
        check if the user file is corrupt

        :param user_config_dict: 
        :returns: 
        :rtype: 

        """

        if not self._check_same_structure(user_config_dict):

            warnings.warn(
                f"The user config file {self._full_path} was corrupt",
                BadStructureWarning,
            )
            warnings.warn(
                f"and has been backed up to {self._full_path}.bak and replaced",
                BadStructureWarning,
            )
            warnings.warn(
                f"with the default config. The CURRENT config is now default",
                BadStructureWarning,
            )

            self._backup_user_config(user_config_dict)
            self._write_default_config()

            self._configuration = self._default_structure

        else:

            self._check_same_types(user_config_dict)

            self._configuration = user_config_dict

    def _check_same_structure(self, user_config_dict: dict) -> bool:
        """
        Return True if d1 and d2 have the same keys structure 
        (same set of keys, and all nested dictionaries have
        the same structure)

        :param d1: dictionary 1
        :param d2: dictionary 2
        :return: True or False
        """

        is_same = True
        d1 = self._subs_values_with_none(user_config_dict)
        d2 = self._subs_values_with_none(self._default_structure)

        difference = diff(d1, d2)

        if "D" in difference:

            is_same = False

        return is_same

    def _check_same_types(self, user_config_dict: dict) -> None:
        """
        
        check in the values all have the same types 
        and if not backup and replace


        :param user_config_dict: 
        :returns: 
        :rtype: 

        """

        replaced = []

        # this ensures the lists are ordered. It is one hell of a hack

        sorted_default = json.loads(json.dumps(self._default_structure, sort_keys=True))
        sorted_user = json.loads(json.dumps(user_config_dict, sort_keys=True))

        for (key1, value1), (key2, value2) in zip(
            self._traverse_dict(sorted_default), self._traverse_dict(sorted_user),
        ):

            assert key1 == key2, f"{key1} != {key2}"

            if not isinstance(value2, type(value1)):

                if self._is_number(value1) and self._is_number(value2):

                    # ok these are both numbers so we can ignore

                    continue

                warnings.warn(
                    f" The value of {key1} is {value2} of type {type(value2)} and should be of {type(value1)}",
                    BadTypeWarning,
                )
                warnings.warn(
                    f"we have backed up your old config in {self._full_path}.bak and replaced the corrupt values",
                    BadTypeWarning,
                )
                warnings.warn("with the default ones", BadTypeWarning)

                # keep track of what we will fix
                replaced.append([key2, value2, value1])

        self._backup_user_config(user_config_dict)

        # go thru and replace the values in place
        for key, bad_value, good_value in replaced:

            replace_inplace(user_config_dict, key, bad_value, good_value)

    def _write_default_config(self) -> None:

        file_utils.if_directory_not_existing_then_make(self._config_path)

        with open(self._full_path, "w") as f:

            yaml.dump(
                self._default_structure,
                stream=f,
                default_flow_style=False,
                Dumper=yaml.SafeDumper,
            )

    def _backup_user_config(self, user_config_dict: dict) -> None:
        """
        write the read in user config to a backup file
        in the same directory

        :param user_config_dict: 
        :returns: 
        :rtype: 

        """

        backup_file_name: Path = Path(f"{self._full_path}.bak)")

        with backup_file_name.open("w") as f:

            yaml.dump(
                user_config_dict,
                stream=f,
                default_flow_style=False,
                Dumper=yaml.SafeDumper,
            )

    def _traverse_dict(self, d):

        for key in d:

            if isinstance(d[key], dict):

                for key, value in self._traverse_dict(d[key]):

                    yield key, value

            else:

                yield key, d[key]

    def _subs_values_with_none(self, d):
        """
        This remove all values from d and all
        nested dictionaries of d, substituing all values with None

        :param d: input dictionary
        :return: a copy of d with all values substituted with None
        """
        if isinstance(d, dict):

            return {k: self._subs_values_with_none(d[k]) for k in d}

        else:

            # Replace all non-dict values with None.
            return None

    @staticmethod
    def _is_number(val):

        return type(val) == int or type(val) == float

    def __getitem__(self, key):

        if key in self._configuration:

            return self._configuration[key]

        else:

            raise ValueError(f"Configuration key {key} does not exist")

    def __setitem__(self, key, item):

        if key in self._configuration:

            assert not isinstance(
                self._configuration[key], dict
            ), f"Woah, you are going to overwrite the structure"

            self._configuration[key] = item

        else:

            raise ValueError(f"Configuration key {key} does not exist")

    def __repr__(self):

        print(self._full_path)

        return yaml.dump(self._configuration, default_flow_style=False)


def replace_inplace(data, match_key, match_value, repl):
    if isinstance(data, (dict, list)):
        for k, v in data.items() if isinstance(data, dict) else enumerate(data):
            if (v == match_value) and (k == match_key):
                data[k] = repl
            replace_inplace(v, match_key, match_value, repl)
