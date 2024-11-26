# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParmed(PythonPackage):
    """ParmEd is a general tool for aiding in investigations of
    biomolecular systems using popular molecular simulation
    packages, like Amber, CHARMM, and OpenMM written in
    Python."""

    homepage = "https://parmed.github.io/ParmEd/html/index.html"
    pypi = "ParmEd/ParmEd-3.4.3.tar.gz"

    license("MIT")

    version("3.4.3", sha256="90afb155e3ffe69230a002922b28968464126d4450059f0bd97ceca679c6627c")

    depends_on("cxx", type="build")  # generated

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
