# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFluidfftMpiWithFftw(PythonPackage):
    """Fluidfft MPI plugin using fftw."""

    pypi = "fluidfft-mpi_with_fftw/fluidfft_mpi_with_fftw-0.0.1.tar.gz"

    maintainers("paugier")
    license("CECILL-B", checked_by="paugier")

    version("0.0.1", sha256="ab8c1867e745715892f8d30c9409e9509467a610f5a702ac7b5cfa003787f6ce")

    with default_args(type=("build", "run")):
        depends_on("python@3.9:")
        depends_on("py-mpi4py")

    with default_args(type="link"):
        depends_on("fftw")

    with default_args(type="build"):
        depends_on("py-meson-python")
        depends_on("py-transonic@0.6.4:")
        depends_on("py-fluidfft-builder")
        depends_on("py-cython@3.0:")

    depends_on("py-fluidfft", type="run")
