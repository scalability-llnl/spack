# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCdo(PythonPackage):
    """The cdo package provides an interface to the Climate Data
    Operators from Python."""

    pypi = "cdo/cdo-1.3.2.tar.gz"

    maintainers("Try2Code", "skosukhin")

    version("1.5.6", sha256="fec1a75382f01b3c9c368e8f143d98b12323e06975663f87d9b60c739ae1d335")

    depends_on("python@2.7:", type=("build", "run"))

    depends_on("py-setuptools", type="build")
    depends_on("cdo+netcdf", type="run")
    depends_on("py-netcdf4", type=("build", "run"))
    depends_on("py-xarray", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))

    def setup_run_environment(self, env):
        env.set("CDO", self.spec["cdo"].prefix.bin.cdo)
