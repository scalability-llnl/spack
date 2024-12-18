# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJcb(PythonPackage):
    """
    JEDI Configuration Builder
    """

    homepage = "https://github.com/NOAA-EMC/jcb"
    git = "https://github.com/NOAA-EMC/jcb"

    maintainers("danholdaway", "CoryMartin-NOAA", "AlexanderRichert-NOAA")

    license("GPL-3.0-only", checked_by="AlexanderRichert-NOAA")

    version("develop", branch="develop", commit="16399323e36df6f17bfd4740a2330ca7fae31537")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-pyyaml@6:", type=("build", "run"))
    depends_on("py-jinja2@3.1.2:", type=("build", "run"))
    depends_on("py-click@8:", type=("build", "run"))

    depends_on("py-pytest@7:", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check(self):
        env["PYTHONPATH"] = ":".join(
            (join_path(self.build_directory, "build/lib"), env["PYTHONPATH"])
        )
        pytest = which(join_path(self.spec["py-pytest"].prefix.bin, "pytest"))
        pytest("-v", self.build_directory)
