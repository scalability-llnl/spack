# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyepsg(PythonPackage):
    """Provides simple access to https://epsg.io/."""

    homepage = "https://pyepsg.readthedocs.io/en/latest/"
    pypi = "pyepsg/pyepsg-0.3.2.tar.gz"

    license("LGPL-3.0-or-later")

    version("0.4.0", sha256="2d08fad1e7a8b47a90a4e43da485ba95705923425aefc4e2a3efa540dbd470d7")
    version("0.3.2", sha256="597ef8c0e8c1be3db8f68c5985bcfbbc32e22f087e93e81ceb03ff094898e059")

    depends_on("py-setuptools", type="build")
    depends_on("py-requests", type=("build", "run"))
