# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Veclibfort(Package):
    """Lightweight but flexible shim designed to rectify the incompatibilities
    between the Accelerate/vecLib BLAS and LAPACK libraries shipped with macOS
    and FORTRAN code compiled with modern compilers such as GNU Fortran."""

    homepage = "https://github.com/mcg1969/vecLibFort"
    url = "https://github.com/mcg1969/vecLibFort/archive/0.4.2.tar.gz"
    git = "https://github.com/mcg1969/vecLibFort.git"

    license("BSL-1.0")

    version("develop", branch="master")
    version("0.4.3", sha256="fe9e7e0596bfb4aa713b2273b21e7d96c0d7a6453ee4b214a8a50050989d5586")
    version("0.4.2", sha256="c61316632bffa1c76e3c7f92b11c9def4b6f41973ecf9e124d68de6ae37fbc85")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Build shared libraries as well as static libs.")

    # virtual dependency
    provides("blas")
    # https://github.com/scipy/scipy/wiki/Dropping-support-for-Accelerate
    provides("lapack@3.2.1")

    requires("platform=darwin", msg="vecLibFort can be installed on macOS only")

    @property
    def libs(self):
        shared = True if "+shared" in self.spec else False
        return find_libraries("libvecLibFort", root=self.prefix, shared=shared, recursive=True)

    @property
    def headers(self):
        # veclibfort does not come with any headers. Return an empty list
        # to avoid `spec['blas'].headers` from crashing.
        return HeaderList([])

    def install(self, spec, prefix):
        if sys.platform != "darwin":
            raise InstallError("vecLibFort can be installed on macOS only")

        filter_file(r"^PREFIX=.*", "", "Makefile")

        make_args = []

        if spec.satisfies("%gcc@6:"):
            make_args += ["CFLAGS=-flax-vector-conversions"]

        make_args += ["PREFIX=%s" % prefix, "install"]

        make(*make_args)

        # test
        fc = which("fc")
        flags = ["-o", "tester", "-O", "tester.f90"]
        flags.extend(spec["veclibfort"].libs.ld_flags.split())
        fc(*flags)
        Executable("./tester")()
