# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class SagaGis(AutotoolsPackage, SourceforgePackage):
    """
    SAGA is a GIS for Automated Geoscientific Analyses and has been designed
    for an easy and effective implementation of spatial algorithms. It offers
    a comprehensive, growing set of geoscientific methods and provides an
    easily approachable user interface with many visualisation options
    """

    homepage = "http://saga-gis.org/"
    sourceforge_mirror_path = "SAGA%20-%205.0.0/saga-5.0.0.tar.gz"
    git = "git://git.code.sf.net/p/saga-gis/code"

    license("GPL-2.0-or-later")

    version("develop", branch="master")
    version("7.4.0", branch="release-7.4.0")
    version("7.3.0", branch="release-7.3.0")
    version("7.1.1", branch="release-7.1.1")
    version("7.1.0", branch="release-7.1.0")
    version("7.0.0", branch="release-7.0.0")
    version("6.4.0", branch="release-6.4.0")
    version("6.3.0", branch="release-6.3.0")
    version("6.2.0", branch="release-6.2.0")
    version("6.1.0", branch="release-6.1.0")
    version("6.0.0", branch="release-6.0.0")
    version("5.0.1", branch="release-5-0-1")
    version("5.0.0", branch="release-5.0.0")
    version("4.1.0", branch="release-4.1.0")
    version("4.0.0", branch="release-4.0.0")
    version("3.0.0", branch="release-3.0.0", deprecated=True)
    version("2.3-lts", branch="release-2-3-lts", deprecated=True)
    version("2.3.1", branch="release-2-3-1", deprecated=True)
    version("2.3.0", branch="release-2-3-0", deprecated=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("gui", default=True, description="Build GUI and interactive SAGA tools")
    variant("odbc", default=True, description="Build with ODBC support")

    # FIXME Saga-gis configure file disables triangle even if
    # --enable-triangle flag is used
    # variant('triangle', default=True,   description='Build with triangle.c

    # non free for commercial use otherwise use qhull')
    variant(
        "libfire", default=True, description="Build with libfire (non free for commercial usage)"
    )
    variant("openmp", default=True, description="Build with OpenMP enabled")
    variant("python", default=False, description="Build Python extension")

    variant("postgresql", default=False, description="Build with PostgreSQL library")
    variant("opencv", default=False, description="Build with libraries using OpenCV")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("libsm", type="link")

    depends_on("libharu")
    depends_on("wxwidgets")
    depends_on("postgresql", when="+postgresql")
    depends_on("unixodbc", when="+odbc")

    # SAGA-GIS requires projects.h from proj
    depends_on("proj")
    # https://sourceforge.net/p/saga-gis/bugs/271/
    depends_on("proj@:5", when="@:7.3")

    # Saga-Gis depends on legacy opencv API removed in opencv 4.x
    depends_on("opencv@:3.4.6+jpeg+video+objdetect+ml+openmp+photo", when="+opencv")
    depends_on("jpeg", when="+opencv")
    # Set hl variant due to similar issue #7145
    depends_on("hdf5+hl")

    # write support for grib2 is available since 2.3.0 (https://gdal.org/drivers/raster/grib.html)
    depends_on("gdal@2.3:+grib+hdf5+netcdf")

    depends_on("gdal@2.3:2.4+grib+hdf5+netcdf", when="@:7.2")
    depends_on("libgeotiff@:1.4", when="@:7.2")

    # FIXME Saga-Gis uses a wrong include path
    # depends_on('qhull', when='~triangle')

    depends_on("swig", type="build", when="+python")
    extends("python", when="+python")

    configure_directory = "saga-gis"

    def patch(self):
        if "+opencv" in self.spec:
            opencv_dir = self.spec["opencv"].prefix
            opencv_makefile = join_path(
                "saga-gis", "src", "tools", "imagery", "imagery_opencv", "Makefile.am"
            )

            filter_file(r"/usr(/include/opencv)", r"{0}\1".format(opencv_dir), opencv_makefile)

    def configure_args(self):
        args = []
        args += self.enable_or_disable("gui")
        args += self.enable_or_disable("odbc")
        # FIXME Saga-gis configure file disables triangle even if
        # --enable-triangle flag is used
        # args += self.enable_or_disable('triangle')
        # FIXME SAGA-GIS uses a wrong include path
        # if '~triangle' in self.spec:
        #    args.append('--disable-triangle')
        args += self.enable_or_disable("libfire")
        args += self.enable_or_disable("openmp")
        args += self.enable_or_disable("python")
        args += self.with_or_without("postgresql")

        return args

    def setup_run_environment(self, env):
        # Point saga to its tool set, will be loaded during runtime
        env.set("SAGA_MLB", self.prefix.lib.saga)
        env.set("SAGA_TLB", self.prefix.lib.saga)
