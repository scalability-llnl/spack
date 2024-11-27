# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArmPyart(PythonPackage):
    """Python ARM Radar Toolkit.

    A growing collection of weather radar algorithms and utilities build on top
    of the Scientific Python stack and distributed under the 3-Clause BSD
    license. Py-ART is used by the Atmospheric Radiation Measurement (ARM)
    Climate Research Facility for working with data from a number of
    precipitation and cloud radars, but has been designed so that it can be
    used by others in the radar and atmospheric communities to examine,
    processes, and analyse data from many types of weather radars."""

    homepage = "https://github.com/ARM-DOE/pyart"
    pypi = "arm_pyart/arm_pyart-1.12.7.tar.gz"

    version("1.12.7", sha256="b7b23ecef270c60b017d94603941f0c117de072a10125c5f58c0685d801f9161")

    depends_on("c", type="build")  # generated

    variant("cartopy", description="Plot grids on maps", default=False)
    variant("cylp", description="Linear programming solver", default=False)
    variant("gdal", description="Output GeoTIFFs from grid objects", default=False)
    variant("hdf5", description="Support for HDF5 files", default=False)
    variant("rsl", description="Use RSL library", default=False)
    variant("wradlib", description="Calculate texture of differential phase field", default=False)

    conflicts("~hdf5", when="+wradlib")
    conflicts("~gdal", when="+wradlib")

    depends_on("python@3.6:3.10", type=("build", "run"))

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm@6.2:", type="build")

    depends_on("py-cython", type="build")
    depends_on("py-numpy", type=("build", "run"))
    # https://github.com/ARM-DOE/pyart/issues/1550
    depends_on("py-numpy@:1", when="@:1.18.1", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-netcdf4", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-pooch", type=("build", "run"))
    depends_on("py-cftime", type=("build", "run"))
    depends_on("py-fsspec", type=("build", "run"))
    depends_on("py-s3fs", type=("build", "run"))
    depends_on("py-xarray@0.21.1:", type=("build", "run"))

    # These are not listed but needed due to being imported in a python file
    depends_on("py-pandas", type="run")
    depends_on("py-pylab-sdk", type="run")

    # Dependencies for variants
    depends_on("py-cartopy", type="run", when="+cartopy")
    depends_on("py-cylp", type="run", when="+cylp")
    depends_on("gdal+python", type="run", when="+gdal")
    depends_on("py-h5py", type="run", when="+hdf5")
    depends_on("rsl", type=("build", "run"), when="+rsl")
    depends_on("py-wradlib", type="run", when="+wradlib")

    patch("StringIO.patch")

    def setup_build_environment(self, env):
        if "+rsl" in self.spec:
            env.set("RSL_PATH", self.spec["rsl"].prefix)
        else:
            # set RSL_PATH to empty to make sure RSL is not picked up from a
            # non-spack install in /usr/local
            env.set("RSL_PATH", "")
