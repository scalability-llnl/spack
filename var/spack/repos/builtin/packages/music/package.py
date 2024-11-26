# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Music(CMakePackage):
    """MUSIC (Multi-Scale Initial Conditions for Cosmological Simulations).

    Introduced in [Hahn and Abel][1].

    [1]: https://arxiv.org/abs/1103.6031
    """

    homepage = "https://www-n.oca.eu/ohahn/MUSIC/"
    git = "https://bitbucket.org/ohahn/music.git"

    maintainers("charmoniumQ")

    version("2021-12-01", commit="6747c54f3b73ec36719c265fd96362849a83cb45")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "hdf5",
        default=False,
        description=(
            "Compile with HDF5. Required by Some MUSIC output plug-ins "
            "(e.g., ENZO, Arepo and the MUSIC generic format"
        ),
    )
    variant("single_prec", default=False, description="Enable single-precision")

    depends_on("fftw@3:")
    depends_on("gsl")
    depends_on("hdf5", when="+hdf5")

    def cmake_args(self):
        return [self.define_from_variant("MUSIC_ENABLE_SINGLE_PRECISION", "single_prec")]

    def install(self, spec, prefix):
        music_exe = os.path.join(self.build_directory, "MUSIC")
        set_executable(music_exe)
        mkdirp(prefix.bin)
        install(music_exe, prefix.bin)
