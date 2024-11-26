# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Sparskit(MakefilePackage):
    """SPARSKIT: A basic tool-kit for sparse matrix computations (Version 2).

    Made by Yousef Saad, University of Minnesota.
    """

    homepage = "https://www-users.cse.umn.edu/~saad/software/SPARSKIT/"

    license("LGPL-2.1-or-later")

    version(
        "develop",
        sha256="ecdd0a9968d6b45153a328710a42fe87600f0bba0e3c53896090b8ae1c113b7a",
        url="http://www-users.cs.umn.edu/~saad/software/SPARSKIT/SPARSKIT2.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # The library uses blas routine which needs to be known when the lib is used.
    # A dependent package should add self.spec['blas'].libs.ld_flags
    # at the end of its link line.
    # But, asis, this packages compiles without needing to know about it.
    # depends_on('blas', type='run')

    variant("pic", default=True, description="Compile with position independent code.")
    variant("debug", default=False, description="Builds a debug version of the library")

    # We provide the standard Make flags here:
    # https://spack.readthedocs.io/en/latest/packaging_guide.html?highlight=flag_handler#compiler-flags
    def flag_handler(self, name, flags):
        spec = self.spec
        if "+pic" in spec:
            if name == "fflags":
                flags.append(self.compiler.fc_pic_flag)
        if name == "fflags":
            if "gfortran" in self.compiler.fc:
                flags.append("-std=legacy")
                flags.append("-Wall")
        if "+debug" in spec:
            if "-g" in self.compiler.debug_flags:
                flags.append("-g")
            if "-O0" in self.compiler.opt_flags:
                flags.append("-O0")
            elif "-O" in self.compiler.opt_flags:
                flags.append("-O")
        else:
            if "-O3" in self.compiler.opt_flags:
                flags.append("-O3")
            elif "-O2" in self.compiler.opt_flags:
                flags.append("-O2")

        return (None, flags, None)

    def edit(self, spec, prefix):
        mkfile = FileFilter("makefile")
        mkfile.filter(r"^(OPT).*=.+", r"\1= -c $(FFLAGS)")
        if os.path.exists("libskit.a"):
            os.unlink("libskit.a")

    def build(self, spec, prefix):
        make("clean")
        make("F77={0}".format(spack_fc))

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        install("libskit.*", prefix.lib)

    @property
    def libs(self):
        return find_libraries("libskit*", root=self.prefix, shared=False, recursive=True)
