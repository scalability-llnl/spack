# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Mscgen(AutotoolsPackage):
    """Mscgen is a small program that parses Message Sequence Chart descriptions
    and produces PNG, SVG, EPS or server side image maps (ismaps) as the
    output."""

    homepage = "https://www.mcternan.me.uk/mscgen/"
    url = "https://www.mcternan.me.uk/mscgen/software/mscgen-src-0.20.tar.gz"

    version("0.20", sha256="3c3481ae0599e1c2d30b7ed54ab45249127533ab2f20e768a0ae58d8551ddc23")

    depends_on("c", type="build")  # generated

    depends_on("flex")
    depends_on("bison")
    depends_on("pkgconfig")
    depends_on("libgd")
