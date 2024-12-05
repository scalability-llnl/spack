# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Parser for spec literals (see token.py for grammar)"""
import pathlib
import re
from typing import List, Optional

from llnl.util.tty import color

import spack.deptypes
import spack.error
import spack.spec
import spack.version
from spack.token import NAME, Token, TokenContext, TokenType, strip_quotes_and_unescape, tokenize

#: Regex with groups to use for splitting (optionally propagated) key-value pairs
SPLIT_KVP = re.compile(rf"^({NAME})(==?)(.*)$")


class SpecParser:
    """Parse text into specs"""

    __slots__ = "literal_str", "ctx"

    def __init__(self, literal_str: str):
        self.literal_str = literal_str
        self.ctx = TokenContext(filter(lambda x: x.kind != TokenType.WS, tokenize(literal_str)))

    def tokens(self) -> List[Token]:
        """Return the entire list of token from the initial text. White spaces are
        filtered out.
        """
        return list(filter(lambda x: x.kind != TokenType.WS, tokenize(self.literal_str)))

    def next_spec(
        self, initial_spec: Optional["spack.spec.Spec"] = None
    ) -> Optional["spack.spec.Spec"]:
        """Return the next spec parsed from text.

        Args:
            initial_spec: object where to parse the spec. If None a new one
                will be created.

        Return
            The spec that was parsed
        """
        if not self.ctx.next_token:
            return initial_spec

        def add_dependency(dep, **edge_properties):
            """wrapper around root_spec._add_dependency"""
            try:
                root_spec._add_dependency(dep, **edge_properties)
            except spack.error.SpecError as e:
                raise SpecParsingError(str(e), self.ctx.current_token, self.literal_str) from e

        initial_spec = initial_spec or spack.spec.Spec()
        root_spec = SpecNodeParser(self.ctx, self.literal_str).parse(initial_spec)
        while True:
            if self.ctx.accept(TokenType.START_EDGE_PROPERTIES):
                edge_properties = EdgeAttributeParser(self.ctx, self.literal_str).parse()
                edge_properties.setdefault("depflag", 0)
                edge_properties.setdefault("virtuals", ())
                dependency = self._parse_node(root_spec)
                add_dependency(dependency, **edge_properties)

            elif self.ctx.accept(TokenType.DEPENDENCY):
                dependency = self._parse_node(root_spec)
                add_dependency(dependency, depflag=0, virtuals=())

            else:
                break

        return root_spec

    def _parse_node(self, root_spec):
        dependency = SpecNodeParser(self.ctx, self.literal_str).parse()
        if dependency is None:
            msg = (
                "the dependency sigil and any optional edge attributes must be followed by a "
                "package name or a node attribute (version, variant, etc.)"
            )
            raise SpecParsingError(msg, self.ctx.current_token, self.literal_str)
        if root_spec.concrete:
            raise spack.spec.RedundantSpecError(root_spec, "^" + str(dependency))
        return dependency

    def all_specs(self) -> List["spack.spec.Spec"]:
        """Return all the specs that remain to be parsed"""
        return list(iter(self.next_spec, None))


class SpecNodeParser:
    """Parse a single spec node from a stream of tokens"""

    __slots__ = "ctx", "has_compiler", "has_version", "literal_str"

    def __init__(self, ctx, literal_str):
        self.ctx = ctx
        self.literal_str = literal_str
        self.has_compiler = False
        self.has_version = False

    def parse(
        self, initial_spec: Optional["spack.spec.Spec"] = None
    ) -> Optional["spack.spec.Spec"]:
        """Parse a single spec node from a stream of tokens

        Args:
            initial_spec: object to be constructed

        Return
            The object passed as argument
        """
        if not self.ctx.next_token or self.ctx.expect(TokenType.DEPENDENCY):
            return initial_spec

        if initial_spec is None:
            initial_spec = spack.spec.Spec()

        # If we start with a package name we have a named spec, we cannot
        # accept another package name afterwards in a node
        if self.ctx.accept(TokenType.UNQUALIFIED_PACKAGE_NAME):
            initial_spec.name = self.ctx.current_token.value

        elif self.ctx.accept(TokenType.FULLY_QUALIFIED_PACKAGE_NAME):
            parts = self.ctx.current_token.value.split(".")
            name = parts[-1]
            namespace = ".".join(parts[:-1])
            initial_spec.name = name
            initial_spec.namespace = namespace

        elif self.ctx.accept(TokenType.FILENAME):
            return FileParser(self.ctx).parse(initial_spec)

        def raise_parsing_error(string: str, cause: Optional[Exception] = None):
            """Raise a spec parsing error with token context."""
            raise SpecParsingError(string, self.ctx.current_token, self.literal_str) from cause

        def add_flag(name: str, value: str, propagate: bool):
            """Wrapper around ``Spec._add_flag()`` that adds parser context to errors raised."""
            try:
                initial_spec._add_flag(name, value, propagate)
            except Exception as e:
                raise_parsing_error(str(e), e)

        while True:
            if self.ctx.accept(TokenType.COMPILER):
                if self.has_compiler:
                    raise_parsing_error("Spec cannot have multiple compilers")

                compiler_name = self.ctx.current_token.value[1:]
                initial_spec.compiler = spack.spec.CompilerSpec(compiler_name.strip(), ":")
                self.has_compiler = True

            elif self.ctx.accept(TokenType.COMPILER_AND_VERSION):
                if self.has_compiler:
                    raise_parsing_error("Spec cannot have multiple compilers")

                compiler_name, compiler_version = self.ctx.current_token.value[1:].split("@")
                initial_spec.compiler = spack.spec.CompilerSpec(
                    compiler_name.strip(), compiler_version
                )
                self.has_compiler = True

            elif (
                self.ctx.accept(TokenType.VERSION_HASH_PAIR)
                or self.ctx.accept(TokenType.GIT_VERSION)
                or self.ctx.accept(TokenType.VERSION)
            ):
                if self.has_version:
                    raise_parsing_error("Spec cannot have multiple versions")

                initial_spec.versions = spack.version.VersionList(
                    [spack.version.from_string(self.ctx.current_token.value[1:])]
                )
                initial_spec.attach_git_version_lookup()
                self.has_version = True

            elif self.ctx.accept(TokenType.BOOL_VARIANT):
                variant_value = self.ctx.current_token.value[0] == "+"
                add_flag(self.ctx.current_token.value[1:].strip(), variant_value, propagate=False)

            elif self.ctx.accept(TokenType.PROPAGATED_BOOL_VARIANT):
                variant_value = self.ctx.current_token.value[0:2] == "++"
                add_flag(self.ctx.current_token.value[2:].strip(), variant_value, propagate=True)

            elif self.ctx.accept(TokenType.KEY_VALUE_PAIR):
                match = SPLIT_KVP.match(self.ctx.current_token.value)
                assert match, "SPLIT_KVP and KEY_VALUE_PAIR do not agree."

                name, _, value = match.groups()
                add_flag(name, strip_quotes_and_unescape(value), propagate=False)

            elif self.ctx.accept(TokenType.PROPAGATED_KEY_VALUE_PAIR):
                match = SPLIT_KVP.match(self.ctx.current_token.value)
                assert match, "SPLIT_KVP and PROPAGATED_KEY_VALUE_PAIR do not agree."

                name, _, value = match.groups()
                add_flag(name, strip_quotes_and_unescape(value), propagate=True)

            elif self.ctx.expect(TokenType.DAG_HASH):
                if initial_spec.abstract_hash:
                    break
                self.ctx.accept(TokenType.DAG_HASH)
                initial_spec.abstract_hash = self.ctx.current_token.value[1:]

            else:
                break

        return initial_spec


