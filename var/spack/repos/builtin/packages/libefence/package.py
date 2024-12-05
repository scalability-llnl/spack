# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libefence(MakefilePackage):
    """Electric Fence (or eFence) is a memory debugger written by Bruce Perens.
    It consists of a library which programmers can link into their code to override
    the C standard library memory management functions. eFence triggers a program
    crash when the memory error occurs, so a debugger can be used to inspect the
    code that caused the error."""

    homepage = "https://packages.debian.org/unstable/electric-fence"
    url = "https://deb.debian.org/debian/pool/main/e/electric-fence/electric-fence_2.2.6.tar.gz"

    maintainers("cessenat")

    license("GPL-2.0-or-later")

    version("2.2.6", sha256="a949e0dedb06cbcd444566cce1457223f2c41abd3513f21663f30f19ccc48e24")

    depends_on("c", type="build")  # generated

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make(
            "install",
            "LIB_INSTALL_DIR=" + prefix.lib,
            "MAN_INSTALL_DIR=" + prefix.man.man3,
            parallel=False,
        )
