# coding=utf-8

"""
    jinja_atoms.ext
    ~~~~~~~~~~~~~~~

    Implements the Jinja Atoms extension itself.

    :copyright: 2013 by Roman Semirook.
    :license: BSD, see LICENSE for more details.
"""

import re
import hashlib

from jinja2 import Template, nodes
from jinja2.utils import import_string
from jinja2.ext import Extension
from jinja2.exceptions import TemplateSyntaxError


class JinjaAtomsExtension(Extension):

    tags = set(['atom'])

    ATOMS_NS_RE = re.compile(
        r'\{\%\s*use\s+atoms\s*\'?(?P<tmpl>[^\s]+)\'?\s*as\s*\'?(?P<context>\w+)\'?\s*\%\}',
    )

    def preprocess(self, source, name, filename=None):
        namespaces = re.findall(self.ATOMS_NS_RE, source)
        atoms_ns_map = dict(map(lambda x: (x[1], x[0]), namespaces))
        source = re.sub(self.ATOMS_NS_RE, '', source)
        self.environment.globals.setdefault('atoms_ns', {}).update(atoms_ns_map)

        return source

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        atom_ns = None
        atom_path = []
        atom_args = []
        atom_kwargs = []

        atom_ns = parser.stream.expect('name').value
        parser.stream.expect('colon')

        while parser.stream.current.type not in ['lparen', 'eof']:
            atom_path.append(parser.stream.current.value)
            next(parser.stream)

        parser.stream.expect('lparen')

        while parser.stream.current.type not in ['rparen', 'eof']:
            if atom_args or atom_kwargs:
                parser.stream.expect('comma')

            arg = parser.stream.current
            if arg.type in ['integer', 'string']:
                atom_args.append(
                    nodes.Const(arg.value)
                )
                next(parser.stream)
            elif arg.type in ['lbracket', 'lbrace']:
                arg_expr = parser.parse_expression()
                atom_args.append(arg_expr)
            elif arg.type == 'name':
                arg_name = nodes.Name(arg.value, 'load')
                next(parser.stream)
                if parser.stream.current.type == 'assign':
                    next(parser.stream)
                    arg_expr = parser.parse_expression()
                    atom_kwargs.append(nodes.Keyword(arg.value, arg_expr))
                else:
                    atom_args.append(arg_name)
            else:
                next(parser.stream)

        parser.stream.expect('rparen')

        env_atoms_ns = self.environment.globals.get('atoms_ns')
        env_atom_host = env_atoms_ns and env_atoms_ns.get(atom_ns)
        if not env_atom_host:
            raise TemplateSyntaxError('"%s" atom namespace not found' % atom_ns, lineno)

        full_atom_path = str('.'.join([env_atom_host, ''.join(atom_path)]))
        env_atom_name = 'loaded_atom_%s' % hashlib.md5(full_atom_path).hexdigest()
        if env_atom_name not in self.environment.globals:
            try:
                imported_atom = import_string(full_atom_path)
            except AttributeError:
                raise ImportError('Atom "%s" not found' % full_atom_path)
            self.environment.globals.update({
                env_atom_name: imported_atom
            })

        atom_func = nodes.Name(env_atom_name, 'load')
        node = nodes.Call(atom_func, atom_args, atom_kwargs, None, None)
        node = nodes.Output([node])
        node.set_lineno(lineno)

        return node
