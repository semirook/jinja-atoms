# coding=utf-8

"""
    jinja_atoms.decotators
    ~~~~~~~~~~~~~~~~~~~~~~

    Implements Jinja Atoms decorators
    for atoms marking and managing.

    :copyright: 2013 by Roman Semirook.
    :license: BSD, see LICENSE for more details.
"""

from jinja2 import Environment, environmentfunction
from jinja2 import PackageLoader, ChoiceLoader


def atom(package_path=None, jinja_template=None, env=None):
    if env is not None:
        assert isinstance(env, Environment)
    else:
        assert package_path is not None, 'Atoms package is not defined'
    assert jinja_template is not None, 'Template name is not defined'
    def wrapper(func):
        @environmentfunction
        def atom_args(*args, **kwargs):
            linked_env, args = args[0], args[1:]
            overlay_env = env or linked_env.overlay(
                loader=ChoiceLoader([
                    PackageLoader(package_path, 'html'),
                    PackageLoader(package_path, 'templates')
                ]),
            )
            template = overlay_env.get_template(jinja_template)
            template_context = func(*args, **kwargs)
            return template.render(template_context)
        return atom_args
    return wrapper
