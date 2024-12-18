# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pal(AutotoolsPackage):
    """The PAL library is a partial re-implementation of Pat Wallace's
    popular SLALIB library written in C using a Gnu GPL license
    and layered on top of the IAU's SOFA library (or the BSD-licensed ERFA)
    where appropriate."""

    homepage = "https://github.com/Starlink/pal"
    url = "https://github.com/Starlink/pal/releases/download/v0.9.8/pal-0.9.8.tar.gz"

    license("LGPL-3.0-only")

    version("0.9.8", sha256="191fde8c4f45d6807d4b011511344014966bb46e44029a4481d070cd5e7cc697")

    depends_on("c", type="build")  # generated

    depends_on("sofa-c")
    depends_on("erfa")

    variant("starlink", default=False, description="Build with starlink support.")

    def configure_args(self):
        args = []
        if "~starlink" in self.spec:
            args.append("--without-starlink")
        return args
