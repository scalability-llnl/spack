# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFluidfftPfft(PythonPackage):
    """Fluidfft MPI plugin using pfft."""

    pypi = "fluidfft-pfft/fluidfft_pfft-0.0.1.tar.gz"

    maintainers("paugier")
    license("CECILL-B", checked_by="paugier")

    version("0.0.1", sha256="ef8255bd78c9d2dbfb11715542b221d457eedfa0a5b0bbdd1b95e8fbe64043c5")

    with default_args(type=("build", "run")):
        depends_on("python@3.9:")
        depends_on("py-mpi4py")

    with default_args(type="link"):
        depends_on("fftw")
        depends_on("pfft")

    with default_args(type="build"):
        depends_on("py-meson-python")
        depends_on("py-transonic@0.6.4:")
        depends_on("py-fluidfft-builder")
        depends_on("py-cython@3.0:")

    depends_on("py-fluidfft", type="run")
