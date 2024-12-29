# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySeekpath(PythonPackage):
    """SeeK-path is a python module to obtain band paths in the Brillouin zone of crystal
    structures."""

    homepage = "https://github.com/giovannipizzi/seekpath"
    pypi = "seekpath/seekpath-2.0.1.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version("2.0.1", sha256="188513ee187fbbace49066a29ecea9bbd351f23da3bea33d507d0f590856b082")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-numpy@1.0:", type=("build", "run"))
    depends_on("py-spglib@1.14.1:", type=("build", "run"))
