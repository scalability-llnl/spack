# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Idg(CMakePackage):
    """
    Image Domain Gridding (IDG) is a fast method for convolutional resampling (gridding/degridding)
    of radio astronomical data (visibilities). Direction-dependent effects (DDEs)
    or A-tems can be applied in the gridding process.
    """

    homepage = "https://www.astron.nl/citt/IDG/"
    git = "https://git.astron.nl/RD/idg.git"
    url = "https://git.astron.nl/RD/idg/-/archive/1.2.0/idg-1.2.0.tar.gz"

    maintainers("pelahi")

    license("GPL-3.0-or-later")

    version("1.2.0", commit="ccf8951283c12547326800adae99440c70177449")
    version("1.0.0", commit="3322756fb8b6e3bb1fe5293f3e07e40623ff8486")
    version("0.8.1", commit="a09f3c85094c592f9304fff4c31e920c7592c3c3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("boost")
    depends_on("fftw-api@3")
    depends_on("blas")
