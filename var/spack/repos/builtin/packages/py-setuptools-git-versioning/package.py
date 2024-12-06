# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySetuptoolsGitVersioning(PythonPackage):
    """Use git repo data for building a version number according PEP-440"""

    homepage = "https://setuptools-git-versioning.readthedocs.io/"
    pypi = "setuptools-git-versioning/setuptools-git-versioning-1.13.3.tar.gz"

    maintainers("angus-g")

    license("MIT")

    version("1.13.3", sha256="9dfc59a31dcadcae04bcddc50534ccfc07a25a3180ab5cc1b1e3730217971c63")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("git")
    depends_on("py-toml@0.10.2:", when="^python@:3.10", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
