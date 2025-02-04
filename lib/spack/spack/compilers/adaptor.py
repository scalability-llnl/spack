# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import enum
from typing import Dict, List

from llnl.util import lang

import spack.spec

from .libraries import CompilerPropertyDetector


class Languages(enum.Enum):
    C = "c"
    CXX = "cxx"
    FORTRAN = "fortran"


class CompilerAdaptor:
    def __init__(
        self, compiled_spec: spack.spec.Spec, compilers: Dict[Languages, spack.spec.Spec]
    ) -> None:
        if not compilers:
            raise AttributeError(f"{compiled_spec} has no 'compiler' attribute")

        self.compilers = compilers
        self.compiled_spec = compiled_spec

    def _lang_exists_or_raise(self, name: str, *, lang: Languages) -> None:
        if lang not in self.compilers:
            raise AttributeError(
                f"'{self.compiled_spec}' has no {lang.value} compiler, so the "
                f"'{name}' property cannot be retrieved"
            )

    def _maybe_return_attribute(self, name: str, *, lang: Languages) -> str:
        self._lang_exists_or_raise(name, lang=lang)
        return getattr(self.compilers[lang].package, name)

    @property
    def cc_rpath_arg(self) -> str:
        self._lang_exists_or_raise("cc_rpath_arg", lang=Languages.C)
        return self.compilers[Languages.C].package.rpath_arg

    @property
    def cxx_rpath_arg(self) -> str:
        self._lang_exists_or_raise("cxx_rpath_arg", lang=Languages.CXX)
        return self.compilers[Languages.CXX].package.rpath_arg

    @property
    def fc_rpath_arg(self) -> str:
        self._lang_exists_or_raise("fc_rpath_arg", lang=Languages.FORTRAN)
        return self.compilers[Languages.FORTRAN].package.rpath_arg

    @property
    def f77_rpath_arg(self) -> str:
        self._lang_exists_or_raise("f77_rpath_arg", lang=Languages.FORTRAN)
        return self.compilers[Languages.FORTRAN].package.rpath_arg

    @property
    def linker_arg(self) -> str:
        return self._maybe_return_attribute("linker_arg", lang=Languages.C)

    @property
    def name(self):
        return next(iter(self.compilers.values())).name

    @property
    def version(self):
        return next(iter(self.compilers.values())).version

    def implicit_rpaths(self) -> List[str]:
        result, seen = [], set()
        for compiler in self.compilers.values():
            if compiler in seen:
                continue
            seen.add(compiler)
            result.extend(CompilerPropertyDetector(compiler).implicit_rpaths())
        return result

    @property
    def openmp_flag(self) -> str:
        return next(iter(self.compilers.values())).package.openmp_flag

    @property
    def cxx98_flag(self) -> str:
        return self.compilers[Languages.CXX].package.standard_flag(
            language=Languages.CXX.value, standard="98"
        )

    @property
    def cxx11_flag(self) -> str:
        return self.compilers[Languages.CXX].package.standard_flag(
            language=Languages.CXX.value, standard="11"
        )

    @property
    def cxx14_flag(self) -> str:
        return self.compilers[Languages.CXX].package.standard_flag(
            language=Languages.CXX.value, standard="14"
        )

    @property
    def cxx17_flag(self) -> str:
        return self.compilers[Languages.CXX].package.standard_flag(
            language=Languages.CXX.value, standard="17"
        )

    @property
    def cxx20_flag(self) -> str:
        return self.compilers[Languages.CXX].package.standard_flag(
            language=Languages.CXX.value, standard="20"
        )

    @property
    def cxx23_flag(self) -> str:
        return self.compilers[Languages.CXX].package.standard_flag(
            language=Languages.CXX.value, standard="23"
        )

    @property
    def c99_flag(self) -> str:
        return self.compilers[Languages.C].package.standard_flag(
            language=Languages.C.value, standard="99"
        )

    @property
    def c11_flag(self) -> str:
        return self.compilers[Languages.C].package.standard_flag(
            language=Languages.C.value, standard="11"
        )

    @property
    def c17_flag(self) -> str:
        return self.compilers[Languages.C].package.standard_flag(
            language=Languages.C.value, standard="17"
        )

    @property
    def c23_flag(self) -> str:
        return self.compilers[Languages.C].package.standard_flag(
            language=Languages.C.value, standard="17"
        )

    @property
    def cc_pic_flag(self) -> str:
        self._lang_exists_or_raise("cc_pic_flag", lang=Languages.C)
        return self.compilers[Languages.C].package.pic_flag

    @property
    def cxx_pic_flag(self) -> str:
        self._lang_exists_or_raise("cxx_pic_flag", lang=Languages.CXX)
        return self.compilers[Languages.CXX].package.pic_flag

    @property
    def fc_pic_flag(self) -> str:
        self._lang_exists_or_raise("fc_pic_flag", lang=Languages.FORTRAN)
        return self.compilers[Languages.FORTRAN].package.pic_flag

    @property
    def f77_pic_flag(self) -> str:
        self._lang_exists_or_raise("f77_pic_flag", lang=Languages.FORTRAN)
        return self.compilers[Languages.FORTRAN].package.pic_flag

    @property
    def prefix(self) -> str:
        return next(iter(self.compilers.values())).prefix

    @property
    def extra_rpaths(self) -> List[str]:
        compiler = next(iter(self.compilers.values()))
        return getattr(compiler, "extra_attributes", {}).get("extra_rpaths", [])

    @property
    def cc(self):
        return self._maybe_return_attribute("cc", lang=Languages.C)

    @property
    def cxx(self):
        return self._maybe_return_attribute("cxx", lang=Languages.CXX)

    @property
    def fc(self):
        self._lang_exists_or_raise("fc", lang=Languages.FORTRAN)
        return self.compilers[Languages.FORTRAN].package.fortran

    @property
    def f77(self):
        self._lang_exists_or_raise("f77", lang=Languages.FORTRAN)
        return self.compilers[Languages.FORTRAN].package.fortran


class DeprecatedCompiler(lang.DeprecatedProperty):
    def __init__(self) -> None:
        super().__init__(name="compiler")

    def factory(self, instance, owner) -> CompilerAdaptor:
        spec = instance.spec
        if not spec.concrete:
            raise ValueError("Can only get a compiler for a concrete package.")

        compilers = {}
        for language in Languages:
            deps = spec.dependencies(virtuals=[language.value])
            if deps:
                compilers[language] = deps[0]

        return CompilerAdaptor(instance, compilers)
