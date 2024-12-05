# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMonotonic(PythonPackage):
    """An implementation of time.monotonic() for Python 2 & < 3.3"""

    pypi = "monotonic/monotonic-1.6.tar.gz"

    license("Apache-2.0")

    version("1.6", sha256="3a55207bcfed53ddd5c5bae174524062935efed17792e9de2ad0205ce9ad63f7")
    version("1.2", sha256="c0e1ceca563ca6bb30b0fb047ee1002503ae6ad3585fc9c6af37a8f77ec274ba")

    depends_on("py-setuptools", type="build")
