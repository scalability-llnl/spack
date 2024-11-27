# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFastrlock(PythonPackage):
    """This is a C-level implementation of a fast, re-entrant,
    optimistic lock for CPython."""

    homepage = "https://github.com/scoder/fastrlock"
    pypi = "fastrlock/fastrlock-0.5.tar.gz"

    license("MIT")

    version("0.8.1", sha256="8a5f2f00021c4ac72e4dab910dc1863c0e008a2e7fb5c843933ae9bcfc3d0802")
    version("0.5", sha256="9ae1a31f6e069b5f0f28ba63c594d0c952065de0a375f7b491d21ebaccc5166f")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")
    # in newer pip versions --install-option does not exist
    depends_on("py-pip@:23.0", type="build")

    def install_options(self, spec, prefix):
        return ["--with-cython"]
