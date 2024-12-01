# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


# Although zlib comes with a configure script, it does not use Autotools
# The AutotoolsPackage causes zlib to fail to build with PGI
class Zlib(Package):
    """A free, general-purpose, legally unencumbered lossless
    data-compression library.
    """

    homepage = "http://zlib.net"
    # URL must remain http:// so Spack can bootstrap curl
    url = "http://zlib.net/fossils/zlib-1.2.11.tar.gz"
    tags = ["windows"]

    version("1.2.11", sha256="c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1")
    # Due to the bug fixes, any installations of 1.2.9 or 1.2.10 should be
    # immediately replaced with 1.2.11.
    version("1.2.8", sha256="36658cb768a54c1d4dec43c3116c27ed893e88b02ecfcb44f2166f9c0b7f2a0d")
    version("1.2.3", sha256="1795c7d067a43174113fdf03447532f373e1c6c57c08d61d9e4e9be5e244b05e")

    variant("pic", default=True, description="Produce position-independent code (for shared libs)")
    variant("shared", default=True, description="Enables the build of shared libraries.")
    variant("optimize", default=True, description="Enable -O2 for a more optimized lib")

    patch("w_patch.patch", when="@1.2.11%cce")

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries(["libz"], root=self.prefix, recursive=True, shared=shared)

    def setup_build_environment(self, env):
        if "+pic" in self.spec:
            env.append_flags("CFLAGS", self.compiler.cc_pic_flag)
        if "+optimize" in self.spec:
            env.append_flags("CFLAGS", "-O2")

    def install(self, spec, prefix):
        config_args = []
        if "~shared" in spec:
            config_args.append("--static")
        configure("--prefix={0}".format(prefix), *config_args)

        make()
        if self.run_tests:
            make("check")
        make("install")
