# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDxchange(PythonPackage):
    """DXchange provides an interface with tomoPy and raw tomographic data
    collected at different synchrotron facilities."""

    homepage = "https://github.com/data-exchange/dxchange"
    url = "https://github.com/data-exchange/dxchange/archive/v0.1.2.tar.gz"

    version("0.1.2", sha256="d005b036b6323d0dffd5944c3da0b8a90496d96277654e72b53717058dd5fd87")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-netcdf4", type=("build", "run"))
    depends_on("py-spefile", type=("build", "run"))
    depends_on("py-edffile", type=("build", "run"))
    depends_on("py-tifffile", type=("build", "run"))
    depends_on("py-dxfile", type=("build", "run"))
    depends_on("py-olefile", type=("build", "run"))
    depends_on("py-astropy", type=("build", "run"))
