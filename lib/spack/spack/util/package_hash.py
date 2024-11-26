# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import ast

import spack.directives_meta
import spack.error
import spack.fetch_strategy
import spack.package_base
import spack.repo
import spack.spec
import spack.util.hash
from spack.util.unparse import unparse


class RemoveDocstrings(ast.NodeTransformer):
    """Transformer that removes docstrings from a Python AST.

    This removes *all* strings that aren't on the RHS of an assignment statement from
    the body of functions, classes, and modules -- even if they're not directly after
    the declaration.

    """

    def remove_docstring(self, node):
        def unused_string(node):
            """Criteria for unassigned body strings."""
            return isinstance(node, ast.Expr) and isinstance(node.value, ast.Str)

        if node.body:
            node.body = [child for child in node.body if not unused_string(child)]

        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        return self.remove_docstring(node)

    def visit_ClassDef(self, node):
        return self.remove_docstring(node)

    def visit_Module(self, node):
        return self.remove_docstring(node)


class RemoveDirectives(ast.NodeTransformer):
    """Remove Spack directives from a package AST.

    This removes Spack directives (e.g., ``depends_on``, ``conflicts``, etc.) and
    metadata attributes (e.g., ``tags``, ``homepage``, ``url``) in a top-level class
    definition within a ``package.py``, but it does not modify nested classes or
    functions.

    If removing directives causes a ``for``, ``with``, or ``while`` statement to have an
    empty body, we remove the entire statement. Similarly, If removing directives causes
    an ``if`` statement to have an empty body or ``else`` block, we'll remove the block
    (or replace the body with ``pass`` if there is an ``else`` block but no body).

    """

    def __init__(self, spec):
        # list of URL attributes and metadata attributes
        # these will be removed from packages.
        self.metadata_attrs = [s.url_attr for s in spack.fetch_strategy.all_strategies]
        self.metadata_attrs += spack.package_base.PackageBase.metadata_attrs

        self.spec = spec
        self.in_classdef = False  # used to avoid nested classdefs

    def visit_Expr(self, node):
        # Directives are represented in the AST as named function call expressions (as
        # opposed to function calls through a variable callback). We remove them.
        #
        # Note that changes to directives (e.g., a preferred version change or a hash
        # chnage on an archive) are already represented in the spec *outside* the
        # package hash.
        return (
            None
            if (
                node.value
                and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
                and node.value.func.id in spack.directives_meta.directive_names
            )
            else node
        )

    def visit_Assign(self, node):
        # Remove assignments to metadata attributes, b/c they don't affect the build.
        return (
            None
            if (
                node.targets
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id in self.metadata_attrs
            )
            else node
        )

    def visit_With(self, node):
        self.generic_visit(node)  # visit children
        return node if node.body else None  # remove with statement if it has no body

    def visit_For(self, node):
        self.generic_visit(node)  # visit children
        return node if node.body else None  # remove loop if it has no body

    def visit_While(self, node):
        self.generic_visit(node)  # visit children
        return node if node.body else None  # remove loop if it has no body

    def visit_If(self, node):
        self.generic_visit(node)

        # an empty orelse is ignored by unparsing, but an empty body with a full orelse
        # ends up unparsing as a syntax error, so we replace the empty body into `pass`.
        if not node.body:
            if node.orelse:
                node.body = [ast.Pass()]
            else:
                return None

        # if the node has a body, it's valid python code with or without an orelse
        return node

    def visit_FunctionDef(self, node):
        # do not descend into function definitions
        return node

    def visit_ClassDef(self, node):
        # packages are always top-level, and we do not descend
        # into nested class defs and their attributes
        if self.in_classdef:
            return node

        # guard against recrusive class definitions
        self.in_classdef = True
        self.generic_visit(node)
        self.in_classdef = False

        # replace class definition with `pass` if it's empty (e.g., packages that only
        # have directives b/c they subclass a build system class)
        if not node.body:
            node.body = [ast.Pass()]

        return node


class TagMultiMethods(ast.NodeVisitor):
    """Tag @when-decorated methods in a package AST."""

    def __init__(self, spec):
        self.spec = spec
        # map from function name to (implementation, condition_list) tuples
        self.methods = {}

    def visit_FunctionDef(self, func):
        conditions = []

        for dec in func.decorator_list:
            if isinstance(dec, ast.Call) and dec.func.id == "when":
                try:
                    # evaluate spec condition for any when's
                    cond = dec.args[0].s

                    # Boolean literals come through like this
                    if isinstance(cond, bool):
                        conditions.append(cond)
                        continue

                    # otherwise try to make a spec
                    try:
                        cond_spec = spack.spec.Spec(cond)
                    except Exception:
                        # Spec parsing failed -- we don't know what this is.
                        conditions.append(None)
                    else:
                        # Check statically whether spec satisfies the condition
                        conditions.append(self.spec.satisfies(cond_spec))

                except AttributeError:
                    # In this case the condition for the 'when' decorator is
                    # not a string literal (for example it may be a Python
                    # variable name). We append None because we don't know
                    # whether the constraint applies or not, and it should be included
                    # unless some other constraint is False.
                    conditions.append(None)

        # anything defined without conditions will overwrite prior definitions
        if not conditions:
            self.methods[func.name] = []

        # add all discovered conditions on this node to the node list
        impl_conditions = self.methods.setdefault(func.name, [])
        impl_conditions.append((func, conditions))

        # don't modify the AST -- return the untouched function node
        return func


