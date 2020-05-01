[![Travis CI w/ Logo](https://img.shields.io/travis/grburgess/configya/master.svg?logo=travis)](https://travis-ci.org/grburgess/configya)
[![codecov](https://codecov.io/gh/grburgess/configya/branch/master/graph/badge.svg)](https://codecov.io/gh/grburgess/configya)
![PyPI](https://img.shields.io/pypi/v/configya?style=plastic)
## status
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/grburgess/configya/master?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/grburgess/configya?style=for-the-badge)
![GitHub pull requests](https://img.shields.io/github/issues-pr/grburgess/configya?style=for-the-badge)
![GitHub contributors](https://img.shields.io/github/contributors/grburgess/configya?style=for-the-badge)


# configya

![alt text](https://raw.githubusercontent.com/grburgess/configya/master/logo.png)

```bash
pip install configya
```

## What is this?

I often make YAML configuration files for codes to input default parameters. I kept repeating myself and wanting more robustness to the structure required in the file... so I decided to make a generic one. 

## What it does?

* Inherit the **YAMLConfig** class and pass to the super  class a dict with the structure of your config and default values as well as the location and name of the config file.
* Upon creating a config object, it will check if there is an existing config, and if not create a default one
* If there is an existing config, it makes sure the structure and value types conform to default file structure and types
* If it finds errors, it yells at you, backs yours up and tries to correct the corrupted one. 
* Only simple values like strings and numbers are checked... but maybe more in the future

## What next?

fork it and add more... I'm sure this could be better

### Check it out


```python
from configya import YAMLConfig
```

Create a dictionary with the (nested) structure you desire and give it some default values


```python
my_structure = {}
my_structure['n_workers'] = 4
my_structure['server'] = dict(name='supercomputer', address='10.10.1.1')
my_structure['my_iq'] = 80
my_structure['hours_spent_this'] = 'too many'


```

Create your class somewhere in your package


```python
class MyConfig(YAMLConfig):  
    def __init__(self):

        super(MyConfig, self).__init__(my_structure,
                                       '~/.my_cool_program',
                                       'config.yml')
    
```

The first time you make it, the default config will be written. It will yell at you.


```python
config = MyConfig()

```

    /Users/jburgess/.environs/yaml_config/lib/python3.7/site-packages/configya-0.3.0-py3.7.egg/configya/yaml_config.py:84: NoConfigurationWarning: No configuration file found! Making one in /Users/jburgess/.my_cool_program/config.yml



```python
!ls /Users/jburgess/.my_cool_program/
```

    config.yml



Yes, it is there.


```python
config
```

    /Users/jburgess/.my_cool_program/config.yml





    hours_spent_this: too many
    my_iq: 80
    n_workers: 4
    server:
      address: 10.10.1.1
      name: supercomputer




```python
config['server']['name']
```




    'supercomputer'




```python
config['my_iq']
```




    80



Well...


```python
config['my_iq'] = 200
config['my_iq']
```




    200



### Safety first
It will not allow you to clobber nested dicts


```python
config['server'] = 5
```


    ---------------------------------------------------------------------------

    AssertionError                            Traceback (most recent call last)

    <ipython-input-10-3d0b32c9a17b> in <module>
    ----> 1 config['server'] = 5
    

    ~/.environs/yaml_config/lib/python3.7/site-packages/configya-0.3.0-py3.7.egg/configya/yaml_config.py in __setitem__(self, key, item)
        294         if key in self._configuration:
        295 
    --> 296             assert not isinstance(self._configuration[key], dict), f"Woah, you are going to overwrite the structure"
        297 
        298             self._configuration[key] = item


    AssertionError: Woah, you are going to overwrite the structure


Cannot add things that are not there


```python
config['ooops'] = 10
```

Or find them


```python
config['what?'] 
```

What if I manually change the config in my github repo, and the one on my local computer is not up to date?


```python
my_structure = {}
my_structure['n_workers'] = 4
my_structure['server'] = dict(name='supercomputer', address='10.10.1.1')
my_structure['my_iq'] = 80
my_structure['hours_spent_this'] = 'too many'
# Added a new number!
my_structure['total_number_of_postdocs'] = 1e5


```


```python
class MyConfig(YAMLConfig):  
    def __init__(self):

        super(MyConfig, self).__init__(my_structure,
                                       '~/.my_cool_program',
                                       'config.yml')
    
```


```python
config = MyConfig()
```

    /Users/jburgess/.environs/yaml_config/lib/python3.7/site-packages/configya-0.3.0-py3.7.egg/configya/yaml_config.py:109: BadStructureWarning: The user config file /Users/jburgess/.my_cool_program/config.yml was corrupt
      BadStructureWarning,
    /Users/jburgess/.environs/yaml_config/lib/python3.7/site-packages/configya-0.3.0-py3.7.egg/configya/yaml_config.py:113: BadStructureWarning: and has been backed up to /Users/jburgess/.my_cool_program/config.yml.bak and replaced
      BadStructureWarning,
    /Users/jburgess/.environs/yaml_config/lib/python3.7/site-packages/configya-0.3.0-py3.7.egg/configya/yaml_config.py:117: BadStructureWarning: with the default config. The CURRENT config is now default
      BadStructureWarning,



```python
config
```

    /Users/jburgess/.my_cool_program/config.yml





    hours_spent_this: too many
    my_iq: 80
    n_workers: 4
    server:
      address: 10.10.1.1
      name: supercomputer
    total_number_of_postdocs: 100000.0




```python
!ls /Users/jburgess/.my_cool_program/
```

    config.yml     config.yml.bak



Also, if you manually edit the config in an editor, it will check if the types are correct. If not, it will replace that value with the default value and backup your config


```python

```
