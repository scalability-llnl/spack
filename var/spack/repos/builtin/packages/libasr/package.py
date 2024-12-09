# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libasr(AutotoolsPackage):
    """libasr is a free, simple and portable asynchronous resolver library."""

    homepage = "https://github.com/OpenSMTPD/libasr"
    url = "https://github.com/OpenSMTPD/libasr/releases/download/1.0.4/libasr-1.0.4.tar.gz"

    license("WTFPL")

    version("1.0.4", sha256="19fb6bed10d15c9775c8d008cd1130155917ae4e801c729fe85e6d88a545dab4")
    version("1.0.3", sha256="9cd88e0172e6d426438875e09229d1d473d56db546d02b630f9dd14db226d68d")

    depends_on("c", type="build")  # generated
