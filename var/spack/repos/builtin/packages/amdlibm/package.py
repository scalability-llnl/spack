# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Amdlibm(SConsPackage):
    """AMD LibM is a software library containing a collection of basic math
    functions optimized for x86-64 processor-based machines. It provides
    many routines from the list of standard C99 math functions.
    Applications can link into AMD LibM library and invoke math functions
    instead of compiler's math functions for better accuracy and
    performance."""

    homepage = "https://developer.amd.com/amd-aocl/amd-math-library-libm/"
    git = "https://github.com/amd/aocl-libm-ose.git"
    maintainers = ["amd-toolchain-support"]

    # If a user who doesn't specify a version
    # amdlibm installed for commit ID:4033e02
    # of master branch.
    # To install amdlibm from latest master branch:
    # spack install amdlibm ^amdlibm@master
    version("3.0", branch="aocl-3.0")
    version("2.2", commit="4033e022da428125747e118ccd6fdd9cee21c470")

    variant("verbose", default=False,
            description="Building with verbosity")

    # Mandatory dependencies
    depends_on("python@3.6.1:", type=("build", "run"))
    depends_on("scons@3.1.2:", type=("build"))
    depends_on("mpfr", type=("link"))

    patch("0001-libm-ose-Scripts-cleanup-pyc-files.patch", when="@2.2")
    patch("0002-libm-ose-prevent-log-v3.c-from-building.patch", when="@2.2")

    conflicts("%gcc@:9.1.999", msg="Minimum required GCC version is 9.2.0")

    def build_args(self, spec, prefix):
        """Setting build arguments for amdlibm """
        args = ["--prefix={0}".format(prefix)]

        if "%aocc" in spec:
            args.append("--compiler=aocc")

        # we are circumventing the use of
        # Spacks compiler wrappers because
        # SCons wipes out all environment variables.
        args.append("CC={0}".format(self.compiler.cc))
        args.append("CXX={0}".format(self.compiler.cxx))

        if "+verbose" in spec:
            args.append("verbose=1")
        else:
            args.append("verbose=0")

        return args

    install_args = build_args

    @run_after('install')
    def create_symlink(self):
        """Symbolic link for backward compatibility"""
        with working_dir(self.prefix.lib):
            os.symlink('libalm.a', 'libamdlibm.a')
            os.symlink('libalm.so', 'libamdlibm.so')
