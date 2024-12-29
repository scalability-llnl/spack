# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyReferencing(PythonPackage):
    """JSON Referencing + Python."""

    homepage = "https://referencing.readthedocs.io/"
    pypi = "referencing/referencing-0.35.1.tar.gz"

    maintainers("wdconinc")

    license("MIT", checked_by="wdconinc")

    version("0.35.1", sha256="25b42124a6c8b632a425174f24087783efb348a6f1e0008e63cd4466fedf703c")

    depends_on("py-hatchling", type="build")
    depends_on("py-hatch-vcs", type="build")

    depends_on("py-attrs@22.2.0:", type=("build", "run"))
    depends_on("py-rpds-py@0.7.0:", type=("build", "run"))
