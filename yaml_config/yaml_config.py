import os
import yaml
import collections
import yaml_config.file_utils as file_utils


class YAMLConfig(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            #    print('Creating the object')
            cls._instance = super(YAMLConfig, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    def __init__(self, structure, config_path, config_name):

        assert isinstance(
            structure, collections.OrderedDict
        ), "the structure must be in the form of an ordered dict"

        self._default_structure = structure
        self._config_path = file_utils.sanitize_filename(config_path)
        self._config_name = config_name
        self._full_path = os.path.join(self._config_path, self._config_name)

        self._check_if_existing()

    def read_config(self):

        with open(self._full_path, "r") as f:
            user_config_dict = yaml.load(f, Loader=yaml.SafeLoader)

        self._check_if_corrupt(user_config_dict):

        self._configuration = user_config_dict

        
            
    def _check_if_existing(self):

        if not file_utils.file_existing_and_readable(self._full_path):

            self._write_default_config()

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

    def _check_same_structure(self, d1, d2):
        """
        Return True if d1 and d2 have the same keys structure 
        (same set of keys, and all nested dictionaries have
        the same structure)

        :param d1: dictionary 1
        :param d2: dictionary 2
        :return: True or False
        """

        # This uses the fact that two dictionaries are equal if they have the same keys and the same values

        return self._subs_values_with_none(d1) == self._subs_values_with_none(d2)

    def _check_if_corrupt(self, user_config_dict):

        if not self._check_same_structure(user_config_dict, self._default_structure):

            self._backup_user_config(user_config_dict)
            self._write_default_config()

        for key, value in self._traverse_dict(user_config_dict):

            print (k, v)
            
    #    for key, value in self._traverse_dict(config_dict):

    def _write_default_config(self):

        file_utils.if_directory_not_existing_then_make(self._config_path)

        with open(self._full_path) as f:

            yaml.dump(f, self._default_structure, default_flow_style=False)

    def _backup_user_config(self, user_config_dict):

        pass
            
    def _traverse_dict(self, d):

        for key in d:

            if isinstance(d[key], dict):

                for key, value in self._traverse_dict(d[key]):

                    yield key, value

            else:

                yield key, d[key]

    def __getitem__(self, key):

        if key in self._configuration:

            return self._configuration[key]

        else:

            raise ValueError(
                "Configuration key %s does not exist in %s." % (key, self._filename)
            )

    def __repr__(self):

        return yaml.dump(self._configuration, default_flow_style=False)
