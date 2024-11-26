# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFluidfftFftwmpi(PythonPackage):
    """Fluidfft plugin using fftwmpi."""

    pypi = "fluidfft-fftwmpi/fluidfft_fftwmpi-0.0.1.tar.gz"

    maintainers("paugier")
    license("CECILL-B", checked_by="paugier")

    version("0.0.1", sha256="af3c606852e991c2c1b3ea4f7558c69ab9138b713a7166a6eedf48ef1af660d3")

    with default_args(type=("build", "run")):
        extends("python@3.9:")
        depends_on("py-mpi4py")

    with default_args(type="link"):
        depends_on("fftw")

    with default_args(type="build"):
        depends_on("py-meson-python")
        depends_on("py-transonic@0.6.4:")
        depends_on("py-fluidfft-builder")
        depends_on("py-cython@3.0:")

    depends_on("py-fluidfft", type="run")
