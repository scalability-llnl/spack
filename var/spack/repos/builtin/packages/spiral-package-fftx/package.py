# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SpiralPackageFftx(Package):
    """This is the SPIRAL package for FFTX:  FFTX is the exascale follow-on to
    the FFTW open source discrete FFT package for executing the Fast Fourier
    Transform as well as higher-level operations composed of linear operations
    combined with DFT transforms."""

    homepage = "https://spiralgen.com"
    url = "https://github.com/spiral-software/spiral-package-fftx/archive/refs/tags/1.3.0.tar.gz"
    git = "https://github.com/spiral-software/spiral-package-fftx.git"

    maintainers("spiralgen")
    # Although this package 'extends("spiral-software")' don't declare it as
    # such.  If this package is required spiral-software should be installed
    # with the +fftx variant active

    license("BSD-2-Clause-FreeBSD")

    version("develop", branch="develop")
    version("main", branch="main")
    version("1.3.0", sha256="f798165bd9a96b41262e889ca235d86dfda4e0fdc414bfb9b463c50ca86f480b")
    version("1.2.2", sha256="18dacc3f974c4bd58295be2ea61f8ae0aada9a239f27b93d7806df564612cf22")
    version("1.2.1", sha256="3f15aa5949c1b09eb59257cf1c5f6fcddc6e46f77ae9d5fce8acd8b9f99ce941")
    version("1.1.1", sha256="99ec7fab9274d378524b4933917fae23f9590255518c7a124cb46bd5e8d9af37")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # FFTX package is an extension for Spiral (spec: spiral-software).

    def install(self, spec, prefix):
        spiral_pkgs = join_path(prefix, "namespaces", "packages", "fftx")
        install_tree(".", spiral_pkgs)
