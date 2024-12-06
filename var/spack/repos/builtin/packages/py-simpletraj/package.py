# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySimpletraj(PythonPackage):
    """Lightweight coordinate-only trajectory reader based on code
    from GROMACS, MDAnalysis and VMD."""

    pypi = "simpletraj/simpletraj-0.5.tar.gz"

    maintainers("d-beltran")

    # Versions
    version("0.5", sha256="860ccba82e7a6085ef1cbff74eb2db53df65fd58edabae3c45b8c45a219b8a3b")

    depends_on("c", type="build")  # generated

    # Dependencies
    depends_on("py-setuptools", type="build")
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
