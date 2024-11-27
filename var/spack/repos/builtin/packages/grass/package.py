# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Grass(AutotoolsPackage):
    """GRASS GIS (Geographic Resources Analysis Support System), is a free
    and open source Geographic Information System (GIS) software suite
    used for geospatial data management and analysis, image processing,
    graphics and maps production, spatial modeling, and visualization."""

    homepage = "https://grass.osgeo.org"
    url = "https://grass.osgeo.org/grass78/source/grass-7.8.5.tar.gz"
    list_url = "https://grass.osgeo.org/download/software/sources/"
    git = "https://github.com/OSGeo/grass.git"

    maintainers("adamjstewart")

    license("MIT")

    version("master", branch="master")
    version("8.2.0", sha256="621c3304a563be19c0220ae28f931a5e9ba74a53218c5556cd3f7fbfcca33a80")
    version("7.8.5", sha256="a359bb665524ecccb643335d70f5436b1c84ffb6a0e428b78dffebacd983ff37")
    version("7.8.2", sha256="33576f7078f805b39ca20c2fa416ac79c64260c0581072a6dc7d813f53aa9abb")
    version("7.8.1", sha256="6ae578fd67afcce7abec4ba4505dcc55b3d2dfe0ca46b99d966cb148c654abb3")
    version("7.8.0", sha256="4b1192294e959ffd962282344e4ff325c4472f73abe605e246a1da3beda7ccfa")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("cxx", default=True, description="Support C++ functionality")
    variant("tiff", default=False, description="Support TIFF functionality")
    variant("png", default=False, description="Support PNG functionality")
    variant("postgres", default=False, description="Support PostgreSQL functionality")
    variant("mysql", default=False, description="Support MySQL functionality")
    variant("sqlite", default=False, description="Support SQLite functionality")
    variant("opengl", default=False, description="Support OpenGL functionality")
    variant("odbc", default=False, description="Support ODBC functionality")
    variant("fftw", default=False, description="Support FFTW functionality")
    variant("blas", default=False, description="Support BLAS functionality")
    variant("lapack", default=False, description="Support LAPACK functionality")
    variant("cairo", default=False, description="Support Cairo functionality")
    variant("freetype", default=False, description="Support FreeType functionality")
    variant("readline", default=False, description="Support Readline functionality")
    variant("regex", default=False, description="Support regex functionality")
    variant("pthread", default=False, description="Support POSIX threads functionality")
    variant("openmp", default=False, description="Support OpenMP functionality")
    variant("opencl", default=False, description="Support OpenCL functionality")
    variant("bzlib", default=False, description="Support BZIP2 functionality")
    variant("zstd", default=False, description="Support Zstandard functionality")
    variant("gdal", default=True, description="Enable GDAL/OGR support")
    variant("liblas", default=False, description="Enable libLAS support")
    variant("wxwidgets", default=False, description="Enable wxWidgets support")
    variant("netcdf", default=False, description="Enable NetCDF support")
    variant("geos", default=False, description="Enable GEOS support")
    variant("x", default=False, description="Use the X Window System")

    # https://htmlpreview.github.io/?https://github.com/OSGeo/grass/blob/master/REQUIREMENTS.html
    # General requirements
    depends_on("gmake@3.81:", type="build")
    depends_on("iconv")
    depends_on("zlib-api")
    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("proj")
    # GRASS 7.8.0 was supposed to support PROJ 6, but it still checks for
    # share/proj/epsg, which was removed in PROJ 6
    depends_on("proj@:5", when="@:7.8.0")
    # PROJ6 support released in GRASS 7.8.1
    # https://courses.neteler.org/grass-gis-7-8-1-released-with-proj-6-and-gdal-3-support/
    depends_on("proj@6:", when="@7.8.1:")
    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-six", when="@7.8:", type=("build", "run"))

    # Optional packages
    depends_on("libtiff", when="+tiff")
    depends_on("libpng", when="+png")
    depends_on("postgresql", when="+postgres")
    depends_on("mariadb", when="+mysql")
    depends_on("sqlite", when="+sqlite")
    depends_on("gl", when="+opengl")
    depends_on("unixodbc", when="+odbc")
    depends_on("fftw", when="+fftw")
    depends_on("blas", when="+blas")
    depends_on("lapack", when="+lapack")
    depends_on("cairo@1.5.8:", when="+cairo")
    depends_on("freetype", when="+freetype")
    depends_on("readline", when="+readline")
    depends_on("opencl", when="+opencl")
    depends_on("bzip2", when="+bzlib")
    depends_on("zstd", when="+zstd")
    depends_on("gdal", when="+gdal")
    conflicts("^gdal@3.3:", when="@7.8")
    depends_on("liblas", when="+liblas")
    depends_on("wxwidgets", when="+wxwidgets")
    depends_on("py-wxpython@2.8.10.1:", when="+wxwidgets", type=("build", "run"))
    depends_on("netcdf-c", when="+netcdf")
    depends_on("geos", when="+geos")
    depends_on("libx11", when="+x")

    def url_for_version(self, version):
        url = "https://grass.osgeo.org/grass{0}/source/grass-{1}.tar.gz"
        return url.format(version.up_to(2).joined, version)

    # https://grasswiki.osgeo.org/wiki/Compile_and_Install
    def configure_args(self):
        spec = self.spec

        args = [
            "--without-nls",
            # TODO: add packages for these optional dependencies
            "--without-opendwg",
            "--without-pdal",
            "--with-proj-share={0}".format(spec["proj"].prefix.share.proj),
        ]

        if spec.satisfies("+cxx"):
            args.append("--with-cxx")
        else:
            args.append("--without-cxx")

        if spec.satisfies("+tiff"):
            args.append("--with-tiff")
        else:
            args.append("--without-tiff")

        if spec.satisfies("+png"):
            args.append("--with-png")
        else:
            args.append("--without-png")

        if spec.satisfies("+postgres"):
            args.append("--with-postgres")
        else:
            args.append("--without-postgres")

        if spec.satisfies("+mysql"):
            args.append("--with-mysql")
        else:
            args.append("--without-mysql")

        if spec.satisfies("+sqlite"):
            args.append("--with-sqlite")
        else:
            args.append("--without-sqlite")

        if spec.satisfies("+opengl"):
            args.append("--with-opengl")
        else:
            args.append("--without-opengl")

        if spec.satisfies("+odbc"):
            args.append("--with-odbc")
        else:
            args.append("--without-odbc")

        if spec.satisfies("+fftw"):
            args.append("--with-fftw")
        else:
            args.append("--without-fftw")

        if spec.satisfies("+blas"):
            args.append("--with-blas")
        else:
            args.append("--without-blas")

        if spec.satisfies("+lapack"):
            args.append("--with-lapack")
        else:
            args.append("--without-lapack")

        if spec.satisfies("+cairo"):
            args.append("--with-cairo")
        else:
            args.append("--without-cairo")

        if spec.satisfies("+freetype"):
            args.append("--with-freetype")
        else:
            args.append("--without-freetype")

        if spec.satisfies("+readline"):
            args.append("--with-readline")
        else:
            args.append("--without-readline")

        if spec.satisfies("+regex"):
            args.append("--with-regex")
        else:
            args.append("--without-regex")

        if spec.satisfies("+pthread"):
            args.append("--with-pthread")
        else:
            args.append("--without-pthread")

        if spec.satisfies("+openmp"):
            args.append("--with-openmp")
        else:
            args.append("--without-openmp")

        if spec.satisfies("+opencl"):
            args.append("--with-opencl")
        else:
            args.append("--without-opencl")

        if spec.satisfies("+bzlib"):
            args.append("--with-bzlib")
        else:
            args.append("--without-bzlib")

        if spec.satisfies("+zstd"):
            args.append("--with-zstd")
        else:
            args.append("--without-zstd")

        if spec.satisfies("+gdal"):
            args.append("--with-gdal={0}/gdal-config".format(spec["gdal"].prefix.bin))
        else:
            args.append("--without-gdal")

        if spec.satisfies("+liblas"):
            args.append("--with-liblas={0}/liblas-config".format(spec["liblas"].prefix.bin))
        else:
            args.append("--without-liblas")

        if spec.satisfies("+wxwidgets"):
            args.append("--with-wxwidgets={0}/wx-config".format(spec["wxwidgets"].prefix.bin))
        else:
            args.append("--without-wxwidgets")

        if spec.satisfies("+netcdf"):
            args.append("--with-netcdf={0}/bin/nc-config".format(spec["netcdf-c"].prefix))
        else:
            args.append("--without-netcdf")

        if spec.satisfies("+geos"):
            args.append("--with-geos={0}/bin/geos-config".format(spec["geos"].prefix))
        else:
            args.append("--without-geos")

        if spec.satisfies("+x"):
            args.append("--with-x")
        else:
            args.append("--without-x")

        return args

    # see issue: https://github.com/spack/spack/issues/11325
    # 'Platform.make' is created after configure step
    # hence invoke the following function afterwards
    @run_after("configure")
    def fix_iconv_linking(self):
        if self.spec["iconv"].name != "libiconv":
            return

        makefile = FileFilter("include/Make/Platform.make")
        makefile.filter(r"^ICONVLIB\s*=.*", "ICONVLIB = -liconv")
