# Benchmark

- Preparing the system for benchmarking
- Running benchmarks

:::{objectives}

:::

:::{instructor-note}

:::

## Preparing: Use `pyperf` to tune your system

Most personal laptops would be running in a power-saver / balanced power management mode.
This would include that the system has a scaling governor which can change the CPU clock frequency on demand. This can cause **jitter**
which means that benchmarks are not reproducible enough and are less reliable.
In order to improve this consider running the following

:::{warning}
It requires admin / root privileges.
:::

```console
# python -m pyperf system tune
```

## Benchmark problem

- Sorting
- N-Body problem
