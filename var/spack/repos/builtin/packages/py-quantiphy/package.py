# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQuantiphy(PythonPackage):
    """physical quantities (numbers with units)"""

    homepage = "https://quantiphy.readthedocs.io"
    pypi = "quantiphy/quantiphy-2.20.tar.gz"

    maintainers("ax3l")

    license("MIT", checked_by="ax3l")

    version("2.20", sha256="ba5375ac55c3b90077a793588dd5a88aaf81b2c3b0fc9c9359513ac39f6ed84d")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-flit-core@2:3", type=("build"))
