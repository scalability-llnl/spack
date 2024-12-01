# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmnl(AutotoolsPackage):
    """libmnl is a minimalistic user-space library oriented to Netlink
    developers. There are a lot of common tasks in parsing, validating,
    constructing of both the Netlink header and TLVs that are repetitive
    and easy to get wrong. This library aims to provide simple helpers
    that allows you to re-use code and to avoid re-inventing the wheel."""

    homepage = "https://netfilter.org/projects/libmnl/"
    url = "https://netfilter.org/projects/libmnl/files/libmnl-1.0.5.tar.bz2"

    license("LGPL-2.1-or-later", checked_by="wdconinc")

    version("1.0.5", sha256="274b9b919ef3152bfb3da3a13c950dd60d6e2bcd54230ffeca298d03b40d0525")

    # Versions that were initially sourced at a third party are now deprecated
    with default_args(deprecated=True):
        version(
            "1.0.3",
            sha256="14405da1bb3a679c24e0fe1f2845d47359ed2de8055e588df4b6b19cab68e901",
            url="https://github.com/threatstack/libmnl/archive/libmnl-1.0.3.tar.gz",
        )
        version(
            "1.0.2",
            sha256="2caec4716aceb245130f4e42f8c118b92618e37db8bb94e2799aff42b95c269f",
            url="https://github.com/threatstack/libmnl/archive/libmnl-1.0.2.tar.gz",
        )
        version(
            "1.0.1",
            sha256="60fe2a6ce59f6118b75b598dc11fc89b97e20ff8633fbea26fc568c45bbb672b",
            url="https://github.com/threatstack/libmnl/archive/libmnl-1.0.1.tar.gz",
        )

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
