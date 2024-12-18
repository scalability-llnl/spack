# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPynio(PythonPackage):
    """PyNIO ("pie-nee-oh") is a Python module that allows read and/or
    write access to a variety of scientific data formats popular in
    climate and weather"""

    homepage = "https://www.pyngl.ucar.edu/Nio.shtml"
    url = "https://github.com/NCAR/pynio/archive/1.5.4.tar.gz"

    license("Apache-2.0")

    version("1.5.4", sha256="e5bb57d902740d25e4781a9f89e888149f55f2ffe60f9a5ad71069f017c89e1a")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("hdf5", default=False, description="Include HDF5 support")
    variant("gdal", default=False, description="Include GDAL support")

    # The setup.py claims it requires these abolutely.
    depends_on("libpng")
    depends_on("jpeg")
    depends_on("zlib-api")

    # Spack does not currently have netcdf below 4.x, and 3.x is a
    # fundamentally different format. So, currently this is only providing
    # support for netcdf4.
    depends_on("netcdf-c@3.6.0:")

    # Turning on the hdf (i.e. hdf4) dependency causes it not to build, with
    # compile errors that (weirdly) relate to the declarations of HDF5.
    # Very odd, so I have put it in as a comment, for some brave soul to take
    # on later.
    # depends_on('hdf', when='+hdf4')

    # This one works, though.
    depends_on("hdf5", when="+hdf5")

    # Turning on the GDAL dependency apparently forces it to link with
    # -ljasper, meaning that really it depends on gdal+jasper. In my view
    # it should not need this unless one were specifically using PyNio to
    # use GDAL to read JPEG-2000 files, but it seems to be hard-wired
    # in PyNio's setup.py.
    depends_on("gdal+jasper", when="+gdal")

    # I have left off a few other optional dependencies, as they are not yet
    # in Spack. HDFEOS, HDFEOS5, GRIB. See the pynio setup.py for details.

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))

    def setup_build_environment(self, env):
        """
        These environment variables are how the setup.py knows which options
        to turn on, and how to find them.
        """
        env.set("F2CLIBS", "gfortran")
        env.set("HAS_NETCDF4", "1")
        env.set("NETCDF4_PREFIX", self.spec["netcdf-c"].prefix)
        if "+hdf5" in self.spec:
            env.set("HAS_HDF5", "1")
            env.set("HDF5_PREFIX", self.spec["hdf5"].prefix)
        if "+gdal" in self.spec:
            env.set("HAS_GDAL", "1")
            env.set("GDAL_PREFIX", self.spec["gdal"].prefix)


#        This one is trouble - see comments above.
#        if '+hdf4' in self.spec:
#            env.set('HAS_HDF4', '1')
#            env.set('HDF4_PREFIX', self.spec['hdf'].prefix)
