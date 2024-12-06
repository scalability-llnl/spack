# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySuperqt(PythonPackage):
    """Missing widgets and components for PyQt/PySide"""

    homepage = "https://pyapp-kit.github.io/superqt/"
    pypi = "superqt/superqt-0.6.1.tar.gz"

    license("BSD-3-Clause", checked_by="A-N-Other")

    version("0.6.1", sha256="f1a9e0499c4bbcef34b6f895eb57cd41301b3799242cd030029238124184dade")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-hatchling", type="build")
    depends_on("py-hatch-vcs", type="build")

    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-pygments@2.4:", type=("build", "run"))
    depends_on("py-qtpy@1.1:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4.3:", type=("build", "run"))

    conflicts("^py-typing-extensions@3.10.0.0")
