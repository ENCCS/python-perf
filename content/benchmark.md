# Benchmark

:::{objectives}

- Introduce the 
- Preparing the system for benchmarking
- Running benchmarks

:::

:::{instructor-note}

:::

## The problem: word-count-hpda

![word-count schematic](./img/arrows.png)

In this episode, we will use an
[example project](https://github.com/ENCCS/word-count-hpda)
which finds most frequent words in books and plots the result
from those statistics. The project contains a
script `source/wordcount.py` which is executed to analyze word 
frequencies from some books. The books are saved in plain-text format
in the [data](https://github.com/ENCCS/word-count-hpda/tree/main/data) directory.

For example to run this code for one book, *pg99.txt*

```console
$ git clone https://github.com/ENCCS/word-count-hpda.git
$ cd word-count-hpda 
$ python source/wordcount.py data/pg99.txt processed_data/pg99.dat
$ python source/plotcount.py processed_data/pg99.dat results/pg99.png
```

## Preparation: Use `pyperf` to tune your system

Most personal laptops would be running in a power-saver / balanced power management mode.
This would include that the system has a scaling governor which can change the CPU clock frequency on demand. This can cause **jitter**
which means that benchmarks are not reproducible enough and are less reliable.

In order to improve reliability of your benchmarks consider running the following

:::{warning}
It requires admin / root privileges.
:::

```console
# python -m pyperf system tune
```

## Benchmark using `time`

In order to observe the cost of computation, we need to choose a 
sufficiently large input data file and time the computation. We can
do that by concatenating all the books into a single input file
approximately 45 MB in size.


::::{tab-set}
:sync-group: env

:::{tab-item} IPython / Jupyter
:sync: ipy

Copy the following script.

```python
import fileinput
from pathlib import Path

files = Path("data").glob("pg*.txt")
file_concat = Path("data", "concat.txt")

with (
    fileinput.input(files) as file_in,
    file_concat.open("w") as file_out
):
    for line in file_in:
        file_out.write(line)
```

Open an IPython console or Jupyterlab, with `word-count-hpda` as the
current working directory (you can also use `%cd` inside IPython
to change the directory).

```ipython
%paste

%ls -lh data/concat.txt

import sys
sys.path.insert(0, "source")

import wordcount

%time wordcount.word_count("data/concat.txt", "processed_data/concat.dat", 1)
```


:::


:::{tab-item} Unix Shell
:sync: sh

```console
$ cat data/pg*.txt > data/concat.txt
$ ls -lh data/concat.txt
$ time python source/wordcount.py data/concat.txt processed_data/concat.dat


:::

::::

:::::{solution}

::::{tab-set}
:sync-group: env

:::{tab-item} IPython
:sync: ipy

```ipython
In [1]: %paste
import fileinput
from pathlib import Path

files = Path("data").glob("pg*.txt")
file_concat = Path("data", "concat.txt")

with (
    fileinput.input(files) as file_in,
    file_concat.open("w") as file_out
):
    for line in file_in:
        file_out.write(line)
## -- End pasted text --

In [2]: %ls -lh data/concat.txt
-rw-rw-r-- 1 ashwinmo ashwinmo 45M sep 24 14:54 data/concat.txt

In [3]: import sys
   ...: sys.path.insert(0, "source")

In [4]: import wordcount

In [5]: %time wordcount.word_count("data/concat.txt", "processed_data/concat.dat", 1)
CPU times: user 2.64 s, sys: 146 ms, total: 2.79 s
Wall time: 2.8 s
```

:::

:::{tab-item} Unix Shell
:sync: sh

```console
$ cat data/pg*.txt > data/concat.txt
$ ls -lh data/concat.txt
-rw-rw-r-- 1 ashwinmo ashwinmo 46M sep 24 14:58 data/concat.txt
$ time python source/wordcount.py data/concat.txt processed_data/concat.dat

real    0m2,826s
user    0m2,645s
sys     0m0,180s
```

:::

::::

:::::


## Benchmark using `timeit`

If you run the `%time` magic / `time` command again, you will notice 
that the results vary a bit. To get a **reliable** answer we should repeat
the benchmark several times using [`timeit`]. [`timeit`] is part of
the Python standard library and it can be imported in a Python script
or used via a command-line interface.

If you're using IPython / Jupyter notebook, the best choice will be
to use the `%timeit` magic.

[`timeit`]: https://docs.python.org/library/timeit.html

As an example, here we benchmark the Numpy array:

```ipython
import numpy as np

a = np.arange(1000)

%timeit a ** 2
# 1.4 µs ± 25.1 ns per loop
```


We could do the same for the `word_count` function.

::::{tab-set}
:sync-group: env

:::{tab-item} IPython / Jupyter
:sync: ipy

```ipython
In [6]: %timeit wordcount.word_count("data/concat.txt", "processed_data/concat.dat", 1)
# 2.81 s ± 12.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

```
:::

:::{tab-item} Unix Shell
:sync: sh

```sh
$ export PYTHONPATH=source
$ python -m timeit --setup 'import wordcount' 'wordcount.word_count("data/concat.txt", "processed_data/concat.dat", 1)'
# 1 loop, best of 5: 2.75 sec per loop
```
:::
::::

:::{keypoints}

- `pyperf` can be used to tune the system
- We understood the use of `time` and `timeit` to create benchmarks
- `time` is faster
- `timeit` is more reliable

:::