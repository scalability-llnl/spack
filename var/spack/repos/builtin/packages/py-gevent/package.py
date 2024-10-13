# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGevent(PythonPackage):
    """gevent is a coroutine-based Python networking library."""

    homepage = "https://www.gevent.org"
    pypi = "gevent/gevent-23.7.0.tar.gz"
    git = "https://github.com/gevent/gevent.git"

    license("MIT")

    version("23.7.0", sha256="d0d3630674c1b344b256a298ab1ff43220f840b12af768131b5d74e485924237")
    version("21.12.0", sha256="f48b64578c367b91fa793bf8eaaaf4995cb93c8bc45860e473bf868070ad094e")
    version("21.8.0", sha256="43e93e1a4738c922a2416baf33f0afb0a20b22d3dba886720bc037cd02a98575")
    version("1.5.0", sha256="b2814258e3b3fb32786bb73af271ad31f51e1ac01f33b37426b66cb8491b4c29")

    depends_on("c", type="build")  # generated

    depends_on("python@3.8:", when="@23.7.0:", type=("build", "run"))
    depends_on("python@:3.10", when="@:21.12", type=("build", "run"))

    depends_on("py-setuptools@40.8:", when="@20.5.1:", type=("build", "run"))
    depends_on("py-setuptools@40.8:", when="@1.5:", type="build")
    depends_on("py-setuptools@24.2:", when="@:1.4", type="build")
    depends_on("py-cython@3:", when="@20.5.1:", type="build")
    depends_on("py-cython@0.29.14:", when="@1.5:", type="build")
    depends_on("py-cffi@1.12.3:", type=("build", "run"))
    depends_on("py-greenlet@3:", when="@23.7: ^python@3.12:", type=("build", "run"))
    depends_on("py-greenlet@2:", when="@22.10.2: ^python@:3.11", type=("build", "run"))
    depends_on("py-greenlet@1.1:1", when="@21.8:21.12.0", type=("build", "run"))
    depends_on("py-greenlet@0.4.17:1", when="@20.12:21.1.2", type=("build", "run"))
    depends_on("py-greenlet@0.4.14:", type=("build", "run"))
    depends_on("py-zope-event", when="@20.5.1:", type=("build", "run"))
    depends_on("py-zope-interface", when="@20.5.1:", type=("build", "run"))

    # https://github.com/gevent/gevent/issues/1599
    conflicts("^py-cython@3:", when="@:20.5.0")

    # Deprecated compiler options. upstream PR: https://github.com/gevent/gevent/pull/1896
    patch("icc.patch", when="@:21.12.0 %intel")

    # https://github.com/gevent/gevent/issues/2031
    patch("cython.patch", when="@:24.2.1^py-cython@3.0.10:3.0.11")

    @run_before("install")
    def recythonize(self):
        # Clean pre-generated cython files -- we've seen issues with Python 3.8 due to
        # an old cython that was used to generate the C sources.
        # On top of that, they specify a prerequisite on a file in cython's prefix,
        # meaning that cython runs again depending on whether it was installed before e.g.
        # 2020... So, just clean and re-run from scratch instead.
        python("setup.py", "clean")

    def flag_handler(self, name, flags):
        if name == "cflags":
            if self.spec.satisfies("%oneapi@2023:"):
                flags.append("-Wno-error=incompatible-function-pointer-types")
            if self.spec.compiler.name in ["intel", "oneapi"]:
                flags.append("-we147")
        return (flags, None, None)
