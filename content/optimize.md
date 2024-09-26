# Optimize
:::{objectives}

- Optimize the most expensive function from the word-count-hpda project's `wordcount.py` script.
- Show how changes to algorithm influences the performance.
- Introduce a few Python **accelerators**: `cython`, `numba`, `pythran`
- Mention the library `transonic`

:::

:::{instructor-note}

- 15 min teaching/demo
- No type-along intended

:::

## Targeting the most expensive function

In the previous episode by profiling, we found out that `update_word_counts`
consumes around half of the CPU wall time and is called repeatedly. Here is
a snippet from profiling output.

```
...
         53473208 function calls in 8.410 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  1233410    4.151    0.000    7.204    0.000 source/wordcount.py:41(update_word_counts)
  ...
```

## Option 1: changing the algorithm

If we look at the output from the line profiler, we can see that the following two lines 
are the most time-consuming.

:::{code-block} python
:emphasize-lines: 8,9

def update_word_counts(line, counts):
    """
    Given a string, parse the string and update a dictionary of word
    counts (mapping words to counts of their frequencies). DELIMITERS are
    removed before the string is parsed. The function is case-insensitive
    and words in the dictionary are in lower-case.
    """
    for purge in DELIMITERS:
        line = line.replace(purge, " ")
    words = line.split()
    for word in words:
        word = word.lower().strip()
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
:::

::::{demo}
Instead of a `for` loop and a `str.replace` we could use a single regular 
expression substitution. This change would look like this

:::{literalinclude} wordcount/v0_1.py
:start-after: using regex
:end-before: calculate_word_counts
:::

If we run our benchmark with the original code (`v0.py`) and the regex version (`v0_1.py`),
we get

```console

$ time python v0.py data/concat.txt processed_data/concat.dat

real    0m2,934s
user    0m2,733s
sys     0m0,191s
$ time python v0_1.py data/concat.txt processed_data/concat.dat

real    0m2,472s
user    0m2,320s
sys     0m0,147s

```

:::{discussion} Summary
- There is a marginal gain of ~0.5 s which amounts to a 16% performance boost.
- Such changes are less maintainable, but sometime necessary.
:::
::::



## Option 2: using an accelerator

### Accelerators

The following are the few well-known accelerators for Python-Numpy applications.

:::{csv-table}
:header: >
:    "Accelerator", "Compiles", "Implemented in", "Level",  "Supports", "Advantage"
:widths: 10, 10, 5, 5, 10, 20
Cython, "Ahead of time", C, Module, "All of Python, Numpy, and C", "Generic and can also interface C,C++"
Pythran, "Ahead of time", C++, Module, "Most Python and Numpy features", "Escapes GIL always, can optimize vectorized code without loops. Can parallelize using OpenMP."
Numba, "Just in time", LLVM, Function, "Most Python and Numpy features", "Specializes in Numeric codes. Has GPU support, can parallelize"
Jax, "Just in time", C++, "Function or Expression", "Most Python and Numpy features", "Drop-in alternative for Numpy. Designed for creating ML libraries"
Cupy, "Pre-compiled / JIT", "Cython / C / C++", "Function or Expression", "Numpy and Scipy", "Drop-in alternative for Numpy. Supports CUDA and ROCm GPUs"
:::


### Refactoring

One complication with optimizing `update_word_counts` is that it is an
impure function. In other words, it has some side-effects since it:

1. accesses a global variable `DELIMITERS`, and
1. mutates an external dictionary `counts` which is a local variable
   inside the function `calculate_word_counts`.

Thus the function `update_word_counts` on its own can be complicated for
an accelerator to compile since the types of the external variables are unknown. 

:::{code-block} python
:emphasize-lines: 8,14,16

def update_word_counts(line, counts):
    """
    Given a string, parse the string and update a dictionary of word
    counts (mapping words to counts of their frequencies). DELIMITERS are
    removed before the string is parsed. The function is case-insensitive
    and words in the dictionary are in lower-case.
    """
    for purge in DELIMITERS:
        line = line.replace(purge, " ")
    words = line.split()
    for word in words:
        word = word.lower().strip()
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1


:::


:::{literalinclude} wordcount/v0.py
:lines: 3-3

:::
:::{literalinclude} wordcount/v0.py
:pyobject: calculate_word_counts

:::

<!-- One possible way to avoid side-effects is to fold all the above
inside `calculate_word_counts` function.

:::{literalinclude} wordcount/v1_0.py
:pyobject: calculate_word_counts

::: -->

#### Cython

In this example we shall demonstrate **Cython** via a package called
**Transonic** . Transonic lets you switch between Cython, Numba, Pythran and to some extent
Jax using very similar syntax

To use Transonic we add decorators to functions we need to optimize.
There are two decorators

