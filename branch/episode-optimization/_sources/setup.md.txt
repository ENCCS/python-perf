# Installation

This page contains instructions for installing the required dependencies
on a local computer.

## Local installation

If you already have a preferred way to manage Python versions and
libraries, you can stick to that[^1]. If not, we recommend that you install
Python3 and all libraries using
[Miniforge](https://conda-forge.org/download/), a free
minimal installer for the package, dependency and environment manager
[conda](https://docs.conda.io/en/latest/index.html).

Please follow the installation instructions on
<https://conda-forge.org/download/> to install Miniforge.

Make sure that both Python and conda are correctly installed:

``` console
$ python --version
$ # should give something like Python 3.12.5
$ conda --version
$ # should give something like conda 24.7.1
```

With conda (or mamba) installed, install the required dependencies by running:

``` console
$ conda env create -f https://raw.githubusercontent.com/ENCCS/python-perf/main/content/env/environment.yml
```

This will create a new environment `python-perf` which you need to activate
by:

``` console
$ conda activate python-perf
```

Finally, open Jupyter-Lab in your browser:

``` console
$ jupyter-lab
```

[^1]: If you are not using conda, to install the right Python dependencies, download the `requirements.txt` file from [this link](https://raw.githubusercontent.com/ENCCS/python-perf/main/content/env/requirements.txt). Then [follow this guide to create a virtual environment and activate it](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments). Finally inside the virtual environment run `python3 -m pip install -r requirements.txt`.