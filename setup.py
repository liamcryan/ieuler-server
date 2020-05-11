from setuptools import setup
from io import open

with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='ieuler-server',
    version='0.0.0',
    description='Interactive Project Euler Server',
    long_description=readme,
    packages=['app'],
    zip_safe=False,
    install_requires=[
        'flask', 'flask-sqlalchemy',
        # ieuler - not on pypi
    ],
)
