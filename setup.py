from __future__ import absolute_import

from setuptools import setup, find_packages

description = """DI-smartcross: OpenDILab Decision Intelligence Traffic Signal Control Platform"""

setup(
    name='DI-smartcross',
    version='0.1.0',
    description='OpenDILab Decision Intelligence Traffic Signal Control Platform',
    long_description=description,
    author='OpenDILab',
    license='Apache 2.0',
    keywords='Decision Intelligence, Reinforcement Learning, Traffic Signal Control',
    packages=[
        *find_packages(include=('smartcross', 'smartcross.*')),
    ],
    # scripts=[
    #     'entry/sumo_train',
    #     'entry/sumo_eval',
    # ],
    install_requires=[
        "torch>=1.4,<=1.8",
        "di-engine>=0.2",
        "sumolib",
        "traci",
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
        ],
        'style': [
            'yapf==0.29.0',
            'flake8',
        ],
    }
)
