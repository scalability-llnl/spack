# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRobocrys(PythonPackage):
    """Robocrystallographer is a tool to generate text descriptions of crystal
    structures. Similar to how a real-life crystallographer would analyse a
    structure, robocrystallographer looks at the symmetry, local environment, and
    extended connectivity when generating a description. The package includes
    utilities for identifying molecule names, component orientations, heterostructure
    information, and more."""

    homepage = "https://github.com/hackingmaterials/robocrystallographer"
    pypi = "robocrys/robocrys-0.2.7.tar.gz"

    maintainers("meyersbs")

    version("0.2.7", sha256="c8155bbc13efbf66ce0a834ebd0eaba9102f2c405a9cbaac071aa230d81ee5f6")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-spglib", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-inflect", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))
    depends_on("py-matminer", type=("build", "run"))
    depends_on("py-monty", type=("build", "run"))
    depends_on("py-pubchempy", type=("build", "run"))
    depends_on("py-pybtex", type=("build", "run"))
    depends_on("py-ruamel-yaml", type=("build", "run"))
    depends_on("py-pymatgen@2020.10.20:", type=("build", "run"))
