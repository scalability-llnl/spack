# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Low-level wrappers around clingo API."""
import importlib
import pathlib
from types import ModuleType
from typing import Any, Callable, NamedTuple, Optional, Tuple, Union

from llnl.util import lang


def _ast_getter(*names: str) -> Callable[[Any], Any]:
    """Helper to retrieve AST attributes from different versions of the clingo API"""

    def getter(node):
        for name in names:
            result = getattr(node, name, None)
            if result:
                return result
        raise KeyError(f"node has no such keys: {names}")

    return getter


ast_type = _ast_getter("ast_type", "type")
ast_sym = _ast_getter("symbol", "term")


class AspObject:
    """Object representing a piece of ASP code."""


def _id(thing: Any) -> Union[str, AspObject]:
    """Quote string if needed for it to be a valid identifier."""
    if isinstance(thing, AspObject):
        return thing
    elif isinstance(thing, bool):
        return f'"{str(thing)}"'
    elif isinstance(thing, int):
        return str(thing)
    else:
        return f'"{str(thing)}"'


@lang.key_ordering
class AspFunction(AspObject):
    """A term in the ASP logic program"""

    __slots__ = ["name", "args"]

    def __init__(self, name: str, args: Optional[Tuple[Any, ...]] = None) -> None:
        self.name = name
        self.args = () if args is None else tuple(args)

    def _cmp_key(self) -> Tuple[str, Optional[Tuple[Any, ...]]]:
        return self.name, self.args

    def __call__(self, *args: Any) -> "AspFunction":
        """Return a new instance of this function with added arguments.

        Note that calls are additive, so you can do things like::

            >>> attr = AspFunction("attr")
            attr()

            >>> attr("version")
            attr("version")

            >>> attr("version")("foo")
            attr("version", "foo")

            >>> v = AspFunction("attr", "version")
            attr("version")

            >>> v("foo", "bar")
            attr("version", "foo", "bar")

        """
        return AspFunction(self.name, self.args + args)

    def _argify(self, arg: Any) -> Any:
        """Turn the argument into an appropriate clingo symbol"""
        if isinstance(arg, bool):
            return clingo().String(str(arg))
        elif isinstance(arg, int):
            return clingo().Number(arg)
        elif isinstance(arg, AspFunction):
            return clingo().Function(arg.name, [self._argify(x) for x in arg.args], positive=True)
        return clingo().String(str(arg))

    def symbol(self):
        """Return a clingo symbol for this function"""
        return clingo().Function(
            self.name, [self._argify(arg) for arg in self.args], positive=True
        )

    def __str__(self) -> str:
        return f"{self.name}({', '.join(str(_id(arg)) for arg in self.args)})"

    def __repr__(self) -> str:
        return str(self)


class _AspFunctionBuilder:
    def __getattr__(self, name):
        return AspFunction(name)


#: Global AspFunction builder
fn = _AspFunctionBuilder()

_CLINGO_MODULE: Optional[ModuleType] = None


def clingo() -> ModuleType:
    """Lazy imports the Python module for clingo, and returns it."""
    if _CLINGO_MODULE is not None:
        return _CLINGO_MODULE

    try:
        clingo_mod = importlib.import_module("clingo")
        # Make sure we didn't import an empty module
        _ensure_clingo_or_raise(clingo_mod)
    except ImportError:
        clingo_mod = None

    if clingo_mod is not None:
        return _set_clingo_module_cache(clingo_mod)

    clingo_mod = _bootstrap_clingo()
    return _set_clingo_module_cache(clingo_mod)


def _set_clingo_module_cache(clingo_mod: ModuleType) -> ModuleType:
    """Sets the global cache to the lazy imported clingo module"""
    global _CLINGO_MODULE
    importlib.import_module("clingo.ast")
    _CLINGO_MODULE = clingo_mod
    return clingo_mod


