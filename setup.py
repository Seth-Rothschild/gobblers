# A standard setup.py file for a package named gobblers

from setuptools import setup, find_packages

setup(
    name='gobblers',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[ ],
    entry_points={
        'console_scripts': [
            'gobblers = gobblers.__main__:main'
        ]
    }
)

    