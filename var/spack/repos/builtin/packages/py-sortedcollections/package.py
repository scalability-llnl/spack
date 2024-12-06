# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySortedcollections(PythonPackage):
    """Sorted Collections is an Apache2 licensed Python sorted collections library."""

    homepage = "http://www.grantjenks.com/docs/sortedcollections/"
    pypi = "sortedcollections/sortedcollections-1.2.1.tar.gz"

    license("Apache-2.0")

    version("1.2.1", sha256="58c31f35e3d052ada6a1fbfc235a408e9ec5e2cfc64a02731cf97cac4afd306a")

    depends_on("py-setuptools", type="build")
    depends_on("py-sortedcontainers", type=("build", "run"))
