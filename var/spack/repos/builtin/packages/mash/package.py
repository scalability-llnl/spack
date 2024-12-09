# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mash(AutotoolsPackage):
    """
    Fast genome and metagenome distance estimation using MinHash.
    """

    homepage = "https://mash.readthedocs.org/"
    url = "https://github.com/marbl/Mash/archive/refs/tags/v2.3.tar.gz"

    maintainers("marcusboden")

    version("2.3", sha256="f96cf7305e010012c3debed966ac83ceecac0351dbbfeaa6cd7ad7f068d87fe1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    patch("gcc-11.patch", when="%gcc@11:")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("capnproto")
    depends_on("gsl")

    def patch(self):
        if self.spec.satisfies("target=aarch64:"):
            filter_file(
                "CXXFLAGS += -include src/mash/memcpyLink.h -Wl,--wrap=memcpy",
                "",
                "Makefile.in",
                string=True,
            )
            filter_file("CFLAGS += -include src/mash/memcpyLink.h", "", "Makefile.in", string=True)

    def configure_args(self):
        args = []
        args.append("--with-capnp=" + self.spec["capnproto"].prefix)
        args.append("--with-gsl=" + self.spec["gsl"].prefix)
        return args
