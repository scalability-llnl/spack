# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNumdifftools(PythonPackage):
    """Solves automatic numerical differentiation problems in one or more
    variables."""

    homepage = "https://github.com/pbrod/numdifftools"
    pypi = "numdifftools/numdifftools-0.9.41.tar.gz"

    version("0.9.41", sha256="4ef705cd3c06211b3a4e9fd05ad622be916dcfda40732f0128805a2c4be389b4")

    depends_on("python@3.7:", type=("build", "run"))

    depends_on("py-setuptools@39.2:", type="build")
    depends_on("py-numpy@1.9:", type=("build", "run"))
    depends_on("py-scipy@0.8:", type=("build", "run"))
