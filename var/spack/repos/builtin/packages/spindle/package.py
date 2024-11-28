# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Spindle(AutotoolsPackage):
    """Spindle improves the library-loading performance of dynamically
    linked HPC applications.  Without Spindle large MPI jobs can
    overload on a shared file system when loading dynamically
    linked libraries, causing site-wide performance problems.
    """

    homepage = "https://computing.llnl.gov/project/spindle/"
    url = "https://github.com/hpc/Spindle/archive/v0.12.tar.gz"

    version("0.12", sha256="3fd9d0afefa9072fffdf2cfd80a0b5e557e201a0b0eb02e7379eae65e64eb1f2")
    version("0.8.1", sha256="c1e099e913faa8199be5811dc7b8be0266f0d1fd65f0a3a25bb46fbc70954ed6")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("launchmon")
    # All versions provide the runtime option --no-mpi to not use MPI, but mpi
    # is needed for the build:
    # 0.8.1 wants to compile tests with mpi.h, newer versions need mpicc
    depends_on("mpi")

    # Workaround for:
    # spindle_logd.cc:65:76: error: narrowing conversion of '255' from 'int' to 'char'
    # spindle_logd.cc:65:76: error: narrowing conversion of '223' from 'int' to 'char'
    # spindle_logd.cc:65:76: error: narrowing conversion of '191' from 'int' to 'char'
    @when("@0.8.1 %gcc")
    def setup_build_environment(self, env):
        env.append_flags("CPPFLAGS", "-Wno-narrowing")
