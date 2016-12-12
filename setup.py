#!/usr/bin/env python
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    README = readme_file.read()


install_requires = [
    'flywheel>=0.5.1',
    'PyYAML',
    'boto3',
    'placebo'
]


setup(
    name='tight',
    version='0.1.0',
    description="Microframework",
    long_description=README,
    author="Michael McManus",
    author_email='michaeltightmcmanus@gmail.com',
    url='https://github.com/michaelorionmcmanus/tight',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    license='MIT',
    package_data={'tight': ['*.json']},
    include_package_data=True,
    package_dir={'tight': 'tight'},
    zip_safe=False,
    keywords='tight',
    entry_points={},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
)
