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

## So, what's the problem?
[Jinja](http://jinja.pocoo.org) is fast, featurable and one of the most used template engines for Python 
that covers almost all possible use cases. Hundreds of developers all over the world use it in there web projects. 
And they love it.

Jinja was inspired by [Django's templates](https://docs.djangoproject.com/en/dev/topics/templates/) 
and if you had a deal with Django you'll feel yourself at home (or already do). Jinja by all means has a rich set of 
filters, helpers, etc. but there is one great feature that's totally absent. 
I mean [**inclusion tags**](https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#inclusion-tags)
in terms of Django templates.

There are web-developers that do not know about them at all or simply believe it can really slow down Jinja. 
Yes, it could be true with some kind of dirty engine hacks. But. Jinja is extendable by design. 
It's completely legal to write parser extensions and use them. So... render templates inside of another templates 
with some custom context? it’s possible and it’s already done in **Jinja Atoms** for you.

## I don’t understand what you talking about!
If you had no practice with Django and Django template engine itself, you possibly do not understand the use case.
Think about some typical problems. How would you implement a sidebar that has to change it’s behaviour and appearence 
somehow by the context it’s shown in with standard Jinja's built-ins? Or site menu, stored like MPTT-structure 
somewhere in your Postgres or Redis DB? Or a standard set of action buttons that are sensitive to some 
kinds of entities? Yes, you can implement all of that stuff without any extension by using Jinja 
[macroses](http://jinja.pocoo.org/docs/templates/#macros) 
and Flask [context processors](http://flask.pocoo.org/docs/templating/#context-processors) (it's not Jinja feature).

But the main idea of Jinja Atoms is maintanability. And DRY. And ease to use. You can describe them once 
and include pre-rendered complex dynamic content everywhere you need with one simple statement.
