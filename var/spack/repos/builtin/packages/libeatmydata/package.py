# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libeatmydata(AutotoolsPackage):
    """libeatmydata is a small LD_PRELOAD library designed to (transparently)
    disable fsync (and friends, like open(O_SYNC)). This has two side-effects:
    making software that writes data safely to disk a lot quicker and making
    this software no longer crash safe."""

    homepage = "https://www.flamingspork.com/projects/libeatmydata/"
    url = "https://www.flamingspork.com/projects/libeatmydata/libeatmydata-105.tar.gz"

    license("GPL-3.0-or-later")

    version("131", sha256="cf18a8c52138a38541be3478af446c06048108729d7e18476492d62d54baabc4")
    version("105", sha256="bdd2d068b6b27cf47cd22aa4c5da43b3d4a05944cfe0ad1b0d843d360ed3a8dd")

    depends_on("c", type="build")  # generated

    depends_on("strace", type="test")

    def check(self):
        # Tests must run in serial
        make("check", parallel=False)
