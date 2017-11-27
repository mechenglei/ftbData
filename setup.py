# -*- coding: utf-8 -*-

__author__ = 'chenglei'

from setuptools import setup, find_packages

setup(
    name='ftbData',
    version='0.1.1',
    description=(
        'football games; score; football lottery'
    ),
    long_description=open('README.md').read(),
    author='chenglei',
    author_email='mechenglei@163.com',
    license='BSD License',
    packages=find_packages(),
    platforms=['win7', 'linux'],
    url='https://github.com/mechenglei/ftbData',
    install_requires=[
        'pandas',
        'pyquery'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries'
    ],
)
