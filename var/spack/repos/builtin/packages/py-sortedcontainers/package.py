# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySortedcontainers(PythonPackage):
    """Sorted Containers is an Apache2 licensed sorted collections library,
    written in pure-Python, and fast as C-extensions."""

    homepage = "http://www.grantjenks.com/docs/sortedcontainers/"
    pypi = "sortedcontainers/sortedcontainers-2.1.0.tar.gz"

    license("Apache-2.0")

    version("2.4.0", sha256="25caa5a06cc30b6b83d11423433f65d1f9d76c4c6a0c90e3379eaa43b9bfdb88")
    version("2.1.0", sha256="974e9a32f56b17c1bac2aebd9dcf197f3eb9cd30553c5852a3187ad162e1a03a")

    depends_on("py-setuptools", type="build")
