# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Grads(AutotoolsPackage):
    """The Grid Analysis and Display System (GrADS) is an interactive
    desktop tool that is used for easy access, manipulation, and visualization
    of earth science data. GrADS has two data models for handling gridded and
    station data. GrADS supports many data file formats, including
    binary (stream or sequential), GRIB (version 1 and 2), NetCDF,
    HDF (version 4 and 5), and BUFR (for station data)."""

    homepage = "http://cola.gmu.edu/grads/grads.php"

    maintainers("vanderwb")

    license("GPL-2.0-or-later")

    version("2.2.3", sha256="2cbb67284fe64763c589ecaf08d5bd31144554dfd82a1fccf71e1cc424695a9e")
    version("2.2.2", sha256="1b5a600d4d407ffcf2fbbbba42037a6e1ebfdb8246ba56b93c628e3c472b4ded")
    version("2.2.1", sha256="695e2066d7d131720d598bac0beb61ac3ae5578240a5437401dc0ffbbe516206")

    depends_on("c", type="build")  # generated

    variant("geotiff", default=True, description="Enable GeoTIFF support")
    variant("shapefile", default=True, description="Enable Shapefile support")
    variant("grib2", default=True, description="Enable GRIB2 support")
    variant("dap", default=False, description="Enable DAP support")

    # TODO: This variant depends on the "simple X" library, which is no longer available
    # from any trusted source. Revisit if this changes.
    # variant("gui", default=False, description="Enable graphical user interface")

    # These variants are broken in 2.2.1
    # See https://github.com/j-m-adams/GrADS/issues/2
    variant("hdf5", default=True, when="@2.2.2:", description="Enable HDF5 support")
    variant("hdf4", default=True, when="@2.2.2:", description="Enable HDF4 support")
    variant("netcdf", default=True, when="@2.2.2:", description="Enable NetCDF support")

    depends_on("hdf5@:1.10", when="+hdf5")
    depends_on("hdf", when="+hdf4")
    depends_on("netcdf-c", when="+netcdf")
    depends_on("g2c", when="+grib2")
    depends_on("libgeotiff", when="+geotiff")
    depends_on("shapelib", when="+shapefile")
    depends_on("gadap", when="+dap")
    depends_on("udunits")
    depends_on("libgd")
    depends_on("libxmu")
    depends_on("cairo +X +pdf +fc +ft")
    depends_on("readline")
    depends_on("pkgconfig", type="build")

    # The project is hosted on GitHub for versions 2.2.2 and later
    def url_for_version(self, version):
        if version >= Version("2.2.2"):
            url = "https://github.com/j-m-adams/GrADS/archive/refs/tags/v{}.tar.gz"
            return url.format(version)
        else:
            url = "ftp://cola.gmu.edu/grads/{}/grads-{}-src.tar.gz"
            return url.format(version.up_to(2), version)

    # Name of grib2 C library has changed in recent versions
    def patch(self):
        if self.spec.satisfies("@:2.2.2"):
            filter_file("png15", "png", "configure")

        if self.spec.satisfies("+grib2"):
            filter_file("grib2c", "g2c", "configure")
            if self.spec.satisfies("^g2c@1.8.0:"):
                filter_file("G2_VERSION", "G2C_VERSION", "src/gacfg.c")

    def setup_build_environment(self, env):
        env.set("SUPPLIBS", "/")

        # Recent versions configure scripts break without PKG_CONFIG set
        env.set("PKG_CONFIG", self.spec["pkgconfig"].prefix.bin.join("pkg-config"))

        if "+hdf4" in self.spec and "~shared" in self.spec["hdf"]:
            env.set("LIBS", self.spec["hdf:transitive"].libs)

    def setup_run_environment(self, env):
        env.set("GADDIR", self.prefix.data)

    @run_after("install")
    def copy_data(self):
        with working_dir(self.build_directory):
            install_tree("data", self.prefix.data)
        with working_dir(self.package_dir):
            install("udpt", self.prefix.data)
            filter_file(r"({lib})", self.prefix.lib, self.prefix.data.udpt)

    def configure_args(self):
        args = []
        args.extend(self.with_or_without("geotiff"))
        args.extend(self.with_or_without("hdf4"))
        args.extend(self.with_or_without("hdf5"))
        args.extend(self.with_or_without("netcdf"))
        args.extend(self.with_or_without("gadap", variant="dap"))

        return args
