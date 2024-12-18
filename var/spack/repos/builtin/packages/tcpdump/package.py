# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tcpdump(AutotoolsPackage):
    """Tcpdump prints out a description of the contents of packets
    on a network interface that match the Boolean expression;
    the description is preceded by a time stamp, printed, by
    default, as hours, minutes, seconds, and fractions of a
    second since midnight."""

    homepage = "https://www.tcpdump.org/"
    url = "https://www.tcpdump.org/release/tcpdump-4.9.3.tar.gz"

    license("BSD-3-Clause")

    version("4.99.4", sha256="0232231bb2f29d6bf2426e70a08a7e0c63a0d59a9b44863b7f5e2357a6e49fea")
    version("4.99.0", sha256="8cf2f17a9528774a7b41060323be8b73f76024f7778f59c34efa65d49d80b842")
    version("4.9.3", sha256="2cd47cb3d460b6ff75f4a9940f594317ad456cfbf2bd2c8e5151e16559db6410")
    version("4.9.2", sha256="798b3536a29832ce0cbb07fafb1ce5097c95e308a6f592d14052e1ef1505fe79")
    version("4.9.1", sha256="f9448cf4deb2049acf713655c736342662e652ef40dbe0a8f6f8d5b9ce5bd8f3")

    depends_on("c", type="build")  # generated

    depends_on("libpcap")
    depends_on("libpcap@1.10.0:", when="@4.99.0:")
