# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygmt(PythonPackage):
    """A Python interface for the Generic Mapping Tools."""

    homepage = "https://github.com/GenericMappingTools/pygmt"
    pypi = "pygmt/pygmt-0.9.0.tar.gz"

    maintainers("snehring")

    license("BSD-3-Clause", checked_by="snehring")

    version("0.9.0", sha256="1090be7a3745e982af130a0289b9ceb60289b9c2c50fc2e0f681004ed7a1a20e")

    depends_on("python@3.9:3", type=("build", "run"))

    depends_on("py-setuptools@64:", type="build")
    depends_on("py-setuptools-scm@6.2:", type="build")

    depends_on("py-numpy@1.21:", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-xarray", type=("build", "run"))
    depends_on("py-netcdf4", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("gmt@6.3.0:+graphicsmagick", type=("build", "run"))
