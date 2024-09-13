# Installation

This page contains instructions for installing the required dependencies
on a local computer.

## Local installation

If you already have a preferred way to manage Python versions and
libraries, you can stick to that. If not, we recommend that you install
Python3 and all libraries using
[miniconda](https://docs.conda.io/en/latest/miniconda.html), a free
minimal installer for the package, dependency and environment manager
[conda](https://docs.conda.io/en/latest/index.html).

Please follow the installation instructions on
<https://docs.conda.io/en/latest/miniconda.html> to install Miniconda3.

Make sure that both Python and conda are correctly installed:

``` console
$ python --version
$ # should give something like Python 3.12.5
$ conda --version
$ # should give something like conda 24.7.1
```

With conda installed, install the required dependencies by running:

``` console
$ conda env create -f https://raw.githubusercontent.com/ENCCS/python-perf/main/content/env/environment.yml
```

This will create a new environment `pyperf` which you need to activate
by:

``` console
$ conda activate pyperf
```

Finally, open Jupyter-Lab in your browser:

``` console
$ jupyter-lab
```
