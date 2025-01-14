# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Wcstools(MakefilePackage):
    """
    Astronomers often need to relate positions on an image of the sky to positions
    on the real sky to identify catalogued objects in images, tell other people where
    to look to find an identified object, or to compute motions of planets, satellites,
    asteroids, or comets.
    WCSTools is a package of programs and a library of utility subroutines for setting and
    using the world coordinate systems (WCS) in the headers of the most common astronomical
    image formats, FITS and IRAF .imh, to relate image pixels to sky coordinates.
    This software is all written in very portable C, so it should compile and
    run on any computer with a C compiler.
    """

    homepage = "http://tdc-www.harvard.edu/wcstools/"
    url = "http://tdc-www.harvard.edu/software/wcstools/wcstools-3.9.7.tar.gz"
    maintainers("pelahi")
    version("3.9.7", sha256="525f6970eb818f822db75c1526b3122b1af078affa572dce303de37df5c7b088")

    def _make(self, *args, **kwargs):
        # PREFIX must be defined on macOS even when building the library, since
        # it gets hardcoded into the library's install_path
        make("VERBOSE=1", "PREFIX=" + self.prefix, "-C", *args, **kwargs)

    # fix the hard coded Makefile of wcstools
    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")

        makefile.filter(r"^\s*CC\s*=.*", "CC = " + spack_cc)
        makefile.filter(r"^\s*CXX\s*=.*", "CXX = " + spack_cxx)
        makefile.filter(r"^\s*F77\s*=.*", "F77 = " + spack_f77)
        makefile.filter(r"^\s*FC\s*=.*", "FC = " + spack_fc)
        makefile.filter(r"^\s*CFLAGS\s*", "COMPILEFLAGS")

        libmakefile = FileFilter("libwcs/Makefile")

        libmakefile.filter(r"^\s*CC\s*=.*", "CC = " + spack_cc)
        libmakefile.filter(r"^\s*CXX\s*=.*", "CXX = " + spack_cxx)
        libmakefile.filter(r"^\s*F77\s*=.*", "F77 = " + spack_f77)
        libmakefile.filter(r"^\s*FC\s*=.*", "FC = " + spack_fc)
        libmakefile.filter(r"^\s*CFLAGS\s*", "COMPILEFLAGS")

    # there is no make install command
    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.lib)
        install("libwcs/libwcs.a", prefix.lib)
        install_tree("bin", prefix.bin)
