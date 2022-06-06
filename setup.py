# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Module setuptools script."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
meta = {}
with open(os.path.join(here, 'smartcross', '__init__.py'), 'r') as f:
    exec(f.read(), meta)

description = """DI-smartcross: OpenDILab Decision Intelligence Traffic Crossing Signal Control Platform"""

setup(
    name=meta['__TITLE__'],
    version=meta['__VERSION__'],
    description=meta['__DESCRIPTION__'],
    long_description=description,
    author=meta['__AUTHOR__'],
    license='Apache License, Version 2.0',
    keywords='Decision Intelligence, Reinforcement Learning, Traffic Signal Control',
    packages=[
        *find_packages(include=('smartcross', 'smartcross.*')),
    ],
    scripts=[
        'entry/sumo_train',
        'entry/sumo_eval',
        'entry/cityflow_train',
        'entry/cityflow_eval',
    ],
    install_requires=[
        "di-engine>=0.3",
        "torch>=1.4,<=1.8",
        "sumolib",
        "traci",
        "MarkupSafe<=2.0.1'",
    ],
    extras_require={
        'doc': [
            'sphinx>=2.2.1',
            'sphinx_rtd_theme~=0.4.3',
            'enum_tools',
            'sphinx-toolbox',
        ],
        'test': [
            'pytest==5.1.1',
            'pytest-xdist==1.31.0',
            'pytest-cov==2.8.1',
            'pytest-forked~=1.3.0',
            'pytest-mock~=3.3.1',
            'pytest-rerunfailures~=9.1.1',
            'pytest-timeouts~=1.2.1',
            'opencv-python-headless',
            'protobuf<=3.20.1',
        ],
        'style': [
            'yapf==0.29.0',
            'flake8',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research/Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
