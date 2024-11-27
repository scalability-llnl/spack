# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libnfnetlink(AutotoolsPackage):
    """libnfnetlink is a userspace library that provides some low-level
    nfnetlink handling functions.  It is used as a foundation for other,
    netfilter subsystem specific libraries such as libnfnetlink_conntrack,
    libnfnetlink_log and libnfnetlink_queue."""

    homepage = "https://netfilter.org/projects/libnfnetlink/"
    url = "https://netfilter.org/projects/libnfnetlink/files/libnfnetlink-1.0.2.tar.bz2"

    license("GPL-2.0-only")

    version("1.0.2", sha256="b064c7c3d426efb4786e60a8e6859b82ee2f2c5e49ffeea640cfe4fe33cbc376")

    # Versions that were initially sourced at a third party are now deprecated
    with default_args(deprecated=True):
        version(
            "1.0.1",
            sha256="11dd8a1045b03d47c878535eeb6b9eb34db295d21903a4dfd2c2cc63f45e675b",
            url="https://github.com/Distrotech/libnfnetlink/archive/libnfnetlink-1.0.1.tar.gz",
        )
        version(
            "1.0.0",
            sha256="1d43456e51d5ff2e8bc84b68d8acad3bb15603cfaa806ba9693eea4f2aa1abeb",
            url="https://github.com/Distrotech/libnfnetlink/archive/libnfnetlink-1.0.0.tar.gz",
        )
        version(
            "0.0.41",
            sha256="84381ad3aec4fc4884c020c7774a241160d92ed50c9f93a2660db94e212cbb72",
            url="https://github.com/Distrotech/libnfnetlink/archive/libnfnetlink-0.0.41.tar.gz",
        )

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
