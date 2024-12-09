# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Squashfuse(AutotoolsPackage):
    """squashfuse - Mount SquashFS archives using FUSE"""

    homepage = "https://github.com/vasi/squashfuse"
    url = "https://github.com/vasi/squashfuse/releases/download/0.1.104/squashfuse-0.1.104.tar.gz"
    git = "https://github.com/vasi/squashfuse.git"

    maintainers("haampie")

    license("BSD-2-Clause")

    version("master", branch="master")
    version("0.5.2", sha256="54e4baaa20796e86a214a1f62bab07c7c361fb7a598375576d585712691178f5")
    version("0.5.1", sha256="4dd81ea10323078193e5435ad8481b59f3ac8539648ddc732bcaea50b13966c9")
    version("0.5.0", sha256="d7602c7a3b1d0512764547d27cb8cc99d1b21181e1c9819e76461ee96c2ab4d9")
    version("0.4.0", sha256="646e31449b7914d2404933aea88f8d5f72c5d135d7deae3370ccb394c40d114a")
    version("0.2.0", sha256="e8eea1b013b41d0a320e5a07b131bc70df14e6b3f2d3a849bdee66d100186f4f")
    version(
        "0.1.105",
        sha256="3f776892ab2044ecca417be348e482fee2839db75e35d165b53737cb8153ab1e",
        url="https://github.com/vasi/squashfuse/archive/refs/tags/0.1.105.tar.gz",
    )
    version("0.1.104", sha256="aa52460559e0d0b1753f6b1af5c68cfb777ca5a13913285e93f4f9b7aa894b3a")
    version("0.1.103", sha256="42d4dfd17ed186745117cfd427023eb81effff3832bab09067823492b6b982e7")

    depends_on("c", type="build")  # generated

    variant("shared", default=True, description="Enable shared libraries")
    variant("static", default=True, description="Enable static libraries")
    variant("min_size", default=False, description="Build small binaries")

    variant("zlib", default=True, description="Enable zlib/gzip compression support")
    variant("lz4", default=True, description="Enable LZ4 compression support")
    variant("lzo", default=True, description="Enable LZO compression support")
    variant("xz", default=True, description="Enable xz compression support")
    variant("zstd", default=True, description="Enable Zstandard/zstd support")

    conflicts("~shared", when="~static", msg="Enable shared, static or both")

    depends_on("fuse@2.5:")
    depends_on("fuse@:2", when="@:0.1.103")

    # Note: typically libfuse is external, but this implies that you have to make
    # pkg-config external too, because spack's pkg-config doesn't know how to
    # locate system pkg-config's fuse.pc/fuse3.pc
    depends_on("pkgconfig", type="build")

    # compression libs
    depends_on("zlib-api", when="+zlib")
    depends_on("lz4", when="+lz4")
    depends_on("lzo", when="+lzo")
    depends_on("xz", when="+xz")
    depends_on("zstd", when="+zstd")

    depends_on("m4", type="build", when="@0.1.105,master")
    depends_on("autoconf", type="build", when="@0.1.105,master")
    depends_on("automake", type="build", when="@0.1.105,master")
    depends_on("libtool", type="build", when="@0.1.105,master")

    def flag_handler(self, name, flags):
        if name == "cflags" and "+min_size" in self.spec:
            if "-Os" in self.compiler.opt_flags:
                flags.append("-Os")
                return (None, None, flags)

        return (flags, None, None)

    def configure_args(self):
        args = ["--disable-demo"]
        args += self.enable_or_disable("shared")
        args += self.enable_or_disable("static")
        if "+zlib" in self.spec:
            args.append("--with-zlib=%s" % self.spec["zlib-api"].prefix)
        else:
            args.append("--without-zlib")
        args += self.with_or_without("lz4", activation_value="prefix")
        args += self.with_or_without("lzo", activation_value="prefix")
        args += self.with_or_without("xz", activation_value="prefix")
        args += self.with_or_without("zstd", activation_value="prefix")
        return args
