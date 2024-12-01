# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyReportlab(PythonPackage):
    """The ReportLab Toolkit. An Open Source Python library for generating
    PDFs and graphics."""

    homepage = "https://www.reportlab.com"
    pypi = "reportlab/reportlab-3.4.0.tar.gz"

    version("4.0.4", sha256="7f70b3b56aff5f11cb4136c51a0f5a56fe6e4c8fbbac7b903076db99a8ef31c1")
    version("3.6.12", sha256="b13cebf4e397bba14542bcd023338b6ff2c151a3a12aabca89eecbf972cb361a")
    version("3.4.0", sha256="5beaf35e59dfd5ebd814fdefd76908292e818c982bd7332b5d347dfd2f01c343")

    depends_on("python@3.7:3", when="@3.6.9:", type=("build", "run"))
    # version restictions were taken over from release 3.4.0 setup.py
    depends_on("py-setuptools@2.2:", type="build")
    depends_on("py-pip@1.4.1:", type="build")
    depends_on("pil@9:", when="@3.6.10:", type=("build", "run"))
    depends_on("pil@2.4.0:", type=("build", "run"))
    depends_on("freetype")

    @when("@:3")
    def patch(self):
        filter_file(
            "[FREETYPE_PATHS]",
            "[FREETYPE_PATHS]\n"
            + "lib={}\n".format(self.spec["freetype"].libs.directories[0])
            + "inc={}\n".format(self.spec["freetype"].headers.directories[0]),
            "setup.cfg",
            string=True,
        )
