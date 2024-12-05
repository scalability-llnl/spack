# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGalaxyToolUtil(PythonPackage):
    """The Galaxy tool utilities."""

    homepage = "https://github.com/galaxyproject/galaxy"
    pypi = "galaxy-tool-util/galaxy-tool-util-22.1.5.tar.gz"

    license("CC-BY-3.0")

    version("22.1.5", sha256="60e0372f16255c5c11ec5c49dff432ed3beb97123d026f463cf633bc605c0112")

    depends_on("py-setuptools", type="build")

    depends_on("py-galaxy-util@22.1:", type=("build", "run"))
    depends_on("py-galaxy-containers@22.1:", type=("build", "run"))
    depends_on("py-lxml", type=("build", "run"))
    depends_on("py-pydantic", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-sortedcontainers", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
