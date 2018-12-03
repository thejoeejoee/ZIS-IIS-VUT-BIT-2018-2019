#!/usr/bin/env python3
# coding=utf-8

import sys
from distutils import core
from os.path import abspath, dirname

from setuptools import find_packages

__author__ = "Josef Kolář (xkolar71), Iva Kavánková (xkavan05), Son Hai Nguyen (xnguye16)"

if sys.version_info < (3, 5):
    print('Run in python >= 3.5 please.', file=sys.stderr)
    exit(1)

base_path = abspath(dirname(__file__))


def setup():
    core.setup(
        name='ziscz',
        version='1.0.0',
        description='Package with ZOO IS for VUT FIT.',
        author=__author__,
        packages=find_packages(),
        install_requires=[
            'Django>=2.1.1',
            'gunicorn>=19.9.0',
            'django-ckeditor>=5.6.1',
            'django-loginas>=0.3.4',
            'django-countries>=5.3.2',
            'django-extensions>=2.1.2',
            'django-webpack-loader>=0.6.0',
            'Pillow>=5.2.0',
            'django-imagekit>=4.0.2',
            'django-rest-framework>=0.1.0',
            'psycopg2-binary>=2.7.5',
            'django-crispy-forms>=1.7.2',
            'django-bootstrap-datepicker-plus>=3.0.5',
            'django_select2>=6.3.1',
            'django-colorful>=1.3',
            'django-js-reverse>=0.8.2',
            'django-relativefilepathfield>=1.0.3',
            'django-debug-toolbar>=1.10.1',
            'django-braces>=1.13.0',
            'python-dateutil>=2.7.5',
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
