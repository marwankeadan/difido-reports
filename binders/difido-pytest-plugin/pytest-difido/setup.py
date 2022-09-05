#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-difido',
    version='0.1.0',
    author='Itai Agmon',
    author_email='itai.agmon@gmail.com',
    maintainer='Itai Agmon',
    maintainer_email='itai.agmon@gmail.com',
    license='MIT',
    url='https://github.com/itaiag/pytest-difido',
    description='PyTest plugin for generating Difido reports',
    long_description=read('README.rst'),
    py_modules=['definitions'],
    python_requires='>=3.5',
    include_package_data=True,
    install_requires=['pytest>=4.0.0', 'requests>=2.20.0', 'requests-toolbelt>=0.8.0'],
    packages= ["difido"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'difido = difido.plugin',
        ],
    },
)
