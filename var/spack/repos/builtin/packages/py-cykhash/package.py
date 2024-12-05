# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCykhash(PythonPackage):
    """Cython wrapper for khash-sets/maps, efficient implementation of isin and unique."""

    homepage = "https://github.com/realead/cykhash"
    pypi = "cykhash/cykhash-2.0.1.tar.gz"

    maintainers("snehring")

    license("MIT")

    version("2.0.1", sha256="b4794bc9f549114d8cf1d856d9f64e08ff5f246bf043cf369fdb414e9ceb97f7")

    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.28:", type="build")
