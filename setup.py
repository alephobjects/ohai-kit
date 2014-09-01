#!/usr/bin/env python
import os
from setuptools import setup, find_packages


setup(
    name='ohai_kit',
    version='1.0',
    url='http://github.com/alephobjects/ohai-kit',
    description='Open Hardware Assembly Instruction Kit',
    long_description='Open Hardware Assembly Instruction Kit',
    author='Avea Palecek',
    author_email='',
    platforms=['any'],
    packages=find_packages(),
    package_data={'ohai_kit': 
        ['static/ohai_kit/*.*',
         'static/ohai_kit/fonts/*.*',
         'templates/ohai_kit/*.*']
    },
    include_package_data=True,
    install_requires=[
        'django>=1.7c3',
        'easy_thumbnails',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    zip_safe=False,
)
