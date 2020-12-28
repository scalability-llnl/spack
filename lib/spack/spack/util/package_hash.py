# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import ast
import hashlib

import spack.repo
import spack.package_base
import spack.directives
import spack.error
import spack.spec
import spack.util.naming


class RemoveDocstrings(ast.NodeTransformer):
    """Transformer that removes docstrings from a Python AST."""
    def remove_docstring(self, node):
        if node.body:
            if isinstance(node.body[0], ast.Expr) and \
               isinstance(node.body[0].value, ast.Str):
                node.body.pop(0)

        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):  # noqa
        return self.remove_docstring(node)

    def visit_ClassDef(self, node):  # noqa
        return self.remove_docstring(node)

    def visit_Module(self, node):  # noqa
        return self.remove_docstring(node)


class RemoveDirectives(ast.NodeTransformer):
    """Remove Spack directives from a package AST."""
    def __init__(self, spec):
        self.spec = spec

    def is_directive(self, node):
        """Check to determine if the node is a valid directive

        Directives are assumed to be represented in the AST as a named function
        call expression.  This means that they will NOT be represented by a
        named function call within a function call expression (e.g., as
        callbacks are sometimes represented).

        Args:
            node (AST): the AST node being checked

        Returns:
            (bool): ``True`` if the node represents a known directive,
                ``False`` otherwise
        """
        return (isinstance(node, ast.Expr) and
                node.value and isinstance(node.value, ast.Call) and
                isinstance(node.value.func, ast.Name) and
                node.value.func.id in spack.directives.__all__)

    def is_spack_attr(self, node):
        return (isinstance(node, ast.Assign) and
                node.targets and isinstance(node.targets[0], ast.Name) and
                node.targets[0].id in spack.package_base.Package.metadata_attrs)

    def visit_ClassDef(self, node):  # noqa
        if node.name == spack.util.naming.mod_to_class(self.spec.name):
            node.body = [
                c for c in node.body
                if (not self.is_directive(c) and not self.is_spack_attr(c))]
        return node


class TagMultiMethods(ast.NodeVisitor):
    """Tag @when-decorated methods in a spec."""
    def __init__(self, spec):
        self.spec = spec
        self.methods = {}

    def visit_FunctionDef(self, node):  # noqa
        nodes = self.methods.setdefault(node.name, [])
        if node.decorator_list:
            dec = node.decorator_list[0]
            if isinstance(dec, ast.Call) and dec.func.id == 'when':
                try:
                    cond = dec.args[0].s
                    nodes.append(
                        (node, self.spec.satisfies(cond, strict=True)))
                except AttributeError:
                    # In this case the condition for the 'when' decorator is
                    # not a string literal (for example it may be a Python
                    # variable name). Therefore the function is added
                    # unconditionally since we don't know whether the
                    # constraint applies or not.
                    nodes.append((node, None))
        else:
            nodes.append((node, None))


class ResolveMultiMethods(ast.NodeTransformer):
    """Remove methods which do not exist if their @when is not satisfied."""
    def __init__(self, methods):
        self.methods = methods

    def resolve(self, node):
        if node.name not in self.methods:
            raise PackageHashError(
                "Future traversal visited new node: %s" % node.name)

        result = None
        for n, cond in self.methods[node.name]:
            if cond:
                return n
            if cond is None:
                result = n
        return result

    def visit_FunctionDef(self, node):  # noqa
        if self.resolve(node) is node:
            node.decorator_list = []
            return node
        return None


def package_content(spec):
    return ast.dump(package_ast(spec))


def package_hash(spec, content=None):
    if content is None:
        content = package_content(spec)
    return hashlib.sha256(content.encode('utf-8')).digest().lower()


def package_ast(spec):
    spec = spack.spec.Spec(spec)

    filename = spack.repo.path.filename_for_package_name(spec.name)
    with open(filename) as f:
        text = f.read()
        root = ast.parse(text)

    root = RemoveDocstrings().visit(root)

    RemoveDirectives(spec).visit(root)

    fmm = TagMultiMethods(spec)
    fmm.visit(root)

    root = ResolveMultiMethods(fmm.methods).visit(root)
    return root


class PackageHashError(spack.error.SpackError):
    """Raised for all errors encountered during package hashing."""
