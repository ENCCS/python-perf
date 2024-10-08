# Performance fundamentals

:::{objectives}

- Learn Python specific performance aspects
:::

:::{instructor-note}

- 10 min teaching/type-along
:::

## Understanding the Python interpreter

:::{discussion} Performance bottlenecks in Python

Have you ever written Python scripts that look something like this?

```python
def read_xyz_from_text_file():
    f = open("mydata.dat", "r")
    for line in f.readlines():
        fields = line.split(",")
        x, y, z = fields[0], fields[1], fields[2]
        # some analysis with x, y and z
    f.close()
```

Compared to C/C++/Fortran, this for-loop will probably be orders of magnitude slower!

:::

This happens because during the execution step CPython mostly interprets instructions. There is some level of optimization involved though. Here is a simplified schematic of how this is invoked:

```{mermaid}
flowchart TD
    a[Source code in .py files] --> tok[Tokenizer]
    tok --> ast[Abstract Syntax Tree]
    ast --> c[Byte-code: __pycache__]
    c --> d[Machine code in Python Virtual Machine]
    d --> c
```

:::{important}

While doing so, the interpreter

- evaluates a result, expression-by-expression.
- every intermediate result is packed and unpacked as an instance of `object` (Python) / `PyObject` (CPython API) behind the scenes.

:::

:::{type-along}

Try out the following code in [Python Tutor]

```python
import io

def rms_from_text_file(f):
    """Compute root-mean-square of comma-separated values."""
    rms = 0
    n_samples = 0
    
    for line in f.readlines():
        fields = line.split(",")
        x, y, z = float(fields[0]), float(fields[1]), float(fields[2])
        # compute root-mean-square value
        rms += ((x**2 + y**2 + z**2) / 3) ** 0.5
        n_samples += 1
        
    return rms / n_samples


fake_file = io.StringIO("""\
0.27194615,0.85939776,0.76905204
0.51586611,0.59174447,0.06501842
0.23109192,0.8260391,0.08045166
""")

avg_rms = rms_from_text_file(fake_file)
```

Be aware that this is a simplified version of the execution. Since it does not go into
the expression level. However you can get an idea of the intermediate objects being
returned and the way the interpreter parses the code.

:::

[Python Tutor]: https://pythontutor.com/render.html#code=import%20io%0A%0Adef%20rms_from_text_file%28f%29%3A%0A%20%20%20%20%22%22%22Compute%20root-mean-square%20of%20comma-separated%20values.%22%22%22%0A%20%20%20%20rms%20%3D%200%0A%20%20%20%20n_samples%20%3D%200%0A%20%20%20%20%0A%20%20%20%20for%20line%20in%20f.readlines%28%29%3A%0A%20%20%20%20%20%20%20%20fields%20%3D%20line.split%28%22,%22%29%0A%20%20%20%20%20%20%20%20x,%20y,%20z%20%3D%20float%28fields%5B0%5D%29,%20float%28fields%5B1%5D%29,%20float%28fields%5B2%5D%29%0A%20%20%20%20%20%20%20%20%23%20compute%20root-mean-square%20value%0A%20%20%20%20%20%20%20%20rms%20%2B%3D%20%28%28x**2%20%2B%20y**2%20%2B%20z**2%29%20/%203%29%20**%200.5%0A%20%20%20%20%20%20%20%20n_samples%20%2B%3D%201%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20return%20rms%20/%20n_samples%0A%0A%0Afake_file%20%3D%20io.StringIO%28%22%22%22%5C%0A0.27194615,0.85939776,0.76905204%0A0.51586611,0.59174447,0.06501842%0A0.23109192,0.8260391,0.08045166%0A%22%22%22%29%0A%0Aavg_rms%20%3D%20rms_from_text_file%28fake_file%29&cumulative=false&curInstr=0&heapPrimitives=nevernest&mode=display&origin=opt-frontend.js&py=311&rawInputLstJSON=%5B%5D&textReferences=false

:::{discussion}

In the previous episode, we described I/O, Memory and CPU bound bottlenecks.
For the above use case and **algorithm**, and **not necessarily the same code**,
what kind of performance issue arise,

1. when the file becomes long, with several millions of lines?
1. when the file is stored in network filesystem which is slow to respond?
1. when instead of 3 fields, `x, y, z`, you have to read 10 million fields for every line of the text?

:::

:::{solution}
We can only guess at this point, but we can expect the above code to be

1. **CPU bound**: the `for` loop becomes a _hotspot_ and vanilla CPython
   without JIT does not optimize this.
2. **I/O bound**: if more time is spent in awaiting output of `f.readlines()` method
3. **Memory bound**: if a line of data does not fit in the memory the code needs to
   handle it in batches. The program will need to be rewritten with nested for-loop
   which depends on the memory availability.

We have to keep in mind that performance depends a lot on the kind of

- input data
- algorithm

Using a better container for the input data or a better algorithm with less
[computation complexity](https://en.wikipedia.org/wiki/Computational_complexity)
can often outperform technical solutions.

:::

## Structured approach towards optimization

The first priority is to look for an more efficient:

1. Data container, data structure, database etc.
2. Algorithm

If the above are not an option, then we move on to performance optimization.

1. First we evaluate the overall performance by **benchmarking**.
2. Then we measure the performance of at either function/method-level or line-level by **profiling**.
3. Finally we generate optimized code.

Any Python code can be replaced using optimized instructions. This is done by
ahead of time (AOT) / just-in-time (JIT) compilation. The question which
remains to be answered is at which level? One can optimize:

![program clip-art](./img/noun_programming.svg){w=30px} : whole programs (Nuitka, Shed Skin)

![interpreter: terminal console clip-art](./img/noun_terminal.svg){w=30px} : interpreter compiling slowest loops (PyPy)

![module: blocks clip-art](./img/noun_module.svg){w=30px} : **modules (`cython`, `pythran`)**

![function clip-art](./img/noun_function.svg){w=30px} : **user-defined functions / methods (`numba`, `transonic`)**

![equality clip-art](./img/noun_equals.svg){w=30px} : **expressions** (`numexpr`)

![function clip-art](./img/noun_function.svg){w=30px} : call compiled functions (`numpy` / Python)

We will take a look at some of these approaches in the coming episodes.

:::{keypoints}

- Develop a strategy on **how** to optimize.
- Go shopping.
  - Look for better ways of reading data or better algorithms
  - Look for tools and libraries to help you alleviate the performance bottlenecks.
:::
