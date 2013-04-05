# coding=utf-8

"""
    jinja_atoms.decotators
    ~~~~~~~~~~~~~~~~~~~~~~

    Implements Jinja Atoms decorators
    for atoms marking and managing.

    :copyright: 2013 by Roman Semirook.
    :license: BSD, see LICENSE for more details.
"""

from jinja2 import environmentfunction
from jinja2 import PackageLoader, ChoiceLoader


def atom(package_path, jinja_path):
    def wrapper(func):
        @environmentfunction
        def atom_args(*args, **kwargs):
            linked_env, args = args[0], args[1:]
            overlay_env = linked_env.overlay(
                loader=ChoiceLoader([
                    PackageLoader(package_path, 'html'),
                    PackageLoader(package_path, 'templates')
                ]),
            )
            template = overlay_env.get_template(jinja_path)
            template_context = func(*args, **kwargs)
            return template.render(template_context)
        return atom_args
    return wrapper
