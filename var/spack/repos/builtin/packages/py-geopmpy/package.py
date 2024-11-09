# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeopmpy(PythonPackage):
    """The Global Extensible Open Power Manager (GEOPM) Service provides a
    user interface for accessing hardware telemetry and settings securely."""

    homepage = "https://geopm.github.io"
    git = "https://github.com/geopm/geopm.git"
    url = "https://github.com/geopm/geopm/tarball/v3.1.0"

    maintainers("bgeltz", "cmcantalupo")
    license("BSD-3-Clause")
    tags = ["e4s"]

    version("develop", branch="dev", get_full_repo=True)
    version("3.1.0", sha256="2d890cad906fd2008dc57f4e06537695d4a027e1dc1ed92feed4d81bb1a1449e")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-setuptools@53.0.0:", type="build")
    depends_on("py-setuptools-scm@7.0.3:", when="@3.1:", type="build")
    depends_on("py-build@0.9.0:", when="@3.1:", type="build")
    depends_on("py-cffi@1.14.5:", type="run")
    depends_on("py-natsort@8.2.0:", type="run")
    depends_on("py-numpy@1.19.5:", type="run")
    depends_on("py-pandas@1.1.5:", type="run")
    depends_on("py-tables@3.7.0:", type="run")
    depends_on("py-psutil@5.8.0:", type="run")
    depends_on("py-pyyaml@6.0:", type="run")
    depends_on("py-docutils@0.18:", type="run")

    build_directory = "geopmpy"

    def setup_build_environment(self, env):
        if not self.spec.version.isdevelop():
            env.set("SETUPTOOLS_SCM_PRETEND_VERSION", self.version)