class ResolveMultiMethods(ast.NodeTransformer):
    """Remove multi-methods when we know statically that they won't be used.

    Say we have multi-methods like this::

        class SomePackage:
            def foo(self): print("implementation 1")

            @when("@1.0")
            def foo(self): print("implementation 2")

            @when("@2.0")
            @when(sys.platform == "darwin")
            def foo(self): print("implementation 3")

            @when("@3.0")
            def foo(self): print("implementation 4")

    The multimethod that will be chosen at runtime depends on the package spec and on
    whether we're on the darwin platform *at build time* (the darwin condition for
    implementation 3 is dynamic). We know the package spec statically; we don't know
    statically what the runtime environment will be. We need to include things that can
    possibly affect package behavior in the package hash, and we want to exclude things
    when we know that they will not affect package behavior.

    If we're at version 4.0, we know that implementation 1 will win, because some @when
    for 2, 3, and 4 will be `False`. We should only include implementation 1.

    If we're at version 1.0, we know that implementation 2 will win, because it
    overrides implementation 1.  We should only include implementation 2.

    If we're at version 3.0, we know that implementation 4 will win, because it
    overrides implementation 1 (the default), and some @when on all others will be
    False.

    If we're at version 2.0, it's a bit more complicated. We know we can remove
    implementations 2 and 4, because their @when's will never be satisfied. But, the
    choice between implementations 1 and 3 will happen at runtime (this is a bad example
    because the spec itself has platform information, and we should prefer to use that,
    but we allow arbitrary boolean expressions in @when's, so this example suffices).
    For this case, we end up needing to include *both* implementation 1 and 3 in the
    package hash, because either could be chosen.

    """

    def __init__(self, methods):
        self.methods = methods

    def resolve(self, impl_conditions):
        """Given list of nodes and conditions, figure out which node will be chosen."""
        result = []
        default = None
        for impl, conditions in impl_conditions:
            # if there's a default implementation with no conditions, remember that.
            if not conditions:
                default = impl
                result.append(default)
                continue

            # any known-false @when means the method won't be used
            if any(c is False for c in conditions):
                continue

            # anything with all known-true conditions will be picked if it's first
            if all(c is True for c in conditions):
                if result and result[0] is default:
                    return [impl]  # we know the first MM will always win
                # if anything dynamic comes before it we don't know if it'll win,
                # so just let this result get appended

            # anything else has to be determined dynamically, so add it to a list
            result.append(impl)

        # if nothing was picked, the last definition wins.
        return result

    def visit_FunctionDef(self, func):
        # if the function def wasn't visited on the first traversal there is a problem
        assert func.name in self.methods, "Inconsistent package traversal!"

        # if the function is a multimethod, need to resolve it statically
        impl_conditions = self.methods[func.name]

        resolutions = self.resolve(impl_conditions)
        if not any(r is func for r in resolutions):
            # multimethod did not resolve to this function; remove it
            return None

        # if we get here, this function is a possible resolution for a multi-method.
        # it might be the only one, or there might be several that have to be evaluated
        # dynamcially.  Either way, we include the function.

        # strip the when decorators (preserve the rest)
        func.decorator_list = [
            dec
            for dec in func.decorator_list
            if not (isinstance(dec, ast.Call) and dec.func.id == "when")
        ]
        return func


def canonical_source(spec, filter_multimethods=True, source=None):
    """Get canonical source for a spec's package.py by unparsing its AST.

    Arguments:
        filter_multimethods (bool): By default, filter multimethods out of the
            AST if they are known statically to be unused. Supply False to disable.
        source (str): Optionally provide a string to read python code from.
    """
    return unparse(package_ast(spec, filter_multimethods, source=source), py_ver_consistent=True)


def package_hash(spec, source=None):
    """Get a hash of a package's canonical source code.

    This function is used to determine whether a spec needs a rebuild when a
    package's source code changes.

    Arguments:
        source (str): Optionally provide a string to read python code from.

    """
    source = canonical_source(spec, filter_multimethods=True, source=source)
    return spack.util.hash.b32_hash(source)


def package_ast(spec, filter_multimethods=True, source=None):
    """Get the AST for the ``package.py`` file corresponding to ``spec``.

    Arguments:
        filter_multimethods (bool): By default, filter multimethods out of the
            AST if they are known statically to be unused. Supply False to disable.
        source (str): Optionally provide a string to read python code from.
    """
    spec = spack.spec.Spec(spec)

    if source is None:
        filename = spack.repo.PATH.filename_for_package_name(spec.name)
        with open(filename) as f:
            source = f.read()

    # create an AST
    root = ast.parse(source)

    # remove docstrings, comments, and directives from the package AST
    root = RemoveDocstrings().visit(root)
    root = RemoveDirectives(spec).visit(root)

    if filter_multimethods:
        # visit nodes and build up a dictionary of methods (no need to assign)
        tagger = TagMultiMethods(spec)
        tagger.visit(root)

        # transform AST using tagged methods
        root = ResolveMultiMethods(tagger.methods).visit(root)

    return root


class PackageHashError(spack.error.SpackError):
    """Raised for all errors encountered during package hashing."""
