# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libpcap(AutotoolsPackage):
    """libpcap is a portable library in C/C++ for packet capture."""

    homepage = "https://www.tcpdump.org/"
    list_url = "https://www.tcpdump.org/release/"
    url = "https://www.tcpdump.org/release/libpcap-1.8.1.tar.gz"
    git = "https://github.com/the-tcpdump-group/libpcap"

    license("BSD-3-Clause", checked_by="wdconinc")

    version("1.10.5", sha256="37ced90a19a302a7f32e458224a00c365c117905c2cd35ac544b6880a81488f0")
    version("1.10.4", sha256="ed19a0383fad72e3ad435fd239d7cd80d64916b87269550159d20e47160ebe5f")
    version("1.10.3", sha256="2a8885c403516cf7b0933ed4b14d6caa30e02052489ebd414dc75ac52e7559e6")
    version("1.10.0", sha256="8d12b42623eeefee872f123bd0dc85d535b00df4d42e865f993c40f7bfc92b1e")
    version("1.9.1", sha256="635237637c5b619bcceba91900666b64d56ecb7be63f298f601ec786ce087094")
    version("1.8.1", sha256="673dbc69fdc3f5a86fb5759ab19899039a8e5e6c631749e48dcd9c6f0c83541e")

    depends_on("c", type="build")
    depends_on("flex", type="build")
    depends_on("bison", type="build")
