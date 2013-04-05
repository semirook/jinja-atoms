# coding=utf-8
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from jinja2 import Environment
from jinja2.exceptions import TemplateSyntaxError

from .ext import JinjaAtomsExtension


class AtomsTestCase(unittest.TestCase):

    def setUp(self):
        self.jinja_env = Environment(
            extensions=[JinjaAtomsExtension]
        )


class ValidAtomsTestCase(AtomsTestCase):

    def test_echo(self):
        result = self.jinja_env.from_string(
            '{% use atoms jinja_atoms.test_atoms as ta %}'
            '{% atom ta:simple_echo() %}'
        ).render()
        self.assertEqual(result, 'ECHO')

    def test_simple_block(self):
        result = self.jinja_env.from_string(
            '{% use atoms jinja_atoms.test_atoms as ta %}'
            '{% atom ta:abc.simple_block() %}'
        ).render()
        self.assertEqual(result, '<p>Hello, Jinja!</p>')

    def test_block_with_args(self):
        result = self.jinja_env.from_string(
            '{% use atoms jinja_atoms.test_atoms as ta %}'
            '{% atom ta:block_with_args(38, "parrots") %}'
        ).render()
        self.assertEqual(result, '<p>There is 38 parrots</p>')

    def test_block_with_kwargs(self):
        result = self.jinja_env.from_string(
            '{% use atoms jinja_atoms.test_atoms as ta %}'
            '{% atom ta:abc.block_with_kwargs(kwarg_one=42, kwarg_two=43) %}'
            '{% atom ta:abc.block_with_kwargs(kwarg_two=43, kwarg_one=42) %}'
        ).render()
        self.assertEqual(
            result,
            '<p>There is 42 or 43 parrots</p><p>There is 42 or 43 parrots</p>'
        )

    def test_multiple_namespaces(self):
        result = self.jinja_env.from_string(
            '{% use atoms jinja_atoms.test_atoms as ta %}'
            '{% use atoms jinja_atoms.test_atoms as test_atoms %}'

            '{% atom ta:abc.block_with_kwargs(kwarg_one=42, kwarg_two=43) %}'
            '{% atom test_atoms:abc.block_with_kwargs(kwarg_two=43, kwarg_one=42) %}'
        ).render()
        self.assertEqual(
            result,
            '<p>There is 42 or 43 parrots</p><p>There is 42 or 43 parrots</p>'
        )

    def test_context_var(self):
        result = self.jinja_env.from_string(
            '{% use atoms jinja_atoms.test_atoms as ta %}'
            '{% set some_arg=42 %}'
            '{% set another_arg="parrots" %}'
            '{% atom ta:block_with_args(some_arg, another_arg) %}'
        ).render()
        self.assertEqual(result, '<p>There is 42 parrots</p>')

    def test_complex_args(self):
        result = self.jinja_env.from_string(
            '{% use atoms jinja_atoms.test_atoms as ta %}'
            '{% atom ta:abc.complex_block(38, 42, [1,2,3], days=31, months=12) %}'
        ).render()
        self.assertEqual(
            result, (
                '<p>We have 38 parrots</p><p>And 42 carrots</p>'
                '<p>And the list: [1, 2, 3]</p>'
                '<p>And the map:</p><p>Months: 12, Days: 31</p>'
            )
        )

    def test_custom_env_block(self):
        result = self.jinja_env.from_string(
            '{% use atoms jinja_atoms.test_atoms.abc as abc %}'
            '{% atom abc:custom_env_simple_block() %}'
        ).render()
        self.assertEqual(result, '<p>Custom env, hello!</p>')


class InvalidAtomsTestCase(AtomsTestCase):

    def test_invalid_namespace_call(self):
        result = lambda: self.jinja_env.from_string(
            '{% use atom jinja_atoms.test_atoms as ta %}'
        ).render()
        self.assertRaises(TemplateSyntaxError, result)

    def test_invalid_namespace_alias(self):
        result = lambda: self.jinja_env.from_string(
            '{% use atoms jinja_atoms.test_atoms ta %}'
        ).render()
        self.assertRaises(TemplateSyntaxError, result)

    def test_unclosed_namespace(self):
        result = lambda: self.jinja_env.from_string(
            '{% use atom jinja_atoms.test_atoms as ta'
        ).render()
        self.assertRaises(TemplateSyntaxError, result)

    def test_almost_closed_namespace(self):
        result = lambda: self.jinja_env.from_string(
            '{% use atom jinja_atoms.test_atoms as ta }'
        ).render()
        self.assertRaises(TemplateSyntaxError, result)

    def test_atom_without_defined_namespace(self):
        result = lambda: self.jinja_env.from_string(
            '{% atom ta:abc.simple_block() %}'
        ).render()
        self.assertRaises(TemplateSyntaxError, result)

    def test_invalid_atom_path(self):
        result = lambda: self.jinja_env.from_string(
            '{% use atoms jinja_atoms.test_atoms as ta %}'
            '{% atom ta:abc.simpleblock() %}'
        ).render()
        self.assertRaises(ImportError, result)

    def test_not_called_atom(self):
        result = lambda: self.jinja_env.from_string(
            '{% use atoms jinja_atoms.test_atoms as ta %}'
            '{% atom ta:abc.simple_block %}'
        ).render()
        self.assertRaises(TemplateSyntaxError, result)

    def test_not_closed_lparen(self):
        result = lambda: self.jinja_env.from_string(
            '{% use atoms jinja_atoms.test_atoms as ta %}'
            '{% atom ta:abc.simple_block( %}'
        ).render()
        self.assertRaises(TemplateSyntaxError, result)

    def test_not_closed_rparen(self):
        result = lambda: self.jinja_env.from_string(
            '{% use atoms jinja_atoms.test_atoms as ta %}'
            '{% atom ta:abc.simple_block) %}'
        ).render()
        self.assertRaises(TemplateSyntaxError, result)

    def test_invalid_atom_args(self):
        result = lambda: self.jinja_env.from_string(
            '{% use atoms jinja_atoms.test_atoms as ta %}'
            '{% atom ta:abc.block_with_args(42) %}'
        ).render()
        self.assertRaises(TypeError, result)

    def test_unclosed_atom(self):
        result = lambda: self.jinja_env.from_string(
            '{% use atoms jinja_atoms.test_atoms as ta %}'
            '{% atom ta:abc.simple_block'
        ).render()
        self.assertRaises(TemplateSyntaxError, result)

    def test_almost_closed_atom(self):
        result = lambda: self.jinja_env.from_string(
            '{% use atoms jinja_atoms.test_atoms as ta %}'
            '{% atom ta:abc.simple_block }'
        ).render()
        self.assertRaises(TemplateSyntaxError, result)
