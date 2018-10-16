#!/usr/bin/env python3
# coding=utf-8

import sys
from distutils import core
from os.path import abspath, dirname

from setuptools import find_packages

__author__ = "Josef Kolář"

if sys.version_info < (3, 5):
    print('Run in python >= 3.5 please.', file=sys.stderr)
    exit(1)

base_path = abspath(dirname(__file__))


def setup():
    core.setup(
        name='ziscz',
        version='1.0.0',
        description='Package with website for local company.',
        author='Josef Kolář',
        author_email='thejoeejoee@gmail.com',
        packages=find_packages(),
        install_requires=[
            'Django',
            'gunicorn',
            'django-ckeditor',
            'django-loginas',
            'django-countries',
            'django-extensions',
            'django-webpack-loader',
            'Pillow',
            'django-imagekit',
            'django-rest-framework',
            'psycopg2-binary',
            'django-crispy-forms',
            'django-bootstrap-datepicker-plus',
            'django_select2',
        ],
        entry_points={
            'console_scripts': [
                'ziscz-manage=ziscz.manage:manage',
            ],
        },
        include_package_data=True,
    )


if __name__ == '__main__':
    setup()
