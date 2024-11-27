# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gnuconfig(Package):
    """
    The GNU config.guess and config.sub scripts versioned by timestamp.
    This package can be used as a build dependency for autotools packages that
    ship a tarball with outdated config.guess and config.sub files.
    """

    homepage = "https://www.gnu.org/software/config/"
    git = "https://github.com/spack/gnuconfig.git"
    url = "https://github.com/spack/gnuconfig/releases/download/2021-08-14/gnuconfig-2021-08-14.tar.gz"
    tags = ["build-tools"]

    maintainers("haampie")

    version("master", branch="master")
    version(
        "2024-07-27", sha256="1135044961853c7f116145cee9bb15c3d29b1b081cf8293954efd0f05d801a7c"
    )
    version(
        "2022-09-17", sha256="95306801ad7086e6a6e13397cb859183d8b7adbba2e372ce0819bad5fcb919b7"
    )
    version(
        "2021-08-14", sha256="69b6d2868e70167ba1bdb9030b49beeb20f00b37e30825e83fd04291d96bc5f7"
    )

    def install(self, spec, prefix):
        with working_dir(self.stage.source_path):
            install("config.sub", prefix)
            install("config.guess", prefix)
