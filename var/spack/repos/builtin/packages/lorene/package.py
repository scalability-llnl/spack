# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Lorene(MakefilePackage):
    """LORENE: Langage Objet pour la RElativite NumeriquE.

    LORENE is a set of C++ classes to solve various problems
    arising in numerical relativity, and more generally in
    computational astrophysics. It provides tools to solve
    partial differential equations by means of multi-domain
    spectral methods."""

    homepage = "https://lorene.obspm.fr/index.html"
    cvs = ":pserver:anonymous:anonymous@octane.obspm.fr:/cvsroot%module=Lorene"

    maintainers("eschnett")

    version("2021.4.22", date="2021-04-22")

    variant("fftw", default=True, description="Use external FFTW for spectral transformations")
    variant(
        "bin_star",
        default=True,
        description="Build Bin_star solver for binary neutron star systems",
    )

    depends_on("blas")
    depends_on("fftw @3:", when="+fftw")
    depends_on("gsl")
    depends_on("lapack")
    depends_on("pgplot")

    parallel = False

    def edit(self, spec, prefix):
        blas_libs = spec["blas"].libs.link_flags
        fftw_incdirs = "-I" + spec["fftw"].prefix.include if spec.satisfies("+fftw") else ""
        fftw_libdirs = "-L" + spec["fftw"].prefix.lib if spec.satisfies("+fftw") else ""
        fftw_libs = spec["fftw"].libs.link_flags
        gsl_incdirs = "-I" + spec["gsl"].prefix.include
        gsl_libdirs = "-L" + spec["gsl"].prefix.lib
        gsl_libs = spec["gsl"].libs.link_flags
        lapack_libs = spec["lapack"].libs.link_flags
        pgplot_incdirs = "-I" + spec["pgplot"].prefix.include
        pgplot_libdirs = "-L" + spec["pgplot"].prefix.lib
        pgplot_libs = spec["pgplot"].libs.link_flags

        substitutions = [
            ("@CXX@", self.compiler.cxx),
            ("@CXXFLAGS@", "-g -I$(HOME_LORENE)/C++/Include -O3 -DNDEBUG"),
            ("@CXXFLAGS_G@", "-g -I$(HOME_LORENE)/C++/Include"),
            ("@F77@", self.compiler.f77),
            ("@F77FLAGS@", "-ffixed-line-length-none -g -O3"),
            ("@F77FLAGS_G@", "-ffixed-line-length-none -g"),
            (
                "@INC@",
                (
                    "-I$(HOME_LORENE)/C++/Include "
                    + "-I$(HOME_LORENE)/C++/Include_extra "
                    + fftw_incdirs
                    + " "
                    + gsl_incdirs
                    + " "
                    + pgplot_incdirs
                ),
            ),
            ("@RANLIB@", "ls"),
            ("@MAKEDEPEND@", ": >$(df).d"),
            ("@FFT_DIR@", "FFTW3"),
            ("@LIB_CXX@", fftw_libdirs + " " + fftw_libs + " -lgfortran"),
            ("@LIB_GSL@", gsl_libdirs + " " + gsl_libs),
            ("@LIB_LAPACK@", lapack_libs + " " + blas_libs),
            ("@LIB_PGPLOT@", pgplot_libdirs + " " + pgplot_libs),
        ]
        local_settings_template = join_path(os.path.dirname(__file__), "local_settings.template")
        local_settings = join_path(self.stage.source_path, "local_settings")
        copy(local_settings_template, local_settings)
        for key, value in substitutions:
            filter_file(key, value, local_settings)

    def build(self, spec, prefix):
        args = ["HOME_LORENE=" + self.build_directory]
        # (We could build the documentation as well.)
        # (We could circumvent the build system and simply compile all
        # source files, and do so in parallel.)
        make("cpp", "fortran", "export", *args)
        if spec.satisfies("+bin_star"):
            with working_dir(join_path("Codes", "Bin_star")):
                make(
                    "-f",
                    "Makefile_O2",
                    "coal",
                    "lit_bin",
                    "init_bin",
                    "coal_regu",
                    "init_bin_regu",
                    "analyse",
                    "prepare_seq",
                    *args,
                )

    def install(self, spec, prefix):
        install_tree("Lib", prefix.lib)
        install_tree("Export/C++/Include", prefix.include)
        install_tree("C++/Include", prefix.include)
        mkdirp(prefix.bin)
        if spec.satisfies("+bin_star"):
            for exe in [
                "coal",
                "lit_bin",
                "init_bin",
                "coal_regu",
                "init_bin_regu",
                "analyse",
                "prepare_seq",
            ]:
                install(join_path("Codes", "Bin_star", exe), prefix.bin)

    @property
    def libs(self):
        shared = self.spec.satisfies("+shared")
        return find_libraries("liblorene*", root=self.prefix, shared=shared, recursive=True)
