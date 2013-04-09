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

If you are using Jinja in non-Flask project, just add the extension into your Jinja environment definition:

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

Jinja was inspired by [Django's templates](https://docs.djangoproject.com/en/dev/topics/templates/) 
and if you had a deal with Django you'll feel yourself at home (or already do). Jinja by all means has a rich set of 
filters, helpers, etc. but there is one great feature that's totally absent. 
I mean [**inclusion tags**](https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#inclusion-tags)
in terms of Django templates.

There are web-developers that do not know about them at all or simply believe it can really slow down Jinja. 
Yes, it could be true with some kind of dirty engine hacks. But. Jinja is extendable by design. 
It's completely legal to write parser extensions and use them. So... you want to render templates 
inside of another templates with some custom context? it’s possible and it’s already done in **Jinja Atoms** for you.


## I don’t understand what you talking about!

If you had no practice with Django and Django template engine itself, you possibly do not understand the use case.
Think about some typical problems. How would you implement a sidebar that has to change it’s behaviour and appearence 
somehow by the context it’s shown in with standard Jinja's built-ins? Or site menu, stored like MPTT-structure 
somewhere in your Postgres or Redis DB? Or a standard set of action buttons that are sensitive to some 
kinds of entities? Yes, you can implement all of that stuff without any extension. But the main idea of Jinja Atoms 
is maintanability. And DRY. And ease to use. Describe them once and include pre-rendered complex dynamic 
content everywhere you need with one simple statement.


## Atoms declaration

First of all, prepare some package inside your project for the atoms set.

```
/my_atoms/
  __init__.py
  oxygen.py
  ...
  /html/
    one_atom_template.html
    another_atom_template.html
    ...
app.py
settings.py
...
```

`oxygen.py` is an example of some module that encapsulates atoms, it's not necessary. 
You can have project-wide atoms in the project's root or create some blueprints-related sets of them (in terms of Flask).
As you wish.

The *atom* is just a function that returns a string back into the calling template
(rendered Jinja template is a unicode string, actually). And...

```python
def simple_echo():
  return 'Hello'
```
...is completely legal atom.


### `@atom` decorator

It's not so simple to render Jinja template. You have to create Jinja environment with some 
template loader, prepare template context and, somehow, be able to work with parent's template 
filters and extensions in the atom's template. The `@atom` decorator do this work for you.

```python
from jinja_atoms.decorators import atom

@atom('package.path', 'atom_template.html')
def simple_atom(my_arg, my_kwarg=None):
  return {'arg': my_arg, 'kwarg': my_kwarg}
```

Note some details here:
- the first decorator argument is a path to some package that contains `html` or `templates` 
directory with atoms templates;
- the second argument is the atom's template name;
- the atom function itself is usual python function, with any number of arguments;
- the function returns regular python dictionary, it's our custom atom's context;
- implicit parent's environment object which is used to create atom 
[overlay](http://jinja.pocoo.org/docs/api/#jinja2.Environment.overlay) environment 
for rendering and template loading is not accessible from the atom function. It is so to prevent 
any possible side effects in the main environment. You don't want waste your time by catching 
very strange bugs, trust me.

If you want to modify the template loader somehow, you can write your own decorator (not joke)
or you can pass custom environment with custom loader as decorator argument `env` like this:

```python
from jinja2 import Environment, PackageLoader

custom_env = Environment(
  loader=PackageLoader('yet.another.package', 'custom_html_path')
)

@atom(jinja_template='atom_template.html', env=custom_env)
def simple_atom(my_arg, my_kwarg=None):
  return {'arg': my_arg, 'kwarg': my_kwarg}
```

Or... send me pull request with argumentation, implementation and tests :)


## Atoms usage

Imagine we have some set of atoms in our oxygen module. And we want to use them (sure, we want).
To call an atom we have to do two things - specify its location and call it from this location.
The *location* is a **namespace** and has special syntax, provided by Jinja Atoms extension.
It is mostly like usual python's import statement.

```jinja
{% use atoms my_atoms as common_atoms %}
{% use atoms my_atoms.oxygen as oxygen_atoms %}
```
Note, these two strings are equal. I'm sure you understand it, there is nothing special here.

The atom call statement is a bit more unusual:
- the namespace alias and relative function path are separated by the colon;
- the function call brackets are always explicit (hello, Django, you have to do the same);
- function arguments are optional, of course.

```jinja
{% atom common_atoms:oxygen.simple_atom(42) %}
```
and
```jinja
{% atom oxygen_atoms:simple_atom(42) %}
```
calls are equal.

*We've defined the `simple_atom` function earlier, with one mandatory positional argument, remember? 
So, we have to pass some object like 42 :)*

For example, the `atom_template.html` is something like this:

```jinja
{% if kwarg %}
  <p>The kwarg value is "{{ kwarg }}".</p>
{% endif %}
<p>The arg value is {{ arg }}.</p>
```

And the main template is like this:

```jinja
{% use atoms my_atoms.oxygen as oxygen_atoms %}

<p>Very simple example. But you can feel the power of idea.</p>
{% atom oxygen_atoms:simple_atom(42, "I am kwarg") %}
```

The `simple_atom` call will render `atom_template.html` with context variables `arg=42` and `kwarg=None`.
A bit of magic and we have the final result:

```html
<p>Very simple example. But you can feel the power of idea.</p>
<p>The kwarg value is "I am kwarg".</p>
<p>The arg value is 42.</p>
```

Now, it's time for sad news. There are some restrictions here:
- you can't pass sets (Jinja parser bug) as an arguments;
- you can't pass tuples as an arguments (but there is workaround for that, I'll show you).

```jinja
{% atom oxygen_atoms:simple_atom({1,2,3}) %}  ## doesn't work
{% atom oxygen_atoms:simple_atom((1,2,3)) %}  ## doesn't work

{% set my_tuple_arg=(1,2,3) %}
{% atom oxygen_atoms:simple_atom(my_tuple_arg) %}  ## works

{% set my_tuple_arg={1,2,3} %}  ## doesn't work, Jinja is broken here
{% atom oxygen_atoms:simple_atom(my_tuple_arg) %}
```

Named objects of any type from the template context, integers, lists, dicts as positional or named arguments - 
you're welcome.

```jinja
{% atom oxygen_atoms:simple_atom(42) %}
{% atom oxygen_atoms:simple_atom("I am potato") %}
{% atom oxygen_atoms:simple_atom([1,2,3]) %}
{% atom oxygen_atoms:simple_atom(some_object_prepared_in_view) %}
{% atom oxygen_atoms:simple_atom(42, my_kwarg={'a': 1, 'b': 2}) %}
```
are correct statements.

Start to use it and you'll love it.

## Roadmap for the 0.2 version
- Real-world examples of the `atoms` usage
- More customizable `@atom` decorator
- Independent cache system (maybe)
- More tests (you never have many of them)
