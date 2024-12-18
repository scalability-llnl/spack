# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MountPointAttributes(AutotoolsPackage):
    """Library to turn expensive, non-scalable file system calls into simple
    string comparison operations."""

    homepage = "https://github.com/LLNL/MountPointAttributes"
    url = "https://github.com/LLNL/MountPointAttributes/files/2270601/mountpointattr-1.1.tar.gz"
    git = "https://github.com/LLNL/MountPointAttributes.git"
    maintainers("lee218llnl")

    version("master", branch="master")
    version(
        "1.1.1",
        sha256="c58967fde59974407b4fee3e490b2e7d922d947e726faf2291c6c886b95abf78",
        url="https://github.com/LLNL/MountPointAttributes/releases/download/v1.1.1/mountpointattr-1.1.1.tar.gz",
    )
    version("1.1", sha256="bff84c75c47b74ea09b6cff949dd699b185ddba0463cb1ff39ab138003c96e02")

    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@master")

    patch("mpa_type_conversion.patch", when="@=1.1")
