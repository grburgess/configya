from setuptools import setup
import os
import versioneer




setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass()

)
