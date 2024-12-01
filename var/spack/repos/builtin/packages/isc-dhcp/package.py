# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class IscDhcp(AutotoolsPackage):
    """ISC DHCP offers a complete open source solution for
    implementing DHCP servers, relay agents, and clients. ISC
    DHCP supports both IPv4 and IPv6, and is suitable for use
    in high-volume and high-reliability applications."""

    homepage = "https://www.isc.org/dhcp/"
    url = "https://downloads.isc.org/isc/dhcp/4.4.2/dhcp-4.4.2.tar.gz"
    list_url = "https://downloads.isc.org/isc/dhcp"
    list_depth = 1

    parallel = False

    license("MPL-2.0")

    version("4.4.2", sha256="1a7ccd64a16e5e68f7b5e0f527fd07240a2892ea53fe245620f4f5f607004521")
    version("4.4.1", sha256="2a22508922ab367b4af4664a0472dc220cc9603482cf3c16d9aff14f3a76b608")
    version("4.4.0", sha256="4a90be0f22ad81c987f5584661b60a594f1b21c581b82bfba3ae60f89ae44397")
    version("4.3.6", sha256="a41eaf6364f1377fe065d35671d9cf82bbbc8f21207819b2b9f33f652aec6f1b")
    version("4.3.5", sha256="eb95936bf15d2393c55dd505bc527d1d4408289cec5a9fa8abb99f7577e7f954")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("bind9", type="build")
