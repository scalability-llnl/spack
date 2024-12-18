# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import llnl.util.filesystem as fs

from spack.package import *


class PyPythran(PythonPackage):
    """Ahead of Time compiler for numeric kernels."""

    homepage = "https://github.com/serge-sans-paille/pythran"
    pypi = "pythran/pythran-0.9.11.tar.gz"
    tags = ["build-tools"]

    license("BSD-3-Clause")
    maintainers("rgommers")

    version("0.16.1", sha256="861748c0f9c7d422b32724b114b3817d818ed4eab86c09781aa0a3f7ceabb7f9")
    version("0.16.0", sha256="37dcf6aa9713b352b05004e3a20d14b3de7399bb0d7fe2027bd2b9e2833fe65a")
    version("0.15.0", sha256="f9bc61bcb96df2cd4b578abc5a62dfb3fbb0b0ef02c264513dfb615c5f87871c")
    version("0.12.2", sha256="2344c7ad76255f31f79d87877cc6bb8bddc5e5593015dae29b3f821c6c06a627")
    version("0.12.0", sha256="eff3dd0d3eebe57372f0d14f82985525e9bcdfb5b1d1010e1932cf9207060f9f")
    version("0.11.0", sha256="0b2cba712e09f7630879dff69f268460bfe34a6d6000451b47d598558a92a875")
    version("0.10.0", sha256="9dac8e1d50f33d4676003e350b1f0c878ce113e6f907920e92dc103352cac5bf")
    version("0.9.12", sha256="5d50dc74dca1d3f902941865acbae981fc24cceeb9d54673d68d6b5c8c1b0001")
    version("0.9.11", sha256="a317f91e2aade9f6550dc3bf40b5caeb45b7e012daf27e2b3e4ad928edb01667")
    version("0.9.10", sha256="8fa1d19624cb2950e5a18974fdcb0dffc57e1a821049dc95df09563edd673915")
    version("0.9.9", sha256="aaabc97f30ad46d1d62303323de6697d2933779afa4666c15b0f433cb50825b1")
    version("0.9.8", sha256="81c10a16fce9ed41211fb70e82fda6984e93f4602a164934648db8cbb08156b3")
    version("0.9.7", sha256="ac36a94bd862e3c80dae585158b90d3e7c5c05fd252819f3ca7d880a1c7c1012")
    version("0.9.6", sha256="2d102a55d9d53f77cf0f4a904eeb5cbaa8fe76e4892319a859fc618401e2f6ba")
    version("0.9.5", sha256="815a778d6889593c0b8ddf08052cff36a504ce4cc8bd8d7bfb856a212f91486e")
    version("0.9.4", sha256="ec9c91f5331454263b064027292556a184a9f55a50f8615e09b08f57a4909855")
    version("0.9.3", sha256="217427a8225a331fdc8f3efe57871aed775cdf2c6e847a0a83df0aaae4b02493")

    depends_on("cxx", type="build")  # generated

    # https://github.com/serge-sans-paille/pythran/pull/2196
    depends_on("py-setuptools@62:", when="@0.15:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-ply@3.4:", type=("build", "run"))
    depends_on("py-gast@0.5", when="@0.15:", type=("build", "run"))
    # upper bound due to https://github.com/scipy/scipy/issues/18390
    depends_on("py-gast@0.5:0.5.3", when="@0.9.12:0.12", type=("build", "run"))
    depends_on("py-gast@0.4", when="@0.9.7:0.9.11", type=("build", "run"))
    depends_on("py-gast@0.3.3:0.3", when="@0.9.6", type=("build", "run"))
    depends_on("py-gast@0.3:", when="@0.9.4:0.9.5", type=("build", "run"))
    depends_on("py-gast", when="@:0.9.3", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    # https://github.com/serge-sans-paille/pythran/issues/2189
    depends_on("py-numpy@:1", when="@:0.15", type=("build", "run"))
    depends_on("py-beniget@0.4", when="@0.9.12:", type=("build", "run"))
    depends_on("py-beniget@0.3", when="@0.9.7:0.9.11", type=("build", "run"))
    depends_on("py-beniget@0.2.1:0.2", when="@0.9.6", type=("build", "run"))
    depends_on("py-beniget@0.2:", when="@0.9.4:0.9.5", type=("build", "run"))
    depends_on("py-beniget", when="@:0.9.3", type=("build", "run"))
    depends_on("llvm-openmp", when="%apple-clang", type=("build", "run"))

    # Historical dependencies
    depends_on("py-pytest-runner", type="build", when="@:0.9")
    depends_on("py-networkx@2:", when="@:0.9.11", type=("build", "run"))
    depends_on("py-decorator", when="@:0.9.11", type=("build", "run"))
    depends_on("py-six", when="@:0.9.11", type=("build", "run"))

    # https://github.com/serge-sans-paille/pythran/pull/1856
    patch("omp.patch", when="@0.9.10:0.9.12")

    # https://github.com/serge-sans-paille/pythran/pull/2029
    patch(
        "https://github.com/serge-sans-paille/pythran/commit/00a454a9c33ff05852c8d36a73cc1aadb9690c9a.patch?full_index=1",
        sha256="5ccf989a259e33e942b7dde39f8e90917e12afd7fda16ec90e9adad8ccf444fb",
        when="@:0.12.0",
    )

    # https://github.com/serge-sans-paille/pythran/issues/1937
    conflicts("%apple-clang@13:", when="@:0.10")
    # https://github.com/serge-sans-paille/pythran/issues/2101
    conflicts("^python@3.11:", when="@:0.12.1")
    # from distutils.errors import CompileError in run.py
    conflicts("^python@3.12:", when="@:0.15")

    @property
    def headers(self):
        # Pythran is mainly meant to be used as a compiler, so return no headers to
        # avoid issue https://github.com/spack/spack/issues/33237 This can be refined
        # later to allow using pythran also as a library.
        return fs.HeaderList([])

    def patch(self):
        # Compiler is used at run-time to determine name of OpenMP library to search for
        cfg_file = join_path("pythran", "pythran-{0}.cfg".format(sys.platform))
        filter_file("CXX=", "CXX=" + self.compiler.cxx, cfg_file)

    def setup_build_environment(self, env):
        # Needed for `spack install --test=root py-pythran`
        if self.spec.satisfies("%apple-clang"):
            env.prepend_path(
                "DYLD_FALLBACK_LIBRARY_PATH", self.spec["llvm-openmp"].libs.directories[0]
            )

    def setup_run_environment(self, env):
        # Needed for `spack test run py-pythran`
        self.setup_build_environment(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Needed for `spack install py-scipy`
        self.setup_build_environment(env)

    def setup_dependent_run_environment(self, env, dependent_spec):
        # Probably needed for something?
        self.setup_build_environment(env)
