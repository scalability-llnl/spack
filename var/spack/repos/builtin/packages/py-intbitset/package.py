# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyIntbitset(PythonPackage):
    """The intbitset library provides a set implementation to store sorted
    unsigned integers either 32-bits integers or an infinite range with fast
    set operations implemented via bit vectors in a Python C extension for
    speed and reduced memory usage."""

    homepage = "https://github.com/inveniosoftware/intbitset"
    pypi = "intbitset/intbitset-3.0.1.tar.gz"

    license("LGPL-3.0-or-later")

    version("3.0.1", sha256="f1e6d03c6729922a223c51849df65b9e916e625aefb911784e7f9acd4c207d53")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
