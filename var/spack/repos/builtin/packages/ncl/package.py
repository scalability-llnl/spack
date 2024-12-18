# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import tempfile

from spack.package import *


class Ncl(Package):
    """NCL is an interpreted language designed specifically for
    scientific data analysis and visualization. Supports NetCDF 3/4,
    GRIB 1/2, HDF 4/5, HDF-EOD 2/5, shapefile, ASCII, binary.
    Numerous analysis functions are built-in."""

    homepage = "https://www.ncl.ucar.edu"
    git = "https://github.com/NCAR/ncl.git"
    url = "https://github.com/NCAR/ncl/archive/6.4.0.tar.gz"

    maintainers("vanderwb")

    license("Apache-2.0")

    version("6.6.2", sha256="cad4ee47fbb744269146e64298f9efa206bc03e7b86671e9729d8986bb4bc30e")
    version("6.5.0", sha256="133446f3302eddf237db56bf349e1ebf228240a7320699acc339a3d7ee414591")
    version("6.4.0", sha256="0962ae1a1d716b182b3b27069b4afe66bf436c64c312ddfcf5f34d4ec60153c8")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    patch("for_aarch64.patch", when="target=aarch64:")

    # Use Spack config file, which we generate during the installation:
    patch("set_spack_config.patch")
    # Make ncl compile with hdf5 1.10 (upstream as of 6.5.0)
    patch("hdf5.patch", when="@6.4.0")
    # ymake-filter's buffer may overflow (upstream as of 6.5.0)
    patch("ymake-filter.patch", when="@6.4.0")
    # ymake additional local library and includes will be filtered improperly
    # WARNING: it is tempting to replace '-Dlinux=linux -Dx86_64=x86_64' with '-Ulinux -Ux86_64'
    # to get rid of 'error: detected recursion whilst expanding macro "linux"' but that breaks
    # the building because the Makefile generation logic depends on whether those macros are
    # defined. Also, the errors can be ignored since "GCC detects when it is expanding recursive
    # macros, emits an error message, and *continues* after the offending macro invocation"
    # (see https://gcc.gnu.org/onlinedocs/cpp/Traditional-macros.html#Traditional-macros).
    patch("ymake.patch", when="@6.4.0:")
    # ncl does not build with gcc@10:
    # https://github.com/NCAR/ncl/issues/123
    patch(
        "https://src.fedoraproject.org/rpms/ncl/raw/12778c55142b5b1ccc26dfbd7857da37332940c2/f/ncl-boz.patch",
        when="%gcc@10:",
        sha256="64f3502c9deab48615a4cbc26073173081c0774faf75778b044d251e45d238f7",
    )
    # g2clib does not have a ymakefile. This patch avoids a benign ymake error.
    patch("ymake-grib.patch", when="+grib")

    # This installation script is implemented according to this manual:
    # http://www.ncl.ucar.edu/Download/build_from_src.shtml

    variant("hdf4", default=False, description="Enable HDF4 support.")
    variant("hdf-eos2", default=False, when="+hdf4", description="Enable HDF-EOS2 support.")
    variant("hdf-eos5", default=False, description="Enable HDF-EOS5 support.")
    variant("gdal", default=False, description="Enable GDAL support.")
    variant("triangle", default=True, description="Enable Triangle support.")
    variant("udunits2", default=True, description="Enable UDUNITS-2 support.")
    variant("openmp", default=True, description="Enable OpenMP support.")
    variant("grib", default=True, description="Enable GRIB support.")
    variant("eemd", default=False, description="Enable EEMD support.")

    # The following variant is typically set for little-endian targets
    variant("byteswapped", default=True, description="Use byteswapped mode for binary data.")

    # Non-optional dependencies according to the manual:
    depends_on("jpeg")
    depends_on("netcdf-c")
    depends_on("cairo+X+ft+pdf")

    # Extra dependencies that may be missing from build system:
    depends_on("bison", type="build")
    depends_on("flex+lex")
    depends_on("iconv")
    depends_on("tcsh")
    depends_on("makedepend", type="build")

    # Also, the manual says that ncl requires zlib, but that comes as a
    # mandatory dependency of libpng, which is a mandatory dependency of cairo.

    # The following dependencies are required, otherwise several components
    # fail to compile:
    depends_on("curl")
    depends_on("iconv")
    depends_on("libx11")
    depends_on("libxaw")
    depends_on("libxmu")
    depends_on("pixman")
    depends_on("bzip2")
    depends_on("freetype")
    depends_on("fontconfig")
    depends_on("zstd")

    # In Spack, we do not have an option to compile netcdf-c without netcdf-4
    # support, so we will tell the ncl configuration script that we want
    # support for netcdf-4, but the script assumes that hdf5 is compiled with
    # szip support. We introduce this restriction with the following dependency
    # statement.
    depends_on("hdf5+szip")
    depends_on("szip")

    # ESMF is only required at runtime (for ESMF_regridding.ncl)
    # There might be more requirements to ESMF but at least the NetCDF support is required to run
    # the examples (see https://www.ncl.ucar.edu/Applications/ESMF.shtml)
    depends_on("esmf+netcdf", type="run")

    # Some of the optional dependencies according to the manual:
    depends_on("hdf", when="+hdf4")
    depends_on("hdf-eos2", when="+hdf-eos2")
    depends_on("hdf-eos5", when="+hdf-eos5")
    depends_on("gdal@:2.4", when="+gdal")
    depends_on("udunits", when="+udunits2")
    depends_on("jasper@:2", when="+grib")
    depends_on("gsl", when="+eemd")

    # We need src files of triangle to appear in ncl's src tree if we want
    # triangle's features.
    resource(
        name="triangle",
        url="https://www.netlib.org/voronoi/triangle.zip",
        sha256="1766327add038495fa3499e9b7cc642179229750f7201b94f8e1b7bee76f8480",
        placement="triangle_src",
        when="+triangle",
    )

    sanity_check_is_file = ["bin/ncl"]

    def patch(self):
        # Make configure scripts use Spack's tcsh
        files = ["Configure"] + glob.glob("config/*")

        # Filter sbang before install so Spack's sbang hook can fix it up
        files += glob.glob("ncarg2d/src/bin/scripts/*")
        files += glob.glob("ncarview/src/bin/scripts/*")
        files += glob.glob("ni/src/scripts/*")

        csh = join_path(self.spec["tcsh"].prefix.bin, "csh")

        filter_file("^#!/bin/csh.*", "#!{0}".format(csh), *files)

        if self.spec.satisfies("+grib"):
            # Newer versions of libjasper do not provide the inmem property
            if self.spec.satisfies("^jasper@2"):
                filter_file("image.inmem_=1;", "", "external/g2clib-1.6.0/enc_jpeg2000.c")

            filter_file("SUBDIRS = ", "SUBDIRS = g2clib-1.6.0 ", "external/yMakefile")
            filter_file(
                "INC=.*",
                "INC=%s" % self.spec["jasper"].prefix.include,
                "external/g2clib-1.6.0/makefile",
            )

    def install(self, spec, prefix):
        if (self.compiler.fc is None) or (self.compiler.cc is None):
            raise InstallError("NCL package requires both " "C and Fortran compilers.")

        self.prepare_site_config()
        self.prepare_install_config()
        self.prepare_src_tree()
        make("Everything", parallel=False)

        # Build system may fail without errors, so check for main program.
        exes = os.listdir(self.spec.prefix.bin)
        if "ncl" not in exes:
            raise RuntimeError("Installation failed (ncl executable was not created)")

        # NCL provides compiler wrappers, but they make assumptions that Spack build
        # will not conform to. This section edits the wrappers to fix them.
        c_wrappers = ["ncargcc", "nhlcc"]
        f77_wrappers = ["ncargf77", "nhlf77"]
        f90_wrappers = ["ncargf90", "nhlf90"]
        lib_paths = []

        for dep in spec.dependencies(deptype="link"):
            lib_paths.append(spec[dep.name].prefix.lib)

        with working_dir(spec.prefix.bin):
            # Change NCARG compiler wrappers to use real compiler, not Spack wrappers
            for wrapper in c_wrappers:
                filter_file(spack_cc, self.compiler.cc, wrapper)
            for wrapper in f77_wrappers:
                filter_file(spack_f77, self.compiler.f77, wrapper)
            for wrapper in f90_wrappers:
                filter_file(spack_fc, self.compiler.fc, wrapper)

            # Make library reference and corrections to wrappers
            for wrapper in c_wrappers + f77_wrappers + f90_wrappers:
                filter_file(
                    "^(set syslibdir[ ]*=).*",
                    r'\1 "{}"'.format(" ".join(["-L{}".format(p) for p in lib_paths])),
                    wrapper,
                )
                filter_file("^(set cairolib[ ]*=).*", r'\1 "-lcairo -lfreetype"', wrapper)

    def setup_run_environment(self, env):
        env.set("NCARG_ROOT", self.spec.prefix)

        # We cannot rely on Spack knowledge of esmf when NCL is an external
        if not self.spec.external:
            env.set("ESMFBINDIR", self.spec["esmf"].prefix.bin)

    def prepare_site_config(self):
        fc_flags = [self.compiler.fc_pic_flag]
        cc_flags = [self.compiler.cc_pic_flag]
        c2f_flags = [self.compiler.cc_pic_flag]

        if "+openmp" in self.spec:
            fc_flags.append(self.compiler.openmp_flag)
            cc_flags.append(self.compiler.openmp_flag)

        if self.spec.satisfies("^hdf5@1.11:"):
            cc_flags.append("-DH5_USE_110_API")

        if self.compiler.name == "gcc":
            fc_flags.append("-fno-range-check")
            c2f_flags.extend(["-lgfortran", "-lm"])
        elif self.compiler.name == "intel":
            fc_flags.append("-fp-model precise")
            cc_flags.extend(
                ["-fp-model precise", "-std=c99", "-D_POSIX_C_SOURCE=2", "-D_GNU_SOURCE"]
            )
            c2f_flags.extend(["-lifcore", "-lifport"])

        if self.spec.satisfies("%gcc@10:"):
            fc_flags.append("-fallow-argument-mismatch")
            cc_flags.append("-fcommon")

        if self.spec.satisfies("+grib"):
            gribline = (
                "#define GRIB2lib %s/external/g2clib-1.6.0/libgrib2c.a -ljasper -lpng -lz -ljpeg\n"
                % self.stage.source_path
            )
        else:
            gribline = ""

        with open("./config/Spack", "w") as f:
            f.writelines(
                [
                    "#define HdfDefines\n",
                    (
                        "#define StdDefines -DByteSwapped\n#define ByteSwapped\n"
                        if self.spec.satisfies("+byteswapped")
                        else ""
                    ),
                    "#define CppCommand '/usr/bin/env cpp -traditional'\n",
                    "#define CCompiler {0}\n".format(spack_cc),
                    "#define FCompiler {0}\n".format(spack_fc),
                    (
                        "#define CtoFLibraries " + " ".join(c2f_flags) + "\n"
                        if len(c2f_flags) > 0
                        else ""
                    ),
                    (
                        "#define CtoFLibrariesUser " + " ".join(c2f_flags) + "\n"
                        if len(c2f_flags) > 0
                        else ""
                    ),
                    (
                        "#define CcOptions " + " ".join(cc_flags) + "\n"
                        if len(cc_flags) > 0
                        else ""
                    ),
                    (
                        "#define FcOptions " + " ".join(fc_flags) + "\n"
                        if len(fc_flags) > 0
                        else ""
                    ),
                    "#define BuildShared NO\n",
                    gribline,
                ]
            )

    def prepare_install_config(self):
        # Remove the results of the previous configuration attempts.
        self.delete_files("./Makefile", "./config/Site.local")

        # Generate an array of answers that will be passed to the interactive
        # configuration script.
        config_answers = [
            # Enter Return to continue
            "\n",
            # Build NCL?
            "y\n",
            # Parent installation directory :
            self.spec.prefix + "\n",
            # System temp space directory   :
            tempfile.gettempdir() + "\n",
            # Build NetCDF4 feature support (optional)?
            "y\n",
        ]

        if "+hdf4" in self.spec:
            config_answers.extend(
                [
                    # Build HDF4 support (optional) into NCL?
                    "y\n",
                    # Also build HDF4 support (optional) into raster library?
                    "y\n",
                    # Did you build HDF4 with szip support?
                    "y\n" if self.spec.satisfies("^hdf+szip") else "n\n",
                ]
            )
        else:
            config_answers.extend(
                [
                    # Build HDF4 support (optional) into NCL?
                    "n\n",
                    # Also build HDF4 support (optional) into raster library?
                    "n\n",
                ]
            )

        gribinc = (
            " " + self.stage.source_path + "/external/g2clib-1.6.0/"
            if self.spec.satisfies("+grib")
            else ""
        )
        config_answers.extend(
            [
                # Build Triangle support (optional) into NCL
                "y\n" if "+triangle" in self.spec else "n\n",
                # If you are using NetCDF V4.x, did you enable NetCDF-4 support?
                "y\n",
                # Did you build NetCDF with OPeNDAP support?
                "y\n" if self.spec.satisfies("^netcdf-c+dap") else "n\n",
                # Build GDAL support (optional) into NCL?
                "y\n" if "+gdal" in self.spec else "n\n",
                # Build EEMD support (optional) into NCL?
                "y\n" if "+eemd" in self.spec else "n\n",
                # Build Udunits-2 support (optional) into NCL?
                "y\n" if "+udunits2" in self.spec else "n\n",
                # Build Vis5d+ support (optional) into NCL?
                "n\n",
                # Build HDF-EOS2 support (optional) into NCL?
                "y\n" if "+hdf-eos2" in self.spec else "n\n",
                # Build HDF5 support (optional) into NCL?
                "y\n",
                # Build HDF-EOS5 support (optional) into NCL?
                "y\n" if "+hdf-eos5" in self.spec else "n\n",
                # Build GRIB2 support (optional) into NCL?
                "y\n" if self.spec.satisfies("+grib") else "n\n",
                # Enter local library search path(s) :
                self.spec["fontconfig"].prefix.lib
                + " "
                + self.spec["pixman"].prefix.lib
                + " "
                + self.spec["bzip2"].prefix.lib
                + (
                    (" " + self.spec["jasper"].libs.directories[0])
                    if self.spec.satisfies("+grib")
                    else ""
                )
                + "\n",
                # Enter local include search path(s) :
                # All other paths will be passed by the Spack wrapper.
                self.spec["freetype"].headers.directories[0] + gribinc + "\n",
                # Go back and make more changes or review?
                "n\n",
                # Save current configuration?
                "y\n",
            ]
        )

        config_answers_filename = "spack-config.in"
        config_script = Executable("./Configure")

        with open(config_answers_filename, "w") as f:
            f.writelines(config_answers)

        with open(config_answers_filename, "r") as f:
            config_script(input=f)

        if self.spec.satisfies("^hdf+external-xdr ^libtirpc"):
            hdf4 = self.spec["hdf"]
            replace_str = hdf4["rpc"].libs.link_flags

            if self.spec.satisfies("^hdf+szip"):
                search_str = "#define HDFlib.*"
            else:
                search_str = "#define IncSearch.*"
                replace_str = "\n#define HDFlib {} {}".format(hdf4.libs.link_flags, replace_str)

            filter_file(
                "({})".format(search_str), r"\1 " + "{}".format(replace_str), "config/Site.local"
            )

    def prepare_src_tree(self):
        if "+triangle" in self.spec:
            triangle_src = join_path(self.stage.source_path, "triangle_src")
            triangle_dst = join_path(self.stage.source_path, "ni", "src", "lib", "hlu")
            copy(join_path(triangle_src, "triangle.h"), triangle_dst)
            copy(join_path(triangle_src, "triangle.c"), triangle_dst)

    @staticmethod
    def delete_files(*filenames):
        for filename in filenames:
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                except OSError as e:
                    raise InstallError("Failed to delete file %s: %s" % (e.filename, e.strerror))
