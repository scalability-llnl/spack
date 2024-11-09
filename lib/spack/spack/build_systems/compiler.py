# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import itertools
import os
import pathlib
import re
import sys
from typing import Dict, List, Sequence, Tuple, Union

import llnl.util.tty as tty
from llnl.util.lang import classproperty

import spack.compiler
import spack.package_base
import spack.util.executable

# Local "type" for type hints
Path = Union[str, pathlib.Path]


class CompilerPackage(spack.package_base.PackageBase):
    """A Package mixin for all common logic for packages that implement compilers"""

    # TODO: how do these play nicely with other tags
    tags: Sequence[str] = ["compiler"]

    #: Optional suffix regexes for searching for this type of compiler.
    #: Suffixes are used by some frameworks, e.g. macports uses an '-mp-X.Y'
    #: version suffix for gcc.
    compiler_suffixes: List[str] = [r"-.*"]

    #: Optional prefix regexes for searching for this compiler
    compiler_prefixes: List[str] = []

    #: Compiler argument(s) that produces version information
    #: If multiple arguments, the earlier arguments must produce errors when invalid
    compiler_version_argument: Union[str, Tuple[str]] = "-dumpversion"

    #: Regex used to extract version from compiler's output
    compiler_version_regex: str = "(.*)"

    #: Static definition of languages supported by this class
    compiler_languages: Sequence[str] = ["c", "cxx", "fortran"]

    def __init__(self, spec: "spack.spec.Spec"):
        super().__init__(spec)
        msg = f"Supported languages for {spec} are not a subset of possible supported languages"
        msg += f"    supports: {self.supported_languages}, valid values: {self.compiler_languages}"
        assert set(self.supported_languages) <= set(self.compiler_languages), msg

    @property
    def supported_languages(self) -> Sequence[str]:
        """Dynamic definition of languages supported by this package"""
        return self.compiler_languages

    @classproperty
    def compiler_names(cls) -> Sequence[str]:
        """Construct list of compiler names from per-language names"""
        names = []
        for language in cls.compiler_languages:
            names.extend(getattr(cls, f"{language}_names"))
        return names

    @classproperty
    def executables(cls) -> Sequence[str]:
        """Construct executables for external detection from names, prefixes, and suffixes."""
        regexp_fmt = r"^({0}){1}({2})$"
        prefixes = [""] + cls.compiler_prefixes
        suffixes = [""] + cls.compiler_suffixes
        if sys.platform == "win32":
            ext = r"\.(?:exe|bat)"
            suffixes += [suf + ext for suf in suffixes]
        return [
            regexp_fmt.format(prefix, re.escape(name), suffix)
            for prefix, name, suffix in itertools.product(prefixes, cls.compiler_names, suffixes)
        ]

    @classmethod
    def determine_version(cls, exe: Path):
        version_argument = cls.compiler_version_argument
        if isinstance(version_argument, str):
            version_argument = (version_argument,)

        for va in version_argument:
            try:
                output = spack.compiler.get_compiler_version_output(exe, va)
                match = re.search(cls.compiler_version_regex, output)
                if match:
                    return ".".join(match.groups())
            except spack.util.executable.ProcessError:
                pass
            except Exception as e:
                tty.debug(
                    f"[{__file__}] Cannot detect a valid version for the executable "
                    f"{str(exe)}, for package '{cls.name}': {e}"
                )

    @classmethod
    def compiler_bindir(cls, prefix: Path) -> Path:
        """Overridable method for the location of the compiler bindir within the preifx"""
        return os.path.join(prefix, "bin")

    @classmethod
    def determine_compiler_paths(cls, exes: Sequence[Path]) -> Dict[str, Path]:
        """Compute the paths to compiler executables associated with this package

        This is a helper method for ``determine_variants`` to compute the ``extra_attributes``
        to include with each spec object."""
        # There are often at least two copies (not symlinks) of each compiler executable in the
        # same directory: one with a canonical name, e.g. "gfortran", and another one with the
        # target prefix, e.g. "x86_64-pc-linux-gnu-gfortran". There also might be a copy of "gcc"
        # with the version suffix, e.g. "x86_64-pc-linux-gnu-gcc-6.3.0". To ensure the consistency
        # of values in the "paths" dictionary (i.e. we prefer all of them to reference copies
        # with canonical names if possible), we iterate over the executables in the reversed sorted
        # order:
        # First pass over languages identifies exes that are perfect matches for canonical names
        # Second pass checks for names with prefix/suffix
        # Second pass is sorted by language name length because longer named languages
        # e.g. cxx can often contain the names of shorter named languages
        # e.g. c (e.g. clang/clang++)
        paths = {}
        exes = sorted(exes, reverse=True)
        languages = {
            lang: getattr(cls, f"{lang}_names")
            for lang in sorted(cls.compiler_languages, key=len, reverse=True)
        }
        for exe in exes:
            for lang, names in languages.items():
                if os.path.basename(exe) in names:
                    paths[lang] = exe
                    break
            else:
                for lang, names in languages.items():
                    if any(name in os.path.basename(exe) for name in names):
                        paths[lang] = exe
                        break

        return paths

    @classmethod
    def determine_variants(cls, exes: Sequence[Path], version_str: str) -> Tuple:
        # path determination is separated so it can be reused in subclasses
        return "", {"compilers": cls.determine_compiler_paths(exes=exes)}
