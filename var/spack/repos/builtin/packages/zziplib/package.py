# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.build_systems.autotools
import spack.build_systems.cmake
from spack.package import *


class Zziplib(AutotoolsPackage, CMakePackage):
    """The zziplib provides read access to zipped files in a zip-archive, using
    compression based solely on free algorithms provided by zlib.  It also
    provides a functionality to overlay the archive filesystem with the
    filesystem of the operating system environment."""

    homepage = "https://github.com/gdraheim/zziplib"
    url = "https://github.com/gdraheim/zziplib/archive/v0.13.69.tar.gz"

    version("0.13.78", sha256="feaeee7c34f18aa27bd3da643cc6a47d04d2c41753a59369d09102d79b9b0a31")
    version("0.13.72", sha256="93ef44bf1f1ea24fc66080426a469df82fa631d13ca3b2e4abaeab89538518dc")
    version("0.13.69", sha256="846246d7cdeee405d8d21e2922c6e97f55f24ecbe3b6dcf5778073a88f120544")

    depends_on("c", type="build")  # generated

    patch("python2to3.patch", when="@:0.13.69")

    # Switch to CMake from 0.13.70, first working release is 0.13.71
    build_system(
        conditional("cmake", when="@0.13.72:"),
        conditional("autotools", when="@:0.13.69"),
        default="cmake",
    )

    depends_on("python@3.5:", type="build", when="@0.13.72:")
    depends_on("python", type="build")
    depends_on("zlib-api")
    # see zzip/CMakeLists.txt
    depends_on("coreutils", type="build", when="@0.13.72:")
    depends_on("pkgconfig", type="build", when="@0.13.72:")
    depends_on("zip", type="build", when="@0.13.72:")
    depends_on("unzip", type="build", when="@0.13.72:")


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
    build_directory = "spack-build"