class FileParser:
    """Parse a single spec from a JSON or YAML file"""

    __slots__ = ("ctx",)

    def __init__(self, ctx):
        self.ctx = ctx

    def parse(self, initial_spec: "spack.spec.Spec") -> "spack.spec.Spec":
        """Parse a spec tree from a specfile.

        Args:
            initial_spec: object where to parse the spec

        Return
            The initial_spec passed as argument, once constructed
        """
        file = pathlib.Path(self.ctx.current_token.value)

        if not file.exists():
            raise spack.spec.NoSuchSpecFileError(f"No such spec file: '{file}'")

        with file.open("r", encoding="utf-8") as stream:
            if str(file).endswith(".json"):
                spec_from_file = spack.spec.Spec.from_json(stream)
            else:
                spec_from_file = spack.spec.Spec.from_yaml(stream)
        initial_spec._dup(spec_from_file)
        return initial_spec


class EdgeAttributeParser:
    __slots__ = "ctx", "literal_str"

    def __init__(self, ctx, literal_str):
        self.ctx = ctx
        self.literal_str = literal_str

    def parse(self):
        attributes = {}
        while True:
            if self.ctx.accept(TokenType.KEY_VALUE_PAIR):
                name, value = self.ctx.current_token.value.split("=", maxsplit=1)
                name = name.strip("'\" ")
                value = value.strip("'\" ").split(",")
                attributes[name] = value
                if name not in ("deptypes", "virtuals"):
                    msg = (
                        "the only edge attributes that are currently accepted "
                        'are "deptypes" and "virtuals"'
                    )
                    raise SpecParsingError(msg, self.ctx.current_token, self.literal_str)
            # TODO: Add code to accept bool variants here as soon as use variants are implemented
            elif self.ctx.accept(TokenType.END_EDGE_PROPERTIES):
                break
            else:
                msg = "unexpected token in edge attributes"
                raise SpecParsingError(msg, self.ctx.next_token, self.literal_str)

        # Turn deptypes=... to depflag representation
        if "deptypes" in attributes:
            deptype_string = attributes.pop("deptypes")
            attributes["depflag"] = spack.deptypes.canonicalize(deptype_string)
        return attributes


def parse(text: str) -> List["spack.spec.Spec"]:
    """Parse text into a list of strings

    Args:
        text (str): text to be parsed

    Return:
        List of specs
    """
    return SpecParser(text).all_specs()


def parse_one_or_raise(
    text: str, initial_spec: Optional["spack.spec.Spec"] = None
) -> "spack.spec.Spec":
    """Parse exactly one spec from text and return it, or raise

    Args:
        text (str): text to be parsed
        initial_spec: buffer where to parse the spec. If None a new one will be created.
    """
    stripped_text = text.strip()
    parser = SpecParser(stripped_text)
    result = parser.next_spec(initial_spec)
    last_token = parser.ctx.current_token

    if last_token is not None and last_token.end != len(stripped_text):
        message = "a single spec was requested, but parsed more than one:"
        message += f"\n{text}"
        if last_token is not None:
            underline = f"\n{' ' * last_token.end}{'^' * (len(text) - last_token.end)}"
            message += color.colorize(f"@*r{{{underline}}}")
        raise ValueError(message)

    if result is None:
        message = "a single spec was requested, but none was parsed:"
        message += f"\n{text}"
        raise ValueError(message)

    return result


class SpecParsingError(spack.error.SpecSyntaxError):
    """Error when parsing tokens"""

    def __init__(self, message, token, text):
        message += f"\n{text}"
        underline = f"\n{' '*token.start}{'^'*(token.end - token.start)}"
        message += color.colorize(f"@*r{{{underline}}}")
        super().__init__(message)
