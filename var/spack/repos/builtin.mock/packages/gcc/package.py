# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

from spack.package import *


class Gcc(CompilerPackage, Package):
    """Simple compiler package."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/gcc-1.0.tar.gz"

    version("14.0", md5="abcdef0123456789abcdef0123456789")
    version("3.0", md5="def0123456789abcdef0123456789abc")
    version("2.0", md5="abcdef0123456789abcdef0123456789")
    version("1.0", md5="0123456789abcdef0123456789abcdef")

    variant(
        "languages",
        default="c,c++,fortran",
        values=("c", "c++", "fortran"),
        multi=True,
        description="Compilers and runtime libraries to build",
    )

    provides("c", when="languages=c")
    provides("cxx", when="languages=c++")
    provides("fortran", when="languages=fortran")

    depends_on("c", type="build")

    c_names = ["gcc"]
    cxx_names = ["g++"]
    fortran_names = ["gfortran"]
    compiler_prefixes = [r"\w+-\w+-\w+-"]
    compiler_suffixes = [r"-mp-\d+(?:\.\d+)?", r"-\d+(?:\.\d+)?", r"\d\d"]
    compiler_version_regex = r"(?<!clang version)\s?([0-9.]+)"
    compiler_version_argument = ("-dumpfullversion", "-dumpversion")

    link_paths = {
        "c": os.path.join("gcc", "gcc"),
        "cxx": os.path.join("gcc", "g++"),
        "fortran": os.path.join("gcc", "gfortran"),
    }

    def install(self, spec, prefix):
        # Create the minimal compiler that will fool `spack compiler find`
        mkdirp(prefix.bin)
        with open(prefix.bin.gcc, "w", encoding="utf-8") as f:
            f.write('#!/bin/bash\necho "%s"' % str(spec.version))
        set_executable(prefix.bin.gcc)

    @property
    def cc(self):
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("c", None)
        result = None
        if "languages=c" in self.spec:
            result = str(self.spec.prefix.bin.gcc)
        return result

    @property
    def cxx(self):
        msg = "cannot retrieve C++ compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("cxx", None)
        result = None
        if "languages=c++" in self.spec:
            result = os.path.join(self.spec.prefix.bin, "g++")
        return result

    @property
    def fortran(self):
        msg = "cannot retrieve Fortran compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("fortran", None)
        result = None
        if "languages=fortran" in self.spec:
            result = str(self.spec.prefix.bin.gfortran)
        return result

    @classmethod
    def runtime_constraints(cls, *, spec, pkg):
        """Callback function to inject runtime-related rules into the solver.

        Rule-injection is obtained through method calls of the ``pkg`` argument.

        Documentation for this function is temporary. When the API will be in its final state,
        we'll document the behavior at https://spack.readthedocs.io/en/latest/

        Args:
            spec: spec that will inject runtime dependencies
            pkg: object used to forward information to the solver
        """
        pkg("*").depends_on(
            "gcc-runtime",
            when="%gcc",
            type="link",
            description="If any package uses %gcc, it depends on gcc-runtime",
        )
        pkg("*").depends_on(
            f"gcc-runtime@{str(spec.version)}:",
            when=f"^[deptypes=build] {spec.name}@{spec.versions}",
            type="link",
            description=f"If any package uses %{str(spec)}, "
            f"it depends on gcc-runtime@{str(spec.version)}:",
        )

        gfortran_str = "libgfortran@5"
        if spec.satisfies("gcc@:6"):
            gfortran_str = "libgfortran@3"
        elif spec.satisfies("gcc@7"):
            gfortran_str = "libgfortran@4"

        for fortran_virtual in ("fortran-rt", gfortran_str):
            pkg("*").depends_on(
                fortran_virtual,
                when=f"^[virtuals=fortran deptypes=build] {spec.name}@{spec.versions}",
                type="link",
                description=f"Add a dependency on '{gfortran_str}' for nodes compiled with "
                f"{str(spec)} and using the 'fortran' language",
            )
        # The version of gcc-runtime is the same as the %gcc used to "compile" it
        pkg("gcc-runtime").requires(
            f"@{str(spec.versions)}", when=f"^[deptypes=build] {spec.name}@{spec.versions}"
        )

        # If a node used %gcc@X.Y its dependencies must use gcc-runtime@:X.Y
        # (technically @:X is broader than ... <= @=X but this should work in practice)
        pkg("*").propagate(
            f"gcc@:{str(spec.version)}", when=f"^[deptypes=build] {spec.name}@{spec.versions}"
        )
