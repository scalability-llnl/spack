# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cereal(CMakePackage):
    """cereal is a header-only C++11 serialization library. cereal takes
    arbitrary data types and reversibly turns them into different
    representations, such as compact binary encodings, XML, or
    JSON. cereal was designed to be fast, light-weight, and easy to
    extend - it has no external dependencies and can be easily bundled
    with other code or used standalone.

    """

    homepage = "https://uscilab.github.io/cereal/"
    url = "https://github.com/USCiLab/cereal/archive/v1.3.2.tar.gz"

    license("BSD-3-Clause")

    version("1.3.2", sha256="16a7ad9b31ba5880dac55d62b5d6f243c3ebc8d46a3514149e56b5e7ea81f85f")
    version("1.3.1", sha256="65ea6ddda98f4274f5c10fb3e07b2269ccdd1e5cbb227be6a2fd78b8f382c976")
    version("1.3.0", sha256="329ea3e3130b026c03a4acc50e168e7daff4e6e661bc6a7dfec0d77b570851d5")
    version("1.2.2", sha256="1921f26d2e1daf9132da3c432e2fd02093ecaedf846e65d7679ddf868c7289c4")
    version("1.2.1", sha256="7d321c22ea1280b47ddb06f3e9702fcdbb2910ff2f3df0a2554804210714434e")
    version("1.2.0", sha256="1ccf3ed205a7a2f0d6a060415b123f1ae0d984cd4435db01af8de11a2eda49c1")
    version("1.1.2", sha256="45607d0de1d29e84d03bf8eecf221eb2912005b63f02314fbade9fbabfd37b8d")
    version("1.1.1", sha256="ec5e2b2c8f145d86eb7c079300360bb06f708527187834f3f127e9a12b07e9cf")
    version("1.1.0", sha256="69113debdac9de561f499af4cf7755b2e8c3afa92649b8178b34a7c6bbe4f12f")
    version("1.0.0", sha256="51c31c84d4c9e410e56d8bfc3424076b3234f11aa349ac8cda3db9f18118c125")
    version("0.9.1", sha256="2a99722df9c3d0f75267f732808a4d7e564cb5a35318a3d1c00086e2ef139385")

    depends_on("cxx", type="build")  # generated

    patch("Boost.patch", when="@:1.3.0")
    patch("Boost2.patch", when="@1.2.2:1.3.0")
    patch("pointers.patch")
    # fixed in HEAD but not released yet
    patch("LockGuard-default-ctor.patch", when="@:1.3.0")

    depends_on("cmake@2.6.2:", type="build")
    depends_on("cmake@3.6.0:", when="@1.3.0:", type="build")

    def cmake_args(self):
        # Boost is only used for self-tests, which we are not running (yet?)
        return [
            "-DCMAKE_DISABLE_FIND_PACKAGE_Boost=TRUE",
            "-DSKIP_PORTABILITY_TEST=TRUE",
            "-DJUST_INSTALL_CEREAL=On",
            "-DWITH_WERROR=Off",
        ]
