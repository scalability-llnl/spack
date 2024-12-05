# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libndp(AutotoolsPackage):
    """Libndp - Library for Neighbor Discovery Protocol"""

    homepage = "http://www.libndp.org/"
    url = "https://github.com/jpirko/libndp/archive/v1.7.tar.gz"

    license("LGPL-2.1-or-later")

    version("1.7", sha256="44be73630ee785ed9f571f9aaaeba0e1d375fa337fd841270034c813b5b0e6fd")
    version("1.6", sha256="565d6c4167f83ec697c762ea002f23e8f0b00828d0749b1ce928f068543e5aad")
    version("1.5", sha256="42c0a8938d4302c72a42e2d954deef7e4903bb3974da6804a929a3cd0b5b6aa7")
    version("1.4", sha256="b9b23d14e9b2d87745810d9d0e956e9fb45f44e794b1629492850c5a8fbbb083")
    version("1.3", sha256="e933dc1b9ce85089de8ba0f6ba4c3ec47eba0e9a404e14c1789a6fa9e23793f6")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
