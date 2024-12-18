# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tnftp(AutotoolsPackage):
    """Tnftp is an FTP client. It is the default FTP client included with many
    BSD operating systems and Darwin"""

    homepage = "https://ftp.netbsd.org/pub/pkgsrc/current/pkgsrc/net/tnftpd/README.html"
    url = "https://cdn.netbsd.org/pub/NetBSD/misc/tnftp/tnftp-20230507.tar.gz"

    maintainers("EbiArnie")

    version("20230507", sha256="be0134394bd7d418a3b34892b0709eeb848557e86474e1786f0d1a887d3a6580")

    depends_on("c", type="build")  # generated

    depends_on("bison")
    depends_on("ncurses")
