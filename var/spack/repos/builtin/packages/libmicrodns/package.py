# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmicrodns(MesonPackage):
    """Minimal mDNS resolver (and announcer) cross-platform library."""

    homepage = "https://github.com/videolabs/libmicrodns/"
    url = "https://github.com/videolabs/libmicrodns/releases/download/0.2.0/microdns-0.2.0.tar.xz"

    license("LGPL-2.1-or-later")

    version("0.2.0", sha256="2da28e7dda4861d76f797f92ac3e6c3e048333b95f9e4fc3a6548ad8afd8c446")
    version("0.1.2", sha256="666c4b9d86b5b3c37357bb78453c7e8b72cd65ade22d0a7963bfbefe51509b5c")
    version("0.1.1", sha256="498c81fd07718f449267a207948536cbb527610942d91999488eaea6de301c52")

    depends_on("c", type="build")  # generated
