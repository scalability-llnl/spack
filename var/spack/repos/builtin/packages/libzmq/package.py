# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Libzmq(AutotoolsPackage):
    """The ZMQ networking/concurrency library and core API"""

    homepage = "https://zguide.zeromq.org/"
    url = "https://github.com/zeromq/libzmq/releases/download/v4.3.5/zeromq-4.3.5.tar.gz"
    git = "https://github.com/zeromq/libzmq.git"

    maintainers("dennisklein")

    license("MPL-2.0")

    version("master", branch="master")
    version("4.3.5", sha256="6653ef5910f17954861fe72332e68b03ca6e4d9c7160eb3a8de5a5a913bfab43")
    version("4.3.4", sha256="c593001a89f5a85dd2ddf564805deb860e02471171b3f204944857336295c3e5")
    version("4.3.3", sha256="9d9285db37ae942ed0780c016da87060497877af45094ff9e1a1ca736e3875a2")
    version("4.3.2", sha256="ebd7b5c830d6428956b67a0454a7f8cbed1de74b3b01e5c33c5378e22740f763")
    version("4.3.1", sha256="bcbabe1e2c7d0eec4ed612e10b94b112dd5f06fcefa994a0c79a45d835cd21eb")
    version("4.3.0", sha256="8e9c3af6dc5a8540b356697081303be392ade3f014615028b3c896d0148397fd")
    version("4.2.5", sha256="cc9090ba35713d59bb2f7d7965f877036c49c5558ea0c290b0dcc6f2a17e489f")
    version("4.2.2", sha256="5b23f4ca9ef545d5bd3af55d305765e3ee06b986263b31967435d285a3e6df6b")
    version("4.1.4", sha256="e99f44fde25c2e4cb84ce440f87ca7d3fe3271c2b8cfbc67d55e4de25e6fe378")
    version("4.1.2", sha256="f9162ead6d68521e5154d871bac304f88857308bb02366b81bb588497a345927")
    version("4.1.1", sha256="43d61e5706b43946aad4a661400627bcde9c63cc25816d4749c67b64c3dab8db")
    version("4.0.7", sha256="e00b2967e074990d0538361cc79084a0a92892df2c6e7585da34e4c61ee47b03")
    version("4.0.6", sha256="28a2a9c9b77014c39087a498942449df18bb9885cdb63334833525a1d19f2894")
    version("4.0.5", sha256="3bc93c5f67370341428364ce007d448f4bb58a0eaabd0a60697d8086bc43342b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "libsodium",
        default=True,
        description="Build with message encryption support via libsodium",
    )

    variant("drafts", default=False, description="Build and install draft classes and methods")

    variant("docs", default=False, description="Build documentation")

    variant(
        "libbsd",
        when="@4.3.3:",
        default=(sys.platform != "darwin"),
        description="Use strlcpy from libbsd " + "(will use own implementation if false)",
    )

    variant("libunwind", default=False, description="Build with libunwind support")

    depends_on("libsodium", when="+libsodium")
    depends_on("libsodium@:1.0.3", when="+libsodium@:4.1.2")

    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@master")
    depends_on("pkgconfig", type="build")
    depends_on("docbook-xml", type="build", when="+docs")
    depends_on("docbook-xsl", type="build", when="+docs")

    depends_on("libbsd", when="+libbsd")

    depends_on("libunwind", when="+libunwind")

    conflicts("%gcc@8:", when="@:4.2.2")
    conflicts("%gcc@11:", when="@:4.3.2")

    # Fix aggressive compiler warning false positive
    patch(
        "https://github.com/zeromq/libzmq/commit/92b2c38a2c51a1942a380c7ee08147f7b1ca6845.patch?full_index=1",
        sha256="310b8aa57a8ea77b7ac74debb3bf928cbafdef5e7ca35beaac5d9c61c7edd239",
        when="@4.3.3:4.3.4",
    )

    # Fix build issues with gcc-12
    patch(
        "https://github.com/zeromq/libzmq/pull/4334.patch?full_index=1",
        sha256="edca864cba914481a5c97d2e975ba64ca1d2fbfc0044e9a78c48f1f7b2bedb6f",
        when="@4.3.4",
    )

    # Fix static assertion failure with gcc-13
    patch(
        "https://github.com/zeromq/libzmq/commit/438d5d88392baffa6c2c5e0737d9de19d6686f0d.patch?full_index=1",
        sha256="e15a8bfe8131f3e648fd79f3c1c931f99cd896b2733a7df1760f5b4354a0687c",
        when="@4.3.3:4.3.4",
    )

    def url_for_version(self, version):
        if version <= Version("4.1.4"):
            url = "http://download.zeromq.org/zeromq-{0}.tar.gz"
        else:
            url = "https://github.com/zeromq/libzmq/releases/download/v{0}/zeromq-{0}.tar.gz"
        return url.format(version)

    @when("@master")
    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")

    def configure_args(self):
        config_args = []

        config_args.extend(self.with_or_without("docs"))
        config_args.extend(self.enable_or_disable("drafts"))
        config_args.extend(self.enable_or_disable("libbsd"))
        config_args.extend(self.with_or_without("libsodium"))
        config_args.extend(self.enable_or_disable("libunwind"))
        # the package won't compile with newer compilers because warnings
        # are converted to errors. Hence, disable such conversion.
        # this option was only added in version 4.2.3.
        if self.spec.version >= Version("4.2.3"):
            config_args.append("--disable-Werror")
        if "clang" in self.compiler.cc:
            config_args.append("CFLAGS=-Wno-gnu")
            config_args.append("CXXFLAGS=-Wno-gnu")
        return config_args
