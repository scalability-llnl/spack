# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyUbiquerg(PythonPackage):
    """Tools for work (erg) everywhere (ubique)."""

    homepage = "https://github.com/pepkit/ubiquerg"
    pypi = "ubiquerg/ubiquerg-0.6.2.tar.gz"

    license("BSD-2-Clause")

    version("0.6.2", sha256="a9b1388799d4c366f956e0c912819099ad8f6cd0e5d890923cdde197f80d14cf")

    depends_on("py-setuptools", type="build")
