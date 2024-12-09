# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pxz(MakefilePackage):
    """Pxz is a parallel LZMA compressor using liblzma."""

    homepage = "https://jnovy.fedorapeople.org/pxz/pxz.html"
    url = "https://jnovy.fedorapeople.org/pxz/pxz-4.999.9beta.20091201git.tar.xz"
    git = "https://github.com/jnovy/pxz.git"

    version("develop", branch="master")
    version(
        "4.999.9beta.20091201git",
        sha256="df69f91103db6c20f0b523bb7f026d86ee662c49fe714647ed63f918cd39767a",
    )

    depends_on("c", type="build")  # generated

    depends_on("xz")

    conflicts("platform=darwin", msg="Pxz runs only on Linux.")

    def install(self, spec, prefix):
        make("install", "DESTDIR=%s" % prefix, "BINDIR=/bin", "MANDIR=/share/man")
