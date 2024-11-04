# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.compiler import UnsupportedCompilerFlag
from spack.package import *


class Clingo(CMakePackage):
    """Clingo: A grounder and solver for logic programs

    Clingo is part of the Potassco project for Answer Set
    Programming (ASP). ASP offers a simple and powerful modeling
    language to describe combinatorial problems as logic
    programs. The clingo system then takes such a logic program and
    computes answer sets representing solutions to the given
    problem."""

    homepage = "https://potassco.org/clingo/"
    url = "https://github.com/potassco/clingo/archive/v5.2.2.tar.gz"
    git = "https://github.com/potassco/clingo.git"
    tags = ["windows"]
    maintainers("tgamblin", "alalazo")

    license("MIT")

    version("master", branch="master", submodules=True)
    version("spack", commit="2a025667090d71b2c9dce60fe924feb6bde8f667", submodules=True)

    version("5.7.1", sha256="544b76779676075bb4f557f05a015cbdbfbd0df4b2cc925ad976e86870154d81")
    version("5.7.0", sha256="ed5401bda54315184697fd69ff0f15389c62779e812058a5f296ba587ed9c10b")
    version("5.6.2", sha256="81eb7b14977ac57c97c905bd570f30be2859eabc7fe534da3cdc65eaca44f5be")
    version("5.5.2", sha256="a2a0a590485e26dce18860ac002576232d70accc5bfcb11c0c22e66beb23baa6")
    version("5.5.1", sha256="b9cf2ba2001f8241b8b1d369b6f353e628582e2a00f13566e51c03c4dd61f67e")
    version("5.5.0", sha256="c9d7004a0caec61b636ad1c1960fbf339ef8fdee9719321fc1b6b210613a8499")
    version("5.4.1", sha256="ac6606388abfe2482167ce8fd4eb0737ef6abeeb35a9d3ac3016c6f715bfee02")
    version("5.4.0", sha256="e2de331ee0a6d254193aab5995338a621372517adcf91568092be8ac511c18f3")
    version("5.3.0", sha256="b0d406d2809352caef7fccf69e8864d55e81ee84f4888b0744894977f703f976")
    version("5.2.2", sha256="da1ef8142e75c5a6f23c9403b90d4f40b9f862969ba71e2aaee9a257d058bfcf")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("docs", default=False, description="build documentation with Doxygen")
    variant("python", default=True, description="build with python bindings")

    # See https://github.com/potassco/clingo/blob/v5.5.2/INSTALL.md
    depends_on("cmake@3.1:", type="build")
    depends_on("cmake@3.18:", type="build", when="@5.5:")

    depends_on("doxygen", type="build", when="+docs")

    with when("@spack,master"):
        depends_on("re2c@0.13:", type="build")
        depends_on("bison@2.5:", type="build", when="platform=linux")
        depends_on("bison@2.5:", type="build", when="platform=darwin")
        depends_on("bison@2.5:", type="build", when="platform=freebsd")

    with when("platform=windows"):
        depends_on("re2c@0.13:", type="build")
        depends_on("winbison@2.4.12:")

    with when("+python"):
        extends("python")
        depends_on("python", type=("build", "link", "run"))
        # Clingo 5.5.0 supports Python 3.6 or later and needs CFFI
        depends_on("python@3.6.0:", type=("build", "link", "run"), when="@5.5.0:")
        depends_on("py-cffi", type=("build", "run"), when="@5.5.0: platform=linux")
        depends_on("py-cffi", type=("build", "run"), when="@5.5.0: platform=darwin")
        depends_on("py-cffi", type=("build", "run"), when="@5.5.0: platform=freebsd")

    patch("python38.patch", when="@5.3:5.4.0")
    patch("size-t.patch", when="%msvc")
    patch("vs2022.patch", when="%msvc@19.30:")
    patch("clingo_msc_1938_native_handle.patch", when="@:5.7.0 %msvc@19.38:")

    def patch(self):
        # In bootstrap/prototypes/*.json we don't want to have specs that work for any python
        # version, so this conditional patch lives here instead of being its own directive.
        if self.spec.satisfies("@spack,5.3:5.4 ^python@3.9:"):
            filter_file(
                "if (!PyEval_ThreadsInitialized()) { PyEval_InitThreads(); }",
                "",
                "libpyclingo/pyclingo.cc",
                string=True,
            )
        # Doxygen is optional but can't be disabled with a -D, so patch
        # it out if it's really supposed to be disabled
        if self.spec.satisfies("~docs"):
            filter_file(
                r"find_package\(Doxygen\)",
                'message("Doxygen disabled for Spack build.")',
                "clasp/CMakeLists.txt",
                "clasp/libpotassco/CMakeLists.txt",
            )

    @property
    def cmake_py_shared(self):
        return self.define("CLINGO_BUILD_PY_SHARED", "ON")

    def cmake_args(self):
        try:
            self.compiler.cxx14_flag
        except UnsupportedCompilerFlag:
            InstallError("clingo requires a C++14-compliant C++ compiler")

        args = [self.define("CLINGO_BUILD_WITH_LUA", False)]

        if self.spec.satisfies("+python"):
            suffix = python(
                "-c", "import sysconfig; print(sysconfig.get_config_var('EXT_SUFFIX'))", output=str
            ).strip()
            args += [
                self.define("CLINGO_REQUIRE_PYTHON", True),
                self.define("CLINGO_BUILD_WITH_PYTHON", True),
                self.define("PYCLINGO_USER_INSTALL", False),
                self.define("PYCLINGO_USE_INSTALL_PREFIX", True),
                self.define("PYCLINGO_INSTALL_DIR", python_platlib),
                self.define("PYCLINGO_SUFFIX", suffix),
                self.cmake_py_shared,
            ]
        else:
            args += [self.define("CLINGO_BUILD_WITH_PYTHON", False)]

        # Use LTO also for non-Intel compilers please. This can be removed when they
        # bump cmake_minimum_required to VERSION 3.9.
        if self.spec.satisfies("+ipo"):
            args.append(self.define("CMAKE_POLICY_DEFAULT_CMP0069", "NEW"))

        return args

    def win_add_library_dependent(self):
        return [python_platlib] if "+python" in self.spec else []
