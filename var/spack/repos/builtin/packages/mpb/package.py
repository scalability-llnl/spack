# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpb(AutotoolsPackage):
    """MPB is a free and open-source software package for computing
    electromagnetic band structures and modes."""

    homepage = "https://github.com/NanoComp/mpb"
    url = "https://github.com/NanoComp/mpb/archive/refs/tags/v1.11.1.tar.gz"

    license("GPL-2.0-only")

    version("1.11.1", sha256="7311fc525214c1184cad3e0626b8540c0b53b3c31c28e61ce6ec2860088eca46")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    depends_on("blas")
    depends_on("fftw-api")
    depends_on("guile")
    depends_on("hdf5")
    depends_on("libctl")

    def configure_args(self):
        spec = self.spec
        config_args = ["--enable-shared", "--enable-maintainer-mode"]
        config_args.append(
            "--with-libctl={0}".format(join_path(spec["libctl"].prefix.share, "libctl"))
        )
        return config_args
