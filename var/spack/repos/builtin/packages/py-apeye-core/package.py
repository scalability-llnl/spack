# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyApeyeCore(PythonPackage):
    """Core (offline) functionality for the apeye library."""

    homepage = "https://github.com/domdfcoding/apeye-core"
    pypi = "apeye_core/apeye_core-1.1.4.tar.gz"

    license("BSD-3-Clause")

    version("1.1.4", sha256="72bb89fed3baa647cb81aa28e1d851787edcbf9573853b5d2b5f87c02f50eaf5")

    depends_on("py-hatch-requirements-txt", type="build")
    depends_on("py-hatchling", type="build")
    depends_on("py-domdf-python-tools@2.6:", type=("build", "run"))
    depends_on("py-idna@2.5:", type=("build", "run"))
