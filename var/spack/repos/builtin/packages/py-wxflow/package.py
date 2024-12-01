# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWxflow(PythonPackage):
    """
    Common set of tools used in weather workflows.
    See https://wxflow.readthedocs.io/en/latest/ for documentation.
    """

    homepage = "https://github.com/NOAA-EMC/wxflow"
    pypi = "wxflow/wxflow-0.1.0.tar.gz"

    maintainers("aerorahul", "WalterKolczynski-NOAA", "AlexanderRichert-NOAA")

    license("LGPL-3.0-only", checked_by="AlexanderRichert-NOAA")

    version("0.2.0", sha256="a0fa903c6bb65e2cfa9deebcc8ec03d8eced82eac54288e73bd9137fcc0457d4")
    version("0.1.0", sha256="4de120688affd7589bd9df0288139d16e97a93bc37efcfaf09fccc1c6ed43ab1")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@1.21.6:", type=("build", "run"))
    depends_on("py-pyyaml@6:", type=("build", "run"))
    depends_on("py-jinja2@3.1.2:", type=("build", "run"))

    depends_on("py-pytest", type="test")

    @on_package_attributes(run_tests=True)
    def patch(self):
        # Disable code coverage generation
        filter_file(r"\s\-\-cov[^\s]+", "", "setup.cfg")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check(self):
        env["PYTHONPATH"] = ":".join(
            (join_path(self.build_directory, "build/lib"), env["PYTHONPATH"])
        )
        pytest = which(join_path(self.spec["py-pytest"].prefix.bin, "pytest"))
        pytest("-v", self.build_directory)
