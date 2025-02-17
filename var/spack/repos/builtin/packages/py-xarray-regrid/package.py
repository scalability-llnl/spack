# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXarrayRegrid(PythonPackage):
    """Regridding utility for xarray"""

    homepage = "https://github.com/xarray-contrib/xarray-regrid"
    pypi = "xarray_regrid/xarray_regrid-0.4.0.tar.gz"

    maintainers("Chrismarsh")

    license("Apache-2.0", checked_by="Chrismarsh")

    version("0.4.0", sha256="f0bef6a346e247c657ed293752b5685f3b559b32de546889ca9e9fca14b81f3a")

    depends_on("py-hatchling", type="build")

    depends_on("python@3.10:", type=("build", "run"))

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-xarray", type=("build", "run"))
    depends_on("py-flox", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
