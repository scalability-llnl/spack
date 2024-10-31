# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class PyCffi(PythonPackage):
    """Foreign Function Interface for Python calling C code"""

    homepage = "https://cffi.readthedocs.io/en/latest/"
    pypi = "cffi/cffi-1.13.0.tar.gz"

    license("MIT")

    version("1.17.1", sha256="1c39c6016c32bc48dd54561950ebd6836e1670f2ae46128f67cf49e789c52824")
    version("1.16.0", sha256="bcb3ef43e58665bbda2fb198698fcae6776483e0c4a631aa5647806c25e02cc0")
    version("1.15.1", sha256="d400bfb9a37b1351253cb402671cea7e89bdecc294e8016a707f6d1d8ac934f9")
    version("1.15.0", sha256="920f0d66a896c2d99f0adbb391f990a84091179542c205fa53ce5787aff87954")
    version("1.14.6", sha256="c9a875ce9d7fe32887784274dd533c57909b7b1dcadcc128a2ac21331a9765dd")
    version("1.14.3", sha256="f92f789e4f9241cd262ad7a555ca2c648a98178a953af117ef7fad46aa1d5591")
    version("1.13.0", sha256="8fe230f612c18af1df6f348d02d682fe2c28ca0a6c3856c99599cdacae7cf226")
    version("1.12.2", sha256="e113878a446c6228669144ae8a56e268c91b7f1fafae927adc4879d9849e0ea7")
    version("1.11.5", sha256="e90f17980e6ab0f3c2f3730e56d1fe9bcba1891eeea58966e89d352492cc74f4")
    version("1.10.0", sha256="b3b02911eb1f6ada203b0763ba924234629b51586f72a21faacc638269f4ced5")
    version("1.1.2", sha256="390970b602708c91ddc73953bb6929e56291c18a4d80f360afa00fad8b6f3339")

    depends_on("c", type="build")  # generated

    # ./spack-src/cffi/ffiplatform.py has _hack_at_distutils which imports
    # setuptools before distutils, but only on Windows. This could be made
    # unconditional to support Python 3.12
    depends_on("python@:3.11", type=("build", "run"))

    # python 3.12 support was released in @1.16:, however the removal
    # in python3.12 of distutils has resulted in an imperfect fix for prefix-based
    # tools like spack, see:
    # https://github.com/spack/spack/pull/46224
    # https://github.com/cython/cython/pull/5754#issuecomment-1752102480
    # until this is correctly fixed, do not enable 3.12 support
    # depends_on("python@:3.12", type=("build", "run"), when="@1.16:")

    depends_on("pkgconfig", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@66.1:", type="build", when="@1.16:")
    depends_on("py-pycparser", type=("build", "run"))
    depends_on("libffi")

    # This patch enables allocate write+execute memory for ffi.callback() on macos
    # https://github.com/conda-forge/cffi-feedstock/pull/47/files
    patch(
        "https://raw.githubusercontent.com/conda-forge/cffi-feedstock/refs/heads/main/recipe/0003-apple-api.patch",
        when="@1.16: platform=darwin",
        sha256="db836e67e2973ba7d3f4185b385fda49e2398281fc10362e5e413b75fdf93bf0",
    )

    def flag_handler(self, name, flags):
        if self.spec.satisfies("%clang@13:"):
            if name in ["cflags", "cxxflags", "cppflags"]:
                flags.append("-Wno-error=ignored-optimization-argument")
                return (flags, None, None)
            if name == "ldflags":
                flags.append("-flto")
                return (flags, None, None)
        return (flags, None, None)

    def setup_build_environment(self, env):
        # This sets the compiler (and flags) that distutils will use
        # to create the final shared library.  It will use the
        # compiler specified by the environment variable 'CC' for all
        # other compilation.  We are setting 'LDSHARED' to the
        # spack compiler wrapper plus a few extra flags necessary for
        # building the shared library.
        if not sys.platform == "darwin":
            env.set("LDSHARED", "{0} -shared -pthread".format(spack_cc))
