# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyugrid(PythonPackage):
    """Work with triangular unstructured grids and the data on them."""

    homepage = "https://github.com/pyugrid/pyugrid"
    pypi = "pyugrid/pyugrid-0.3.1.tar.gz"

    version("0.3.1", sha256="eddadc1e88c0e801f780b1e6f636fbfc00e3d14cdab82b43300fde0918310053")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-netcdf4", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
