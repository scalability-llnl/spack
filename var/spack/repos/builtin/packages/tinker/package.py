# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Tinker(CMakePackage):
    """The Tinker molecular modeling software is a complete and general
    package for molecular mechanics and dynamics, with some special
    features for biopolymers.
    """

    homepage = "https://dasher.wustl.edu/tinker/"
    url = "https://dasher.wustl.edu/tinker/downloads/tinker-8.7.1.tar.gz"

    version("8.7.2", sha256="f9e94ae0684d527cd2772a4a7a05c41864ce6246f1194f6c1c402a94598151c2")
    version(
        "8.7.1",
        sha256="0d6eff8bbc9be0b37d62b6fd3da35bb5499958eafe67aa9c014c4648c8b46d0f",
        deprecated=True,
    )

    patch("tinker-8.7.1-cmake.patch")

    depends_on("fftw")

    root_cmakelists_dir = "source"
