# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Harminv(AutotoolsPackage):
    """Harminv is a free program (and accompanying library) to solve the
    problem of harmonic inversion - given a discrete-time, finite-length
    signal that consists of a sum of finitely-many sinusoids (possibly
    exponentially decaying) in a given bandwidth, it determines the
    frequencies, decay constants, amplitudes, and phases of those sinusoids."""

    homepage = "https://github.com/NanoComp/harminv"
    url = "https://github.com/NanoComp/harminv/releases/download/v1.4.2/harminv-1.4.2.tar.gz"

    license("GPL-2.0-or-later")

    version("1.4.2", sha256="5a9a1bf710972442f065d0d62c62d0c4ec3da4a3696d7160a35602c9470bc7a2")
    version("1.4.1", sha256="e1b923c508a565f230aac04e3feea23b888b47d8e19b08816a97ee4444233670")

    depends_on("c", type="build")  # generated

    depends_on("blas")
    depends_on("lapack")

    def configure_args(self):
        spec = self.spec
        lapack = spec["lapack"].libs
        blas = spec["blas"].libs

        return [
            "--enable-shared",
            "--with-blas={0}".format(blas.ld_flags),
            "--with-lapack={0}".format(lapack.ld_flags),
        ]
