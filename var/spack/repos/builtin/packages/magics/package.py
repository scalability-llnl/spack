# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class Magics(CMakePackage):
    """Magics is the latest generation of the ECMWF's Meteorological plotting
    software MAGICS. Although completely redesigned in C++, it is intended
    to be as backwards-compatible as possible with the Fortran interface."""

    homepage = "https://confluence.ecmwf.int/display/MAGP/Magics"
    url = "https://confluence.ecmwf.int/download/attachments/3473464/Magics-4.2.4-Source.tar.gz?api=v2"
    list_url = "https://confluence.ecmwf.int/display/MAGP/Releases"

    license("Apache-2.0")

    # The policy on which minor releases remain available and which get deleted
    # after a newer version becomes available is unclear.
    version("4.15.3", sha256="1836e1e37534c556f55b5b13812a513091c2fa508b8c4f5a8b6842f07741f1a7")
    version("4.9.3", sha256="c01ee7c4b05c5512e93e573748d2766d299fa1a60c226f2a0d0989f3d7c5239b")
    version("4.4.0", sha256="544058cd334f3e28a16d00ea7811e13cdf282f9c1ebec2ad7868171d925abd24")
    version("4.3.3", sha256="27d3de71cf41f3d557fd85dabaea2baaab34c4c6422a5b5b15071a6a53387601")
    version("4.3.1", sha256="b1995e2f5bf24943715446d1302cc5d7de4cacfe4cee7c3cfd1037ac183cd181")
    version("4.3.0", sha256="f6c0d32c243913e53320dd94ce8e1e6a64bd9a44af77d5ac32c062bc18355b8a")
    version("4.2.6", sha256="9b34a375d9125ab6e8a715b970da2e479f96370bac6a5bb8a015a079ed9e027c")
    version("4.2.4", sha256="920c7dbb1aaabe65a31c6c18010829210f8b2f8d614b6c405dc5a4530e346f07")
    version("4.1.0", sha256="da626c31f53716990754dd72ab7b2f3902a8ad924b23ef3309bd14900d170541")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    conflicts("%gcc@11:", when="@:4.4", msg="missing #include <limits>")

    variant(
        "grib",
        default="eccodes",
        values=("eccodes", "grib-api"),
        description="Specify GRIB backend",
    )
    variant("netcdf", default=False, description="Enable NetCDF support")
    variant("cairo", default=False, description="Enable cairo support[png/jpeg]")
    variant("fortran", default=False, description="Enable Fortran interface")
    variant("metview", default=False, description="Enable metview support")
    variant("qt", default=False, description="Enable metview support with qt")
    variant("bufr", default=False, description="Enable BUFR support")

    variant(
        "build_type",
        default="RelWithDebInfo",
        description="The build type to build",
        values=("Debug", "Release", "RelWithDebInfo", "Production"),
    )

    # Build dependencies
    depends_on("cmake@2.8.11:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("python", type="build")
    depends_on("perl", type="build")
    depends_on("perl-xml-parser", type="build")

    # Non-optional dependencies
    # change of proj4 api starting from version 4.3.0
    # https://github.com/OSGeo/PROJ/wiki/proj.h-adoption-status
    depends_on("proj@:5", when="@:4.2.6")
    depends_on("proj@6:", when="@4.3:")
    depends_on("boost+exception")
    depends_on("expat")

    # Magics (at least up to version 2.34.3) should directly and
    # unconditionally depend on zlib, which is not reflected neither in the
    # installation instructions nor explicitly stated in the cmake script:
    # zlib is pulled as a dependency of png. The dependency on png is formally
    # optional and depends on an unofficial flag ENABLE_PNG, which is
    # redundant, because png is used only when ENABLE_CAIRO=ON. The problem is
    # that files that make calls to png library get compiled and linked
    # unconditionally, which makes png a non-optional dependency (and
    # ENABLE_PNG always has to be set to ON).
    depends_on("zlib-api")
    depends_on("libpng")

    # GRIB support is non-optional, regardless of what the instruction says.
    depends_on("eccodes", when="grib=eccodes")
    depends_on("grib-api", when="grib=grib-api")

    # Even if netcdf is disabled and -DENABLE_NETCDF=OFF is set, building
    # magics still requires legacy netcdf-cxx
    conflicts("~netcdf", when="@4.1.0:4.3.1,4.15.3:")

    # Optional dependencies
    depends_on("netcdf-cxx", when="+netcdf")
    depends_on("pango", when="+cairo")
    depends_on("libemos grib=eccodes", when="+bufr grib=eccodes")
    depends_on("libemos grib=grib-api", when="+bufr grib=grib-api")
    depends_on("qt", when="+metview+qt")

    depends_on("python", type=("build"))
    depends_on("py-jinja2", type=("build"))

    # Replace system python and perl by spack versions:
    def patch(self):
        for plfile in glob.glob("*/*.pl"):
            filter_file("#!/usr/bin/perl", "#!/usr/bin/env perl", plfile)
        for pyfile in glob.glob("*/*.py"):
            filter_file(
                "#!/usr/bin/python",
                "#!/usr/bin/env {0}".format(os.path.basename(self.spec["python"].command.path)),
                pyfile,
            )
        filter_file("HAVE_GRIB", "SKIP_REQUIRED_FILE_WASREMOVED", "test/CMakeLists.txt")

    def cmake_args(self):
        args = ["-DENABLE_ODB=OFF", "-DENABLE_SPOT=OFF"]

        if self.spec.variants["grib"].value == "eccodes":
            args.append("-DENABLE_ECCODES=ON")
        else:
            if self.spec.satisfies("@2.29.1:"):
                args.append("-DENABLE_ECCODES=OFF")

        # magics@4.2.4:4.3.1 cannot be built without netcdf
        if "+netcdf" in self.spec or self.spec.satisfies("@4.1.0:4.3.1"):
            args.append("-DENABLE_NETCDF=ON")
        else:
            args.append("-DENABLE_NETCDF=OFF")

        if "+cairo" in self.spec:
            args.append("-DENABLE_CAIRO=ON")
        else:
            args.append("-DENABLE_CAIRO=OFF")

        if "+fortran" in self.spec:
            args.append("-DENABLE_FORTRAN=ON")
        else:
            args.append("-DENABLE_FORTRAN=OFF")

        if "+bufr" in self.spec:
            args.append("-DENABLE_BUFR=ON")
        else:
            args.append("-DENABLE_BUFR=OFF")

        if "+metview" in self.spec:
            if "+qt" in self.spec:
                args.append("-DENABLE_METVIEW=ON")
                if self.spec["qt"].satisfies("@5:"):
                    args.append("-DENABLE_QT5=ON")
            else:
                args.append("-DENABLE_METVIEW_NO_QT=ON")
        else:
            args.append("-DENABLE_METVIEW=OFF")

        return args

    @property
    def libs(self):
        return find_libraries(["libMagPlus"], root=self.prefix, recursive=True)

    @property
    def headers(self):
        hl = find_all_headers(self.prefix.include)
        hl.directories = [self.prefix.include, self.prefix.include.magics]
        return hl
