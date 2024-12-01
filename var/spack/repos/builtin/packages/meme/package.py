# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.version import Version


class Meme(AutotoolsPackage):
    """The MEME Suite allows the biologist to discover novel motifs in
    collections of unaligned nucleotide or protein sequences, and to perform a
    wide variety of other motif-based analyses."""

    homepage = "https://meme-suite.org"
    url = "http://meme-suite.org/meme-software/5.1.1/meme-5.1.1.tar.gz"

    version("5.5.4", sha256="cda6011c2b855bf2563c4e7a2c255e11e99b5b6e5e73736ff008942507580153")
    version("5.3.0", sha256="b2ddec9db972fcf77b29c7deb62df8b1dd8a6638c13c1aa06a5d563c4a7ff756")
    version("5.2.0", sha256="0cbf8c2172e9b6c07855b8aeec457f4825f0b132f8cbb11192880e2f6033f54f")
    version("5.1.1", sha256="38d73d256d431ad4eb7da2c817ce56ff2b4e26c39387ff0d6ada088938b38eb5")
    version("4.12.0", sha256="49ff80f842b59d328588acfcd1d15bf94c55fed661d22b0f95f37430cc363a06")
    version("4.11.4", sha256="3e869ff57e327a9c8615dbef784e3f1095f7f7a0120cecd55efe10c3f2ee8eb3")

    depends_on("c", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI support")
    variant("magick", default=False, description="Enable imagemagick for png output")

    # Perl runtime deps
    depends_on("perl@5.16:", type=("build", "run"))
    depends_on("perl-xml-parser", type=("build", "run"))
    depends_on("perl-xml-simple", type=("build", "run"))
    # Python runtime deps
    depends_on("python", type=("build", "run"))
    # Build deps
    depends_on("zlib-ng")
    depends_on("ghostscript")
    depends_on("libxml2")
    depends_on("libxslt")
    # Variant deps
    depends_on("imagemagick", type=("build", "run"), when="+magick")
    depends_on("mpi", when="+mpi")

    patch("arm.patch", when="%arm")

    def patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        if self.spec.satisfies("%nvhpc"):
            filter_file("-fno-common", "", "configure")
            filter_file("-Wno-unused", "", "configure")

    def url_for_version(self, version):
        url = "http://meme-suite.org/meme-software/{0}/meme{1}{2}.tar.gz"
        sep = "-" if version >= Version("5.0.2") else "_"
        return url.format(version.up_to(3), sep, version)

    def configure_args(self):
        if "~mpi" in self.spec:
            return ["--enable-serial"]
        return []
