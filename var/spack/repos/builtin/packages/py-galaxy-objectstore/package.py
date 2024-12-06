# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGalaxyObjectstore(PythonPackage):
    """The Galaxy object store framework and default implementations."""

    homepage = "https://github.com/galaxyproject/galaxy"
    pypi = "galaxy-objectstore/galaxy-objectstore-22.1.1.tar.gz"

    license("CC-BY-3.0")

    version("22.1.1", sha256="321a70f8bce89fec8d0322ba5821ee0b26d5cd3170a8dc9b7278cd383a9e88dd")

    depends_on("py-setuptools", type="build")

    depends_on("py-galaxy-util", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
