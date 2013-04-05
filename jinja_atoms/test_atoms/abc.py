# coding=utf-8
from jinja2 import Environment, PackageLoader

from ..decorators import atom


def simple_echo():
    return 'ECHO'


@atom('jinja_atoms.test_atoms', 'simple_block.html')
def simple_block():
    return {'greeting': 'Hello, Jinja!'}


@atom('jinja_atoms.test_atoms', 'block_with_args.html')
def block_with_args(arg_one, arg_two):
    return {
        'arg_one': arg_one,
        'arg_two': arg_two,
    }


@atom('jinja_atoms.test_atoms', 'block_with_kwargs.html')
def block_with_kwargs(kwarg_one=None, kwarg_two=None):
    return {
        'kwarg_one': kwarg_one,
        'kwarg_two': kwarg_two,
    }


@atom('jinja_atoms.test_atoms', 'complex_block.html')
def complex_block(arg, kwarg=None, *args, **kwargs):
    return {
        'arg': arg,
        'kwarg': kwarg,
        'args': args,
        'kwargs': kwargs,
    }


custom_env = Environment(
    loader=PackageLoader('jinja_atoms.test_atoms', 'custom_html')
)


@atom('jinja_atoms.test_atoms', 'simple_block.html', env=custom_env)
def custom_env_simple_block():
    return {'greeting': 'hello!'}
