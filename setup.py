#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Jeroen Ubbink",
    author_email='info@jeroenubbink.nl',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Sync upload pictures directly to a Piwigo album.",
    entry_points={
        'console_scripts': [
            'syncthing2piwigo=syncthing2piwigo.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='syncthing2piwigo',
    name='syncthing2piwigo',
    packages=find_packages(include=['syncthing2piwigo', 'syncthing2piwigo.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jeroenubbink/syncthing2piwigo',
    version='0.1.0',
    zip_safe=False,
)
