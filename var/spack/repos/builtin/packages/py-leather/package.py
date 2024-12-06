# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLeather(PythonPackage):
    """Leather is the Python charting library for those who need charts now and
    don't care if they're perfect."""

    homepage = "https://leather.readthedocs.io/en/stable/"
    pypi = "leather/leather-0.3.3.tar.gz"

    license("MIT")

    version("0.3.3", sha256="076d1603b5281488285718ce1a5ce78cf1027fe1e76adf9c548caf83c519b988")

    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.6.1:", type=("build", "run"))
