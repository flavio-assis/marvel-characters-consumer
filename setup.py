from setuptools import setup, find_packages
import os

VERSION = os.getenv('VERSION', '0.0.1')

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='marvel-characters-consumer',
    version=VERSION,
    description='N26 Challenge - Marvel Characters Consumer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(exclude=['tests*']),
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'load-characters-df=src.main:main'
        ]
    }
)
