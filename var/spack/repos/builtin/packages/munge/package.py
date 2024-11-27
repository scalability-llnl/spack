# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Munge(AutotoolsPackage):
    """MUNGE Uid 'N' Gid Emporium"""

    homepage = "https://dun.github.io/munge/"
    url = "https://github.com/dun/munge/releases/download/munge-0.5.14/munge-0.5.14.tar.xz"
    maintainers("ChristianTackeGSI")

    license("LGPL-3.0-only")

    version("0.5.15", sha256="3f979df117a34c74db8fe2835521044bdeb08e3b7d0f168ca97c3547f51da9ba")
    version("0.5.14", sha256="6606a218f18090fa1f702e3f6fb608073eb6aafed534cf7dd81b67b2e0d30640")
    version("0.5.13", sha256="99753dfd06a4f063c36f3fb0eb1964f394feb649937d94c4734d85b7964144da")
    version("0.5.12", sha256="e972e3c3e947995a99e023f5758047db16cfe2f0c2c9ca76399dc1511fa71be8")
    version(
        "0.5.11",
        sha256="8e075614f81cb0a6df21a0aafdc825498611a04429d0876f074fc828739351a5",
        url="https://github.com/dun/munge/releases/download/munge-0.5.11/munge-0.5.11.tar.bz2",
    )

    depends_on("c", type="build")  # generated

    variant(
        "localstatedir",
        default="PREFIX/var",
        values=any,
        description="Set local state path (possibly to /var)",
    )

    depends_on("openssl")
    depends_on("libgcrypt")
    depends_on("bzip2")

    def configure_args(self):
        args = []
        localstatedir = self.spec.variants["localstatedir"].value
        if localstatedir != "PREFIX/var":
            args.append("--localstatedir={0}".format(localstatedir))
        return args

    def install(self, spec, prefix):
        os.makedirs(os.path.join(prefix, "lib/systemd/system"))
        super().install(spec, prefix)
