Installation
#################

.. toctree::
    :maxdepth: 2

Here we provide user-friendly installation for **DI-smartcross** and all simulators we support.

.. note::

    You can choose the simulators your experiments needed    and install it only to run your experiments.


SUMO installation
=====================

**DI-smartcross** supports SUMO version >= 1.6.0. Here we demonstrate
two easy ways of SUMO installation on Linux.

Install SUMO via apt-get or homebrew
--------------------------------------

On Debian or Ubuntu, SUMO can be directly installed using ``apt``:

.. code:: bash

    sudo add-apt-repository ppa:sumo/stable
    sudo apt-get update
    sudo apt-get install sumo sumo-tools sumo-doc

On macOS, SUMO can be installed using ``homebrew``.

.. code:: bash

    brew update
    brew tap dlr-ts/sumo
    brew install sumo
    brew install --cask sumo-gui

After that, you need to set the ``SUMO_HOME`` environment variable pointing to the directory 
of your SUMO installation by inserting the following line at the end of ``.bashrc``:

.. code:: bash

    export SUMO_HOME=/your/path/to/sumo

There might be some trouble arising when installing with the method above. It is recommended
to build and install SUMO from the source code as follows.

Install SUMO from the source code
---------------------------------

Here we show step-by-step guidance of installation with SUMO 1.8.0 on Linux.

1. install required libraries and dependencies

.. code:: bash

    sudo apt-get install cmake python g++ libxerces-c-dev libfox-1.6-dev libgdal-dev libproj-dev libgl2ps-dev swig

2. download and unzip the installation package

.. code:: bash

    tar xzf sumo-src-1.8.0.tar.gz
    cd sumo-1.8.0
    pwd 

3. compile SUMO

.. code:: bash

    mkdir build/cmake-build
    cd build/cmake-build
    cmake ../..
    make -j $(nproc)

4. environment variables

.. code:: bash

    echo 'export PATH=$HOME/sumo-1.8.0/bin:$PATH
    export SUMO_HOME=$HOME/sumo-1.8.0' | tee -a $HOME/.bashrc
    source ~/.bashrc

5. check install

.. code:: bash

    sumo

If successful, the following message will be shown in the shell.

.. code::

    Eclipse SUMO sumo Version 1.8.0
    Build features: Linux-3.10.0-957.el7.x86_64 x86_64 GNU 5.3.1 Release Proj GUI SWIG GDAL GL2PS
    Copyright (C) 2001-2020 German Aerospace Center (DLR) and others; https://sumo.dlr.de
    License EPL-2.0: Eclipse Public License Version 2 <https://eclipse.org/legal/epl-v20.html>
    Use --help to get the list of options.


CityFlow Installation
==========================

CityFlow simulator can be installed from source code via `CMake <https://cmake.org>`_.
Please make sure it is correctly worked in your system.

Simply download their source code and run ``pip install`` in the root folder to install CityFlow.

.. code:: bash

    git clone https://github.com/cityflow-project/CityFlow.git
    cd CityFlow
    pip install .

You can check installation by running ``import cityflow`` in python.

Install DI-smartcross
==========================


Simply run `pip install` in the root folder of this repository. This will automatically 
install `DI-engine <https://github.com/opendilab/DI-engine>`_ as well.

.. code:: bash

    pip install -e . --user

You can check the installation by running the following command.

.. code:: bash

    python -c 'import ding; import smartcross'
