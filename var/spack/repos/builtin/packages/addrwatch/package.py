# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Addrwatch(AutotoolsPackage):
    """A tool similar to arpwatch for IPv4/IPv6 and ethernet address
    pairing monitoring."""

    homepage = "https://github.com/fln/addrwatch"
    url = "https://github.com/fln/addrwatch/releases/download/v1.0.2/addrwatch-1.0.2.tar.gz"

    license("GPL-3.0-or-later")

    version("1.0.2", sha256="f04e143da881cd63c299125b592cfb85e4812abbd146f419a1894c00f2ae6208")
    version("1.0.1", sha256="f772b62b1c6570b577473e7c98614dad1124352b377324cbebb36360d8f4ce5a")

    depends_on("c", type="build")  # generated

    depends_on("libevent")
    depends_on("libpcap")
