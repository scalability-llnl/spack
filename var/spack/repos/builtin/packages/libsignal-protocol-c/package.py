# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibsignalProtocolC(CMakePackage):
    """C library for the Signal protocol"""

    homepage = "https://signal.org/en/"
    url = "https://github.com/signalapp/libsignal-protocol-c/archive/refs/tags/v2.3.3.tar.gz"

    maintainers("pwablito")

    license("GPL-3.0-only")

    version("2.3.3", sha256="c22e7690546e24d46210ca92dd808f17c3102e1344cd2f9a370136a96d22319d")

    depends_on("c", type="build")  # generated
