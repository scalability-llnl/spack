# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lima(Package):
    """Linux virtual machines, with a focus on running containers"""

    homepage = "https://lima-vm.io"
    url = "https://github.com/lima-vm/lima/archive/refs/tags/v0.23.2.tar.gz"

    maintainers("trws")

    license("Apache-2.0", checked_by="trws")

    version("0.23.2", sha256="fc21295f78d717efc921f8f6d1ec22f64da82bfe685d0d2d505aee76c53da1ff")

    depends_on("qemu@9:")
    depends_on("go@1.22.0:")

    # NOTE: in truth this is a go build, it fetches many go packages during this build
    # process, but at least uses the built qemu and local vz on macos
    def install(self, spec, prefix):
        make()
        make("install", f"DESTDIR={prefix}", "PREFIX=")
