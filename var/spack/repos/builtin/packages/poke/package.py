# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Poke(AutotoolsPackage, GNUMirrorPackage):
    """ "The extensible editor for structured binary data"""

    homepage = "https://www.jemarch.net/poke.html"
    gnu_mirror_path = "poke/poke-1.0.tar.gz"

    maintainers("ChristianTackeGSI")

    license("GPL-3.0-or-later")

    version("3.1", sha256="f405a6ba810916ec717000b6fe98ef10cbe549bf0a366b3f81e1f176ff8ff13f")
    version("3.0", sha256="79a9b2f33c9f8c327c499afadaeeabfeecf6ad4988924d2c6c6f317e50317add")
    version("1.0", sha256="de930b8700c0772b3c2cd0d0ca35f50fd3d77bdf82c6251eb516b49e8ca25b0a")

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig")
    depends_on("readline")
    depends_on("bdw-gc")
    depends_on("json-c")

    build_directory = "spack-build"