def _ensure_clingo_or_raise(clingo_mod: ModuleType) -> None:
    """Ensures the clingo module can access expected attributes, otherwise raises an error."""
    # These are imports that may be problematic at top level (circular imports). They are used
    # only to provide exhaustive details when erroring due to a broken clingo module.
    import spack.config
    import spack.paths as sp
    import spack.util.path as sup

    try:
        clingo_mod.Symbol
    except AttributeError:
        assert clingo_mod.__file__ is not None, "clingo installation is incomplete or invalid"
        # Reaching this point indicates a broken clingo installation
        # If Spack derived clingo, suggest user re-run bootstrap
        # if non-spack, suggest user investigate installation
        # assume Spack is not responsible for broken clingo
        msg = (
            f"Clingo installation at {clingo_mod.__file__} is incomplete or invalid."
            "Please repair installation or re-install. "
            "Alternatively, consider installing clingo via Spack."
        )
        # check whether Spack is responsible
        if (
            pathlib.Path(
                sup.canonicalize_path(
                    spack.config.CONFIG.get("bootstrap:root", sp.default_user_bootstrap_path)
                )
            )
            in pathlib.Path(clingo_mod.__file__).parents
        ):
            # Spack is responsible for the broken clingo
            msg = (
                "Spack bootstrapped copy of Clingo is broken, "
                "please re-run the bootstrapping process via command `spack bootstrap now`."
                " If this issue persists, please file a bug at: github.com/spack/spack"
            )
        raise RuntimeError(
            "Clingo installation may be broken or incomplete, "
            "please verify clingo has been installed correctly"
            "\n\nClingo does not provide symbol clingo.Symbol"
            f"{msg}"
        )


def clingo_cffi() -> bool:
    """Returns True if clingo uses the CFFI interface"""
    return hasattr(clingo().Symbol, "_rep")


def _bootstrap_clingo() -> ModuleType:
    """Bootstraps the clingo module and returns it"""
    import spack.bootstrap

    with spack.bootstrap.ensure_bootstrap_configuration():
        spack.bootstrap.ensure_clingo_importable_or_raise()
        clingo_mod = importlib.import_module("clingo")

    return clingo_mod


def parse_files(*args, **kwargs):
    """Wrapper around clingo parse_files, that dispatches the function according
    to clingo API version.
    """
    clingo()
    try:
        return importlib.import_module("clingo.ast").parse_files(*args, **kwargs)
    except (ImportError, AttributeError):
        return clingo().parse_files(*args, **kwargs)


def parse_term(*args, **kwargs):
    """Wrapper around clingo parse_term, that dispatches the function according
    to clingo API version.
    """
    clingo()
    try:
        return importlib.import_module("clingo.symbol").parse_term(*args, **kwargs)
    except (ImportError, AttributeError):
        return clingo().parse_term(*args, **kwargs)


class NodeArgument(NamedTuple):
    """Represents a node in the DAG"""

    id: str
    pkg: str


class NodeFlag(NamedTuple):
    flag_type: str
    flag: str
    flag_group: str
    source: str


def intermediate_repr(sym):
    """Returns an intermediate representation of clingo models for Spack's spec builder.

    Currently, transforms symbols from clingo models either to strings or to NodeArgument objects.

    Returns:
        This will turn a ``clingo.Symbol`` into a string or NodeArgument, or a sequence of
        ``clingo.Symbol`` objects into a tuple of those objects.
    """
    # TODO: simplify this when we no longer have to support older clingo versions.
    if isinstance(sym, (list, tuple)):
        return tuple(intermediate_repr(a) for a in sym)

    try:
        if sym.name == "node":
            return NodeArgument(
                id=intermediate_repr(sym.arguments[0]), pkg=intermediate_repr(sym.arguments[1])
            )
        elif sym.name == "node_flag":
            return NodeFlag(
                flag_type=intermediate_repr(sym.arguments[0]),
                flag=intermediate_repr(sym.arguments[1]),
                flag_group=intermediate_repr(sym.arguments[2]),
                source=intermediate_repr(sym.arguments[3]),
            )
    except RuntimeError:
        # This happens when using clingo w/ CFFI and trying to access ".name" for symbols
        # that are not functions
        pass

    if clingo_cffi():
        # Clingo w/ CFFI will throw an exception on failure
        try:
            return sym.string
        except RuntimeError:
            return str(sym)
    else:
        return sym.string or str(sym)


def extract_args(model, predicate_name):
    """Extract the arguments to predicates with the provided name from a model.

    Pull out all the predicates with name ``predicate_name`` from the model, and
    return their intermediate representation.
    """
    return [intermediate_repr(sym.arguments) for sym in model if sym.name == predicate_name]
