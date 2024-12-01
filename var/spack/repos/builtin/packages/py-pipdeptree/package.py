# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPipdeptree(PythonPackage):
    """Command line utility to show dependency tree of packages."""

    homepage = "https://github.com/tox-dev/pipdeptree"
    pypi = "pipdeptree/pipdeptree-2.13.0.tar.gz"

    license("MIT")

    version("2.13.0", sha256="ff71a48abd0b1ab810c23734b47de6ebd93270857d6665e21ed5ef6136fcba6e")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-hatch-vcs@0.3:", type="build")
    depends_on("py-hatchling@1.18:", type="build")
