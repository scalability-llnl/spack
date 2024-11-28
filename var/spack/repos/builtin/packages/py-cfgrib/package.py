# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCfgrib(PythonPackage):
    """Python interface to map GRIB files to the NetCDF Common Data Model
    following the CF Convention using ecCodes."""

    homepage = "https://github.com/ecmwf/cfgrib"
    pypi = "cfgrib/cfgrib-0.9.8.5.tar.gz"

    license("Apache-2.0")

    version("0.9.14.1", sha256="a6e66e8a3d8f9823d3eef0c2c6ebca602d5bcc324f0baf4f3d13f68b0b40501e")
    version("0.9.10.4", sha256="b490078192aa13ec89c77296110355521442325866b16a996f4b3cf421542909")
    version("0.9.9.0", sha256="6ff0227df9c5ee34aa7d6ab1f7af3fbe6838523a8a9891c74040b419b03ad289")
    version("0.9.8.5", sha256="07c224d7ac823a1df5738b96b9d3621515538f51f67e55044f9cc8ec1668e1bd")

    # Warning: can create infinite dependency loop with xarray+io ^cfgrib+xarray
    variant("xarray", default=False, description="Add xarray support")

    depends_on("py-setuptools", type="build")
    depends_on("py-attrs@19.2:", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-eccodes@0.9.8:", when="@0.9.10:", type=("build", "run"))
    depends_on("py-eccodes", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))

    # 0.9.14.1 enables support for xarray @2024.09.0:
    # https://github.com/ecmwf/cfgrib/commit/46a79025146b3847e81629748fc3fe16e56097cf
    depends_on("py-xarray@0.15:", when="@0.9.14.1:+xarray", type=("build", "run"))
    depends_on("py-xarray@0.15:2024.08.0", when="@0.9.10:0.9.14.0+xarray", type=("build", "run"))
    depends_on("py-xarray@0.12:2024.08.0", when="@:0.9.14.0+xarray", type=("build", "run"))

    # Historical dependencies
    depends_on("py-pytest-runner", when="@0.9.8.5", type="build")
    depends_on("py-cffi", when="@0.9.8.5", type=("build", "run"))

    @property
    def import_modules(self):
        modules = ["cfgrib"]

        if "+xarray" in self.spec:
            modules.append("cf2cdm")

        return modules
