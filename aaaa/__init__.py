#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import ast
import astor
from argparse import ArgumentParser

modules = set()
excluded = set(dir(__builtins__))
names = {}
start = 8

def translate(name):
    if name is None or (name.startswith('__') and name.endswith('__')):
        return name
    if name not in names:
        names[name] = new_name()
        print(f'{name} -> {names[name]}')
    return names[name]


def new_name():
    return f'{len(names)+start:b}'.replace('0', 'A').replace('1', 'А')


class Visitor(ast.NodeTransformer):

    def visit_Name(self, node):
        if node.id in modules or node.id in excluded:
            return node
        node.id = translate(node.id)
        return node

    def visit_Attribute(self, node):
        super().generic_visit(node)
        if isinstance(node.value, ast.Name) and node.value.id in modules:
            return node
        node.attr = translate(node.attr)
        return node

    def visit_Import(self, node):
        aliases = []
        for alias in node.names:
            asname = translate(alias.asname or alias.name)
            modules.add(asname)
            aliases.append(ast.alias(alias.name, asname))
        node.names = aliases
        return node

    def visit_ImportFrom(self, node):
        aliases = []
        for alias in node.names:
            asname = translate(alias.asname or alias.name)
            modules.add(asname)
            aliases.append(ast.alias(alias.name, asname))
        node.names = aliases
        return node

    @staticmethod
    def _translate_args(args):
        for arg in args.args:
            arg.arg = translate(arg.arg)
        for arg in args.kwonlyargs:
            arg.arg = translate(arg.arg)
        if args.vararg:
            args.vararg.arg = translate(args.vararg.arg)
        if args.kwarg:
            args.kwarg.arg = translate(args.kwarg.arg)

    def visit_FunctionDef(self, node):
        super().generic_visit(node)
        node.name = translate(node.name)
        self._translate_args(node.args)
        return node

    def visit_AsyncFunctionDef(self, node):
        super().generic_visit(node)
        node.name = translate(node.name)
        self._translate_args(node.args)
        return node

    def visit_Lambda(self, node):
        super().generic_visit(node)
        self._translate_args(node.args)
        return node

    def visit_ClassDef(self, node):
        super().generic_visit(node)
        node.name = translate(node.name)
        return node

    def visit_ExceptHandler(self, node):
        super().generic_visit(node)
        node.name = translate(node.name)
        return node

    def generic_visit(self, node):
        return super().generic_visit(node)


def main(args):
    with open(args.filepath) as f:
        source = f.read()
    old_root = ast.parse(source)
    new_root = Visitor().visit(old_root)
    result = astor.to_source(new_root)
    if args.inplace:
        with open(args.filepath, 'w') as f:
            f.write(result)
    else:
        print('='*10)
        print(result)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filepath', metavar='source.py')
    parser.add_argument('--minlen', metavar='n', default=4, type=int)
    parser.add_argument('--inplace', action='store_true')
    args = parser.parse_args()
    start = 2 ** (args.minlen - 1)
    main(args)
