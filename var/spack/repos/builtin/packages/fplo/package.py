# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import platform

from spack.package import *


class Fplo(MakefilePackage):
    """The FPLO(R) package is a full-potential local-orbital code to solve the
    Kohn-Sham equations on a regular lattice or with free boundary conditions
    (finite systems). Relativistic effects are treated either in a
    scalar-relativistic or a full  4-component formalism.  Available
    functionals are LSDA, GGA (PBE 96) and LSDA/GGA+U. Orbital polarization
    correction can be applied."""

    homepage = "https://www.fplo.de/"
    url = "file://{0}/FPLO22.00-62.tar.gz".format(os.getcwd())
    manual_download = True

    version("22.00-62", sha256="0d1d4e9c1e8e41900901e26c3cd08ee39dcfdeb3f2c4c8862055eaf704b6d69e")

    # TODO: Try to get LAPACK to work with something other than MKL. The build
    # fails even with the fallback/builtin lapack.

    # This patch replaces the default builtin lapack with MKL, as MKL is the
    # only functioning LAPACK implementation.
    patch("lapackconfig.patch")

    # This patch does 3 things: (1) Change the order of the src directories so
    # the object dependencies are correct; (2) removes interactivity; and (3)
    # explicitly sets the configuration.
    patch("MMakefile.patch")

    # Add '-ltinfo' for linking.
    patch("ncurses.patch")

    # Set the names for QT and PYTHON.
    patch("qt-make.patch")

    # Sets the correct python module import order.
    patch("fedit_py.patch")

    depends_on("mkl")
    depends_on("ncurses")
    depends_on("perl", type="run")
    depends_on("qt@5+opengl")

    extends("python")
    depends_on("py-numpy")

    conflicts("%gcc@12:")

    @property
    def build_directory(self):
        return join_path(self.stage.source_path, "FPLO{0}".format(self.version))

    def edit(self, spec, prefix):
        # Need to set this to 'gcc' even if using the intel compiler as all of
        # the configuration files are named with 'gcc'.
        if platform.system() == "Linux":
            fplo_cc = "gcc"
        else:
            fplo_cc = os.path.basename(self.compiler.cc)

        fplo_fc = os.path.basename(self.compiler.fc)

        conffile = "{0}-{1}-{2}-{3}".format(
            fplo_cc, fplo_fc, platform.system(), platform.machine()
        )
        mmakefile = FileFilter(join_path(self.build_directory, "install", "MMakefile"))
        mmakefile.filter(r"(^conffile=\$configdir/)$", r"\1{0}".format(conffile))
        mmakefile.filter(r"(^mkl=).*", r"\11")

        # use spack compiler
        files = glob.glob(join_path(self.build_directory, "install", "conf", "*"))
        filter_file(r"^\s*CC\s*=.*", "CC=" + spack_cc, *files)
        filter_file(r"^\s*CXX\s*=.*", "CXX=" + spack_cxx, *files)
        filter_file(r"^\s*F90\s*=.*", "F90=" + spack_fc, *files)

        # patch for 64 bit integers
        if spec["mkl"].satisfies("+ilp64"):
            setuphelper = FileFilter(join_path(self.build_directory, "PYTHON", "setuphelper.py"))
            setuphelper.filter("mkl 64bit integer 32bit", "mkl 64bit integer 64bit")

        # setup python build
        python_makefile = FileFilter(join_path(self.build_directory, "PYTHON", "Makefile"))
        python_makefile.filter(r"(build_ext\s* --inplace)\s*--interactive(\s*.*)", r"\1\2")

    def build(self, spec, prefix):
        mmakefile = Executable(join_path(self.build_directory, "install", "MMakefile"))
        mmakefile_args = ["-f90", spack_fc, "-cc", spack_cc, "-c+", spack_cxx]

        with working_dir(self.build_directory):
            # copy contents of bin
            copy_tree("bin", join_path(self.stage.source_path, "bin"))

            # configure the build
            with working_dir("install"):
                mmakefile(*mmakefile_args)

            # build main
            make()
            make("install")

            # build XFBP
            with working_dir(join_path("XFBP_rel", "XFBP")):
                make()
                make("install")

            # build XFPLO
            with working_dir(join_path("XFPLO_rel", "XFPLO")):
                make()
                make("install")

            # build python
            with working_dir("PYTHON"):
                make("python3")

    def install(self, spec, prefix):
        with working_dir(self.stage.source_path):
            install_tree("bin", prefix.bin)

        with working_dir(self.build_directory):
            install_tree("DOC", join_path(prefix.share, "DOC"))
            with working_dir("PYTHON"):
                install_tree("pyfplo", join_path(python_platlib, "pyfplo"))

    @run_after("install")
    def perl_interpreter(self):
        with working_dir(self.prefix.bin):
            pattern = "^#!.*/usr/bin/perl"
            repl = "#!{0}".format(self.spec["perl"].command.path)
            files = ["fconv2", "fconvdens2", "fdowngrad.pl", "fout2in", "grBhfat", "grpop"]
            filter_file(pattern, repl, *files, backup=False)
