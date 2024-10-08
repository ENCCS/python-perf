# Python performance workshop

This mini-workshop is intended for Python developers who are interested in writing code with
better performance and potentially running it on supercomputers.

:::{prereq}

- Python programming basics (functions, `for` loops, `if`-`else` statements)
  and data structures (`list`, `set`, `dict`, `tuple`)
- Familiarity with well-known numeric libraries (for example, Numpy)
:::

```{csv-table}
:delim: ;
:widths: auto

5 min ; {doc}`setup`
5 min ; {doc}`intro`
10 min ; {doc}`perf-fundamentals`
15 min ; {doc}`benchmark`
15 min ; {doc}`profile`
5-10 min ; **Break**
15 min ; {doc}`optimize`
5 min ; {doc}`parallelize`
```

```{toctree}
:caption: Preparation
:maxdepth: 1

setup
```

```{toctree}
:caption: The lesson
:maxdepth: 1

intro
perf-fundamentals
benchmark
profile
optimize
parallelize
```

```{toctree}
:caption: Reference
:maxdepth: 1

quick-reference
guide
```

(learner-personas)=

## Who is the course for?

Software developers, researchers, students who use Python often and process a lot of data.

## Credits

The lesson is inspired and derived from the following:

### Creative Commons [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/) licensed material

- https://github.com/ENCCS/hpda-python
- https://github.com/ENCCS/word-count-hpda
- https://github.com/coderefinery/word-count
- https://coderefinery.github.io/reproducible-research
- https://hpc-carpentry.github.io/hpc-python/
- Images and description by [authors of lectures.scientific-python.org](https://lectures.scientific-python.org/preface.html#authors) 
and by [authors of deep-learning-intro](https://github.com/carpentries-incubator/deep-learning-intro/blob/main/AUTHORS)
- PyCon Sweden 2019 talk on https://talks.fluid.quest/

### Other open-source licenced material

- Images by [authors of Project Jupyter](https://jupyter.org) is licensed under [BSD 3-Clause "New" or "Revised" License](https://github.com/jupyter/jupyter.github.io/blob/main/LICENSE)
- Images from [The Noun Project](https://thenounproject.com) is licensed under [CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/.)
- Code from <https://github.com/paugier/nbabel> is licensed under [GPLv2](https://github.com/paugier/nbabel/blob/main/LICENSE)
- Video from <https://en.wikipedia.org/wiki/File:Galaxy_collision.ogv> licensed under [CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/.)