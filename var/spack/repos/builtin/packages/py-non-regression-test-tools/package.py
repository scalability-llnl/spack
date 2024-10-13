# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNonRegressionTestTools(PythonPackage):
    """non regression test tools."""

    homepage = "https://gitlab.com/Te_ch/non-regression-test-tools"
    git = "https://gitlab.com/Te_ch/non-regression-test-tools.git"

    maintainers("tech-91")

    license("GPL-2.0-or-later")

    version("develop", branch="develop")
    version("main", branch="main")
    version("1.0.2", tag="v1.0.2", preferred=True)

    depends_on("py-numpy", type="run")
    depends_on("python@3.7:", type="run")
    depends_on("py-setuptools", type="build")
