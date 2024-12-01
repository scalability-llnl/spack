# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BdwGc(AutotoolsPackage):
    """The Boehm-Demers-Weiser conservative garbage collector is a garbage
    collecting replacement for C malloc or C++ new."""

    homepage = "https://www.hboehm.info/gc/"
    url = "https://github.com/ivmai/bdwgc/releases/download/v8.2.8/gc-8.2.8.tar.gz"

    license("Xerox")

    version("8.2.8", sha256="7649020621cb26325e1fb5c8742590d92fb48ce5c259b502faf7d9fb5dabb160")
    version("8.2.6", sha256="b9183fe49d4c44c7327992f626f8eaa1d8b14de140f243edb1c9dcff7719a7fc")
    version("8.2.4", sha256="3d0d3cdbe077403d3106bb40f0cbb563413d6efdbb2a7e1cd6886595dec48fc2")
    version("8.2.2", sha256="f30107bcb062e0920a790ffffa56d9512348546859364c23a14be264b38836a0")
    version("8.0.6", sha256="3b4914abc9fa76593596773e4da671d7ed4d5390e3d46fbf2e5f155e121bea11")
    version("8.0.0", sha256="8f23f9a20883d00af2bff122249807e645bdf386de0de8cbd6cce3e0c6968f04")
    version(
        "7.6.0",
        sha256="a14a28b1129be90e55cd6f71127ffc5594e1091d5d54131528c24cd0c03b7d90",
        url="http://www.hboehm.info/gc/gc_source/gc-7.6.0.tar.gz",
    )
    version(
        "7.4.4",
        sha256="e5ca9b628b765076b6ab26f882af3a1a29cde786341e08b9f366604f74e4db84",
        url="http://www.hboehm.info/gc/gc_source/gc-7.4.4.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("libatomic-ops", default=True, description="Use external libatomic-ops")
    variant(
        "threads",
        default="none",
        values=("none", "posix", "dgux386"),
        multi=False,
        description="Multithreading support",
    )

    depends_on("libatomic-ops", when="+libatomic-ops")

    def configure_args(self):
        spec = self.spec

        config_args = [
            "--enable-static",
            "--with-libatomic-ops={0}".format("yes" if "+libatomic-ops" in spec else "no"),
            "--enable-threads={0}".format(spec.variants["threads"].value),
        ]

        return config_args
