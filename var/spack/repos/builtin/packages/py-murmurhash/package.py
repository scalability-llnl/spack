# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMurmurhash(PythonPackage):
    """Cython bindings for MurmurHash."""

    homepage = "https://github.com/explosion/murmurhash"
    pypi = "murmurhash/murmurhash-1.0.2.tar.gz"

    license("MIT")

    version("1.0.2", sha256="c7a646f6b07b033642b4f52ae2e45efd8b80780b3b90e8092a0cec935fbf81e2")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-wheel@0.32.0:0.32", type="build")
