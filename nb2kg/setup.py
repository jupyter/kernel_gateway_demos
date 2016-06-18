# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os
import sys
from setuptools import setup

# Get location of this file at runtime
HERE = os.path.abspath(os.path.dirname(__file__))

# Eval the version tuple and string from the source
VERSION_NS = {}
with open(os.path.join(HERE, 'nb2kg', '_version.py')) as f:
    exec(f.read(), {}, VERSION_NS)

install_requires=[
    'notebook>=4.2.0,<5.0',
]

setup_args = dict(
    name='nb2kg',
    author='Jupyter Development Team',
    author_email='jupyter@googlegroups.com',
    description='Extension for Jupyter Notebook 4.2.x to enable remote kernels hosted by Kernel Gateway',
    long_description = '''See `the README <https://github.com/jupyter/kernel_gateway_demos/nb2kg>`_ for more information.
''',
    url='https://github.com/jupyter/kernel_gateway_demos/nb2kg',
    version=VERSION_NS['__version__'],
    license='BSD',
    platforms=['Jupyter Notebook 4.2.x'],
    packages=[
        'nb2kg'
    ],
    include_package_data=True,
    scripts=[
    ],
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ]
)

if __name__ == '__main__':
    setup(**setup_args)
