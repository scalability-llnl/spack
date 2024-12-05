# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libpfm4(MakefilePackage):
    """libpfm4 is a userspace library to help
    setup performance events for use with
    the perf_events Linux kernel interface."""

    homepage = "https://perfmon2.sourceforge.net"
    url = "https://downloads.sourceforge.net/project/perfmon2/libpfm4/libpfm-4.12.0.tar.gz"
    maintainers("mwkrentel")

    license("MIT")

    version("4.13.0", sha256="d18b97764c755528c1051d376e33545d0eb60c6ebf85680436813fa5b04cc3d1")
    version("4.12.0", sha256="4b0c1f53f39a61525b69bebf532c68040c1b984d7544a8ae0844b13cd91e1ee4")
    version("4.11.0", sha256="5da5f8872bde14b3634c9688d980f68bda28b510268723cc12973eedbab9fecc")
    version("4.10.1", sha256="c61c575378b5c17ccfc5806761e4038828610de76e2e34fac9f7fa73ba844b49")
    version("4.9.0", sha256="db0fbe8ee28fd9beeb5d3e80b7cb3b104debcf6a9fcf5cb8b882f0662c79e4e2")
    version("4.8.0", sha256="9193787a73201b4254e3669243fd71d15a9550486920861912090a09f366cf68")

    depends_on("c", type="build")  # generated

    # Fails to build libpfm4 with intel compiler version 16 and 17
    conflicts("%intel@16:17")

    # Set default optimization level (-O2) if not specified.
    def flag_handler(self, name, flags):
        if name == "cflags":
            for flag in flags:
                if flag.startswith("-O"):
                    break
            else:
                flags.append("-O2")

        return (flags, None, None)

    # Remove -Werror from CFLAGS.  Given the large space of platform,
    # compiler, version, we don't want to fail the build over a stray
    # warning.
    def patch(self):
        filter_file("-Werror", "", "config.mk")

    @property
    def install_targets(self):
        return [
            "DESTDIR={0}".format(self.prefix),
            "LIBDIR=/lib",
            "INCDIR=/include",
            "MANDIR=/man",
            "LDCONFIG=true",
            "install",
        ]
