# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Czmq(AutotoolsPackage):
    """A C interface to the ZMQ library"""

    homepage = "http://czmq.zeromq.org"
    url = "https://github.com/zeromq/czmq/archive/v4.0.2.tar.gz"

    license("MPL-2.0")

    version("4.2.1", sha256="83457cd32a2c2615b8d7ebcf91b198cb0d8df383a2072b96835ab250164d8a83")
    version("4.1.1", sha256="b7623433547aa4b6e79722796c27ebc7c0470fea4204e920fd05e717c648f889")
    version("4.0.2", sha256="794f80af7392ec8d361ad69646fc20aaa284d23fef92951334009771a732c810")
    version("3.0.2", sha256="e56f8498daf70310b31c42669b2f9b753c5e747eafaff6d4fdac26d72a474b27")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("libtool", type="build")
    depends_on("automake", type="build")
    depends_on("autoconf", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("docbook-xml", type="build")
    depends_on("docbook-xsl", type="build")
    depends_on("uuid")
    depends_on("libzmq")

    def flag_handler(self, name, flags):
        if name == "cflags":
            if self.spec.satisfies("%oneapi@2022.2.0:"):
                flags.append("-Wno-error=gnu-null-pointer-arithmetic")
                flags.append("-Wno-error=strict-prototypes")
        return (flags, None, None)

    def autoreconf(self, spec, prefix):
        autogen = Executable("./autogen.sh")
        autogen()

    def configure_args(self):
        config_args = []
        if "clang" in self.compiler.name:
            config_args.append("CFLAGS=-Wno-gnu")
            config_args.append("CXXFLAS=-Wno-gnu")
        return config_args
