# coding=utf-8

"""
    jinja_atoms.decotators
    ~~~~~~~~~~~~~~~~~~~~~~

    Implements Jinja Atoms decorators
    for atoms marking and managing.

    :copyright: 2013 by Roman Semirook.
    :license: BSD, see LICENSE for more details.
"""

from functools import wraps

from jinja2 import Environment, PackageLoader, ChoiceLoader

from .ext import JinjaAtomsExtension


class AtomFactory():

    def __init__(self):
        self.atom_envs = {}

    def get_env(self, atom_package=None):
        if atom_package and atom_package in self.atom_envs:
            return self.atom_envs[atom_package]

        new_env = Environment(
            loader=ChoiceLoader([
                PackageLoader(atom_package, 'html'),
                PackageLoader(atom_package, 'templates')
            ]),
            extensions=[JinjaAtomsExtension]
        )
        self.atom_envs[atom_package] = new_env

        return new_env

    def build(self):
        def atom(package_path, jinja_path):
            env = self.get_env(package_path)
            template = env.get_template(jinja_path)
            def wrapper(func):
                @wraps(func)
                def atom_args(*args, **kwargs):
                    template_context = func(*args, **kwargs)
                    return template.render(template_context)
                return atom_args
            return wrapper
        return atom


atom_factory = AtomFactory()
atom = atom_factory.build()
