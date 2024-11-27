# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import time

from spack.package import *


class LibuvJulia(AutotoolsPackage):
    """Multi-platform library with a focus on asynchronous IO"""

    homepage = "https://libuv.org"
    url = "https://github.com/JuliaLang/libuv/archive/refs/heads/julia-uv2-1.44.2.tar.gz"
    git = "https://github.com/JuliaLang/libuv.git"

    license("CC-BY-4.0")

    # julia's libuv fork doesn't tag (all?) releases, so we fix commits.
    version("1.48.0", commit="ca3a5a431a1c37859b6508e6b2a288092337029a")
    version("1.44.3", commit="2723e256e952be0b015b3c0086f717c3d365d97e")
    version("1.44.2", commit="e6f0e4900e195c8352f821abe2b3cffc3089547b")
    version("1.44.1", commit="1b2d16477fe1142adea952168d828a066e03ee4c")
    version("1.42.0", commit="3a63bf71de62c64097989254e4f03212e3bf5fc8")

    depends_on("c", type="build")  # generated

    def autoreconf(self, spec, prefix):
        # @haampie: Configure files are checked in, but git does not restore
        # mtime by design. Therefore, touch files to avoid regenerating those.
        # Make sure to set them all to the same time, otherwise weird problems
        # might occur (https://github.com/spack/spack/pull/35945).
        cur = time.time()
        times = (cur, cur)
        os.utime("aclocal.m4", times)
        os.utime("Makefile.in", times)
        os.utime("configure", times)

    @property
    def libs(self):
        return find_libraries(["libuv"], root=self.prefix, recursive=True, shared=False)

    def configure_args(self):
        # Only build static libaries for now
        # https://github.com/JuliaLang/julia/issues/47620
        return ["--disable-shared", "--enable-static", "--with-pic"]
