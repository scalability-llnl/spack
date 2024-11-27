# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fullock(AutotoolsPackage):
    """FULLOCK is a lock library provided by Yahoo! JAPAN,
    that is very fast and runs on user level.This library
    provides two lock type."""

    homepage = "https://antpick.ax/"
    url = "https://github.com/yahoojapan/fullock/archive/v1.0.36.tar.gz"

    license("MIT")

    version("1.0.59", sha256="6e1758f52d438b365c439d3518cae47df5334fd73adbd781c932497d2aaaafca")
    version("1.0.50", sha256="7222976883289376c1b88fd30ecd3ab2f055316103b97df4aa71192954072848")
    version("1.0.39", sha256="0089d4446e3102b5de39e3d18c1b7e5c9567deb77a4e60963e15b5c1b23a594d")
    version("1.0.36", sha256="68d0dc9036c2c1871653b4626a594f57663973c159f083ec68647c60ddc919f7")
    version("1.0.35", sha256="613462155271bf7b90ce745bafb47d23855e1b4813d3b6caa238efffb7c42841")
    version("1.0.34", sha256="6f4c901e5b08f5e82365539cb9c0dbab82529175912f6203a82509a583553021")
    version("1.0.33", sha256="31a292e50553abf71058b47277dbca37d25a772cf99c0f99c85e56dfcd11edb2")
    version("1.0.32", sha256="57d4ca06e5b88a98745062f55ee5ce37c88a49d59d58d09c5178fa1eee4d8353")

    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")
