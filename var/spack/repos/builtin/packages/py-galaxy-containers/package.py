# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGalaxyContainers(PythonPackage):
    """The Galaxy containers module - interfaces for modeling and interacting
    with container backends (docker and docker swarm currently).
    """

    homepage = "https://github.com/galaxyproject/galaxy"
    pypi = "galaxy-containers/galaxy-containers-22.1.1.tar.gz"

    license("CC-BY-3.0")

    version("22.1.1", sha256="41e0003b18e580175d443cf21e9c2d2eb21a265c012164f7255cdb0c03a76334")

    depends_on("py-setuptools", type="build")

    depends_on("py-galaxy-util", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
