# Parallelize
:::{objectives}

- Learn what approaches exist to parallelize applications
- Showcase Dask

:::

:::{instructor-note}

- 5 min teaching/demo

:::

## Different ways to do parallelization

- **Data parallelization**:
    - split an array / data into chunks
    - do computation in separate processes / threads
    - combine it
    - **Libraries**: `mpi4py`, `dask`, `cython`, `numba`, `cupy`, `pythran`
- **Task parallelization**:
    - construct a task or a function
    - feed different sets input data
    - collect the results in a queue and write it
    - **Libraries**: 
        - Standard library: `multiprocessing`, `threading`, `queue`, `asyncio`, `concurrent.futures`
        - Third party: `trio`, `dask`, `ray`

Irrespective of the approach, one common consideration is that a
parallelized part of the code should be free from race-conditions.

In this episode we will showcase parallelizing using Dask.

## Dask

Dask is composed of two parts:

- Dynamic task scheduling optimized for computation. Similar to other workflow 
  management systems, but optimized for interactive computational workloads.
- "Big Data" collections like parallel arrays, dataframes, and lists that extend 
  common interfaces like NumPy, Pandas, or Python iterators to larger-than-memory 
  or distributed environments. These parallel collections run on top of dynamic 
  task schedulers.


:::{figure} img/dask-overview.svg
High level collections are used to generate task graphs which can be executed 
by schedulers on a single machine or a cluster. From the 
[Dask documentation](https://docs.dask.org/en/stable/)
:::

### Dask distributed and dashboard

Dask has a plugin package known as [distributed](https://distributed.dask.org/en/stable/)
which brings in the capability to tap into a variety of computing setups: ranging
from local machines to HPC/Supercomputers and Kubernetes clusters. It also has an integrated
web application called dashboard to monitor the application.

### Dask Bag

A Dask bag enables processing data that can be represented as a sequence of arbitrary 
inputs ("messy data"), like in a Python list. Dask Bags are often used to for 
preprocessing log files, JSON records, or other user defined Python objects.

We will content ourselves with implementing a dask version of the word-count problem, 
specifically the step where we count words in a text. 

::::{demo} Demo: Dask version of word-count

First navigate to the ``word-count-hpda`` directory. The serial version (wrapped in 
multiple functions in the ``source/wordcount.py`` code) looks like this:

:::{code-block} python

filename = './data/concat.txt'
DELIMITERS = ". , ; : ? $ @ ^ < > # % ` ! * - = ( ) [ ] { } / \" '".split()

with open(filename, "r") as input_fd:
    lines = input_fd.read().splitlines()

counts = {}
for line in lines:
    for purge in DELIMITERS:
        line = line.replace(purge, " ")
    words = line.split()
    for word in words:
        word = word.lower().strip()
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1    

sorted_counts = sorted(
    list(counts.items()),
    key=lambda key_value: key_value[1],
    reverse=True
)

sorted_counts[:10]
:::

A very compact ``dask.bag`` version of this code is as follows:

:::{code-block} python

import dask.bag as db

filename = './data/concat.txt'
DELIMITERS = ". , ; : ? $ @ ^ < > # % ` ! * - = ( ) [ ] { } / \" '".split()

text = db.read_text(filename, blocksize='1MiB')
sorted_counts = (
    text
    .filter(lambda word: word not in DELIMITERS)
    .str.lower()
    .str.strip()
    .str.split()
    .flatten()
    .frequencies().topk(10,key=1)
    .compute()
)

sorted_counts
:::

The last two steps of the pipeline could also have been done with a Dask dataframe
(which is the Dask equivalent of a Pandas dataframe):

:::{code-block} python

text = db.read_text(filename, blocksize='1MiB')
filtered = (
    text
    .filter(lambda word: word not in DELIMITERS)
    .str.lower()
    .str.strip()
    .str.split()
    .flatten()
)
ddf = filtered.to_dataframe(columns=['words'])
ddf['words'].value_counts().compute()[:10]
:::

::::

### Dashboard

Try adding the following snippet and visualize the run in a dashboard

```python
from dask.distributed import Client
client = Client()  # start distributed scheduler locally.
client
```

:::{callout} When to use Dask

There is no benefit from using Dask on small datasets. But imagine we were 
analysing a very large text file (all tweets in a year? a genome?). Dask provides 
both parallelisation and the ability to utilize RAM on multiple machines.

:::