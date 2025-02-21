# Copyright Spack Project Developers. See COPYRIGHT file for details.
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
    version("1.1.6", tag="v1.1.6")
    version("1.1.4", tag="v1.1.4")

    depends_on("py-numpy", type="run")
    depends_on("python@3.10:", type="run")
    depends_on("py-setuptools@61:", type="build")
