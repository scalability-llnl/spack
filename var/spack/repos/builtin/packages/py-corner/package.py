# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCorner(PythonPackage):
    """Make some beautiful corner plots."""

    homepage = "https://corner.readthedocs.io"
    pypi = "corner/corner-2.2.2.tar.gz"

    maintainers("LydDeb")

    license("BSD-2-Clause")

    version("2.2.2", sha256="4bc79f3b6778c270103f0926e64ef2606c48c3b6f92daf5382fc4babf5d608d1")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools@62.0:", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-matplotlib@2.1:", type=("build", "run"))
