# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Met(AutotoolsPackage):
    """Statistical tool that matches up grids with either
    gridded analyses or point observations and applies
    configurable methods to compute statistics and diagnostics"""

    homepage = "https://dtcenter.org/community-code/model-evaluation-tools-met"
    url = "https://github.com/dtcenter/MET/archive/refs/tags/v11.0.1.tar.gz"
    git = "https://github.com/dtcenter/MET"

    maintainers("AlexanderRichert-NOAA")

    version("develop", branch="develop")
    version("11.1.0", sha256="e2e371ae1f49185ff8bf08201b1a3e90864a467aa3369b04132d231213c3c9e5")
    version("11.0.2", sha256="f720d15e1d6c235c9a41fd97dbeb0eb1082fb8ae99e1bcdcb5e51be9b50bdfbf")
    version("11.0.1", sha256="48d471ad4634f1b969d9358c51925ce36bf0a1cec5312a6755203a4794b81646")
    version("11.0.0", sha256="648ebb54d07ca099680f4fc23b7ef5095c1a8ac5537c0a5d0e8587bf15991cff")
    version("10.1.1", sha256="9827e65fbd1c64e776525bae072bc2d37d14465e85a952778dcc32a26d8b5c9e")
    version("10.1.0", sha256="8d4c1fb2311d8481ffd24e30e407a1b1bc72a6add9658d76b9c323f1733db336")
    version("10.0.1", sha256="8e965bb0eb8353229a730af511c5fa62bad9744606ab6a218d741d29eb5f3acd")
    version("10.0.0", sha256="92f37c8bd83c951d86026cce294a16e4d3aa6dd41905629d0a729fa1bebe668a")
    version("9.1.3", sha256="7356a5ad79ca961fd965cadd93a7bf6c73b3aa5fb1a01a932580b94e66d0d0c8")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("openmp", default=True, description="Use OpenMP multithreading")
    variant("grib2", default=False, description="Enable compilation of utilities using GRIB2")
    variant("python", default=False, description="Enable python embedding")
    variant("lidar2nc", default=False, description="Enable compilation of lidar2nc")
    variant("modis", default=False, description="Enable compilation of modis")
    variant("graphics", default=False, description="Enable compilation of mode_graphics")

    depends_on("gsl")
    depends_on("bufr")
    depends_on("zlib-api")
    depends_on("netcdf-c")
    depends_on("netcdf-cxx4")
    depends_on("g2c", when="+grib2")

    depends_on("hdf-eos2", when="+modis")
    depends_on("hdf-eos2", when="+lidar2nc")
    depends_on("hdf", when="+modis")
    depends_on("hdf", when="+lidar2nc")

    depends_on("cairo", when="+graphics")
    depends_on("freetype", when="+graphics")

    depends_on("python@3.6.3:", when="+python", type=("build", "run"))
    depends_on("py-netcdf4", when="+python", type=("build", "run"))
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("py-xarray", when="+python", type=("build", "run"))
    depends_on("py-pandas", when="+python", type=("build", "run"))

    patch("openmp_shape_patch.patch", when="@10.1.0")

    # https://github.com/JCSDA/spack-stack/issues/615
    # TODO(srherbener) Apple clang 14.x is getting pickier! When these updates are
    # merged into the MET code base, the following two patches can be removed.
    patch("apple-clang-string-cast-operator.patch", when="@10.1.1: %apple-clang@14:")
    patch("apple-clang-no-register.patch", when="@10.1.1: %apple-clang@14:")

    def url_for_version(self, version):
        if version < Version("11"):
            release_date = {
                "10.1.1": "20220419",
                "10.1.0": "20220314",
                "10.0.1": "20211201",
                "10.0.0": "20210510",
                "9.1.3": "20210319",
            }
            url = "https://github.com/dtcenter/MET/releases/download/v{0}/met-{0}.{1}.tar.gz"
            return url.format(version, release_date[str(version)])
        else:
            url = "https://github.com/dtcenter/MET/archive/refs/tags/v{0}.tar.gz"
            return url.format(version)

    def setup_build_environment(self, env):
        spec = self.spec
        cppflags = []
        ldflags = []
        libs = []

        gsl = spec["gsl"]
        env.set("MET_GSL", gsl.prefix)

        netcdfcxx = spec["netcdf-cxx4"]
        cppflags.append(netcdfcxx.libs.search_flags)
        ldflags.append(netcdfcxx.libs.ld_flags)
        libs.append(netcdfcxx.libs.link_flags)

        netcdfc = spec["netcdf-c"]
        if netcdfc.satisfies("+shared"):
            cppflags.append("-I" + netcdfc.prefix.include)
            ldflags.append("-L" + netcdfc.prefix.lib)
            libs.append(netcdfc.libs.link_flags)
        else:
            nc_config = which(os.path.join(netcdfc.prefix.bin, "nc-config"))
            cppflags.append(nc_config("--cflags", output=str).strip())
            ldflags.append(nc_config("--libs", "--static", output=str).strip())
            libs.append(nc_config("--libs", "--static", output=str).strip())

        zlib = spec["zlib-api"]
        cppflags.append("-D__64BIT__")
        ldflags.append("-L" + zlib.prefix.lib)
        libs.append("-lz")

        bufr = spec["bufr"]
        shared_bufr = True if "+shared" in bufr else False
        bufr_libdir = find_libraries(
            "libbufr_4", root=bufr.prefix, shared=shared_bufr, recursive=True
        ).directories[0]
        env.set("BUFRLIB_NAME", "-lbufr_4")
        env.set("MET_BUFRLIB", bufr_libdir)

        if "+grib2" in spec:
            g2c = spec["g2c"]
            env.set("MET_GRIB2CLIB", g2c.libs.directories[0])
            env.set("MET_GRIB2CINC", g2c.prefix.include)
            env.set("GRIB2CLIB_NAME", "-lg2c")

        if "+python" in spec:
            python = spec["python"]
            env.set("MET_PYTHON", python.command.path)
            env.set("MET_PYTHON_BIN_EXE", python.command.path)
            env.set("MET_PYTHON_CC", "-I" + python.headers.directories[0])
            py_ld = [python.libs.ld_flags]
            if spec["python"].satisfies("~shared"):
                py_ld.append(spec["gettext"].libs.ld_flags)
                py_ld.append(spec["gettext"].libs.ld_flags)
                py_ld.append(spec["libiconv"].libs.ld_flags)
                py_ld.append("-lutil")
            env.set("MET_PYTHON_LD", " ".join(py_ld))

        if "+lidar2nc" in spec or "+modis" in spec:
            hdf = spec["hdf"]
            hdfeos = spec["hdf-eos2"]
            env.set("MET_HDF5", hdf.prefix)
            env.set("MET_HDFEOS", hdfeos.prefix)

            if "+szip" in hdf:
                libs.append(" ".join(hdf["szip"].libs))
            if "+external-xdr" in hdf:
                libs.append(" ".join(hdf["rpc"].libs))

        if "+graphics" in spec:
            cairo = spec["cairo"]
            freetype = spec["freetype"]
            env.set("MET_CAIRO", cairo.prefix)
            cppflags.append("-I" + cairo.prefix.include.cairo)
            env.set("MET_FREETYPE", freetype.prefix)

        env.set("CPPFLAGS", " ".join(cppflags))
        env.set("LIBS", " ".join(libs))
        env.set("LDFLAGS", " ".join(ldflags))

    def configure_args(self):
        args = []
        args.extend(self.enable_or_disable("grib2"))
        args.extend(self.enable_or_disable("python"))
        args.extend(self.enable_or_disable("openmp"))
        args.extend(self.enable_or_disable("lidar2nc"))
        args.extend(self.enable_or_disable("modis"))
        args.extend(self.enable_or_disable("mode_graphics", variant="graphics"))

        if self.spec.satisfies("%apple-clang@14:"):
            args.append("CXXFLAGS=-std=gnu++17")

        return args


#    def setup_run_environment(self, env):
#        env.set('MET_BASE', self.prefix)