- `@transonic.boost` to create ahead-of-time (AOT) compiled modules and it requires type annotations
- `@transonic.jit` to create just-in-time (JIT) compiled modules where type is inferred on runtime

The advantage of using transonic is that you can quickly find out which accelerator works best
while preserving the Python code for debugging and future development. It also abstracts away the
syntax variations that Cython, Pythran etc. have.

The accelerator backend can be chosen in 3 ways:

1. Using an environment variable, `export TRANSONIC_BACKEND=cython`
1. As a parameter to the decorator, `@boost(backend="cython")`
1. As a parameter to the Transonic CLI, `transonic -b cython /path/to/file.py`

We shall use the `@boost` decorator and the environment variable `TRANSONIC_BACKEND` for simplicity

::::{demo}

We make a few changes to the code:

- Pull `DELIMITERS` inside `update_word_counts` function
- Add `@boost` decorators
- Add type annotations as [required by transonic](https://transonic.readthedocs.io/en/latest/examples/type_hints.html).

Cython has an ability to create _inline functions_ and this is also supported in Transonic. Therefore
it is OK that `update_word_counts` is impure.

:::{literalinclude} wordcount/v1_1.py
:start-after: optimize using transonic
:end-before: def word_count_dict_to_tuples

:::

Then compile the file [](./wordcount/v1_1.py)

```console
$ export TRANSONIC_BACKEND=cython
$ transonic v1_1.py 
...
1 files created or updated needs to be cythonized
$ ls -1 __cython__/
build
v1_1_ee8b793c43119b782190c854a1eb2ba7.cpython-312-x86_64-linux-gnu.so
v1_1.pxd
v1_1.py
```

This would auto-generate a module containing only the functions to be optimized and also compiles it.
While running the application, Transonic takes care of swapping the Python function with the compiled
counterpart.

We are ready to benchmark this.

```console
$ time python v1_1.py data/concat.txt processed_data/concat.dat

real    0m4,071s
user    0m4,373s
sys     0m0,288s
```


:::{discussion} Summary
**We see that the compiled function made the script slower**! This could happen because of a few reasons
- Python's dictionary which uses hash-maps, is quite optimized and it is hard to beat it
- Cython interacts with Python a lot. This can be analyzed by running `cd __cython__; cythonize --annotate v1_1.py`
  which generates the following HTML page.

![](./img/Cython_v1_1_py.png)

- Pythran can be used to escape interaction the GIL, but it has a similar performance. Source code: 
  [](./wordcount/v1_2.py) and [](./wordcount/v1_2_pythran.py)
:::

::::

### When do we use accelerators?

#### An example: Astrophysics N-body problem
To simulate an [N-body problem](https://en.wikipedia.org/wiki/N-body_simulation) using a naive algorithm involves
{math}`O(N^2)` operations for each time-step. ![](./img/Galaxy_collision.mp4){w=1px}


<video controls width="640">
  <source src="./_images/Galaxy_collision.mp4" type="video/mp4" />
  Simulation of the interactions between two galaxies as they pass by each other. The simulation contains 5000 Stars.
  Source: <https://en.wikipedia.org/wiki/File:Galaxy_collision.ogv>
</video>


##### Naive Python version

It uses a list of Numpy arrays!

:::{literalinclude} ./nbabel/bench0.py

:::

##### Numpy vectorized version

:::{literalinclude} ./nbabel/bench_numpy_highlevel.py

:::

::::{demo}

**Data** for 16-bodies: [](./nbabel/input16)

- Naive Python version: [](./nbabel/bench0.py)
- Numpy vectorized version: [](./nbabel/bench_numpy_highlevel.py)
- Numpy vectorized version + JIT compilation using Transonic and Pythran: [](./nbabel/bench_numpy_highlevel_jit.py)

```console
$ time python bench0.py input16
$ time bench_numpy_highlevel.py input16
$ export TRANSONIC_BACKEND=pythran
$ time bench_numpy_highlevel_jit.py input16  # Rerun after Pythran module is compiled
```

:::{solution}

```console
$ time python bench0.py input16
...
run in 0:00:12.637249

$ time bench_numpy_highlevel.py input16
...
10001 time steps run in 0:00:04.297485

$ export TRANSONIC_BACKEND=pythran
$ time bench_numpy_highlevel_jit.py input16  # Rerun after Pythran module is compiled
...
10001 time steps run in 0:00:00.042925
```

~300x speedup by using Pythran!

::::

:::{keypoints}

- Algortihmic optimizations are often better
- Accelerators work well with contiguous data structures
- The word-count problem is a poor candidate, but when it involves
  contiguous data structures such as arrays of numbers
  these accelerators can give amazing performance boosts. See here:
    - <https://enccs.github.io/hpda-python/performance-boosting/>
    - <https://github.com/paugier/nbabel/>


:::