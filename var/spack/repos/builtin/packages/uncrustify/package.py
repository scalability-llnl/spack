# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Uncrustify(CMakePackage, AutotoolsPackage):
    """Source Code Beautifier for C, C++, C#, ObjectiveC, Java, and others."""

    homepage = "https://uncrustify.sourceforge.net/"
    git = "https://github.com/uncrustify/uncrustify"
    url = "https://sourceforge.net/projects/uncrustify/files/uncrustify/uncrustify-0.69/uncrustify-0.69.tar.gz"

    maintainers("gmaurel")

    license("GPL-2.0-or-later")

    version("master", branch="master")
    version("0.74", commit="62048b01507304653ea98a74b31e0edbadaf7496")
    version("0.73", commit="25b765b4ccf1fc50302df3779188ccd402962ee0")
    version("0.72", commit="1d3d8fa5e81bece0fac4b81316b0844f7cc35926")
    version("0.71", commit="64d82fd66f9eeeba14a591aa0939d495eccd1bc6")
    version("0.70", commit="51f64d6e62f5ea84f2c428c0478d01b1fbf6948c")
    version("0.69", commit="a7a8fb35d653e0b49e1c86f2eb8a2970025d5989")
    version("0.68", commit="86bc346e01c16c96e4baff8132e024ca13772ce9")
    version("0.67", commit="00321aa37802ae9ae78459957498a3c933b8254f")
    version("0.66", commit="80f549b6f026d0b4cf14eae3a1ba8a7389642e45")
    version("0.65", commit="9056763eb1c8c3837fd718eba03facdd4d8c179d")
    version("0.64", commit="1d7d97fb637dcb05ebc5fe57ee1020e2a659210d")
    version("0.63", commit="44ce0f156396b79ddf3ed9242023a14e9665b76f")
    version("0.62", commit="5987f2223f16b993dbece1360363eef9515fe5e8")
    version("0.61", sha256="1df0e5a2716e256f0a4993db12f23d10195b3030326fdf2e07f8e6421e172df9")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    build_system(
        conditional("cmake", when="@0.64:"),
        conditional("autotools", when="@:0.63"),
        default="cmake",
    )

    with when("build_system=autotools"):
        depends_on("automake", type="build")
        depends_on("autoconf", type="build")
        depends_on("libtool", type="build", when="@0.63")

    patch("uncrustify-includes.patch", when="@0.73")
