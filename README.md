## Jinja Atoms [![Build Status](https://travis-ci.org/semirook/jinja-atoms.png)](https://travis-ci.org/semirook/jinja-atoms)
Atomic inclusion blocks extension for Jinja2 template engine

## Installation
As usual, via pip:

```bash
$ pip install jinja-atoms
```

Sure, you have to have the `jinja2` package already installed in the active python environment 
(it's the only extension dependency).

## Registration
If you use Jinja in non-Flask project, just add extension into your Jinja environment definition:

```python
from jinja2 import Environment
from jinja_atoms.ext import JinjaAtomsExtension
...
env = Environment(
  extensions=[JinjaAtomsExtension],
  ...
)
...
```

The registration is even simpler in Flask:
```python
from jinja_atoms.ext import JinjaAtomsExtension
...
app.jinja_env.add_extension(JinjaAtomsExtension)
...
```
where `app` is your Flask application. Enjoy.
