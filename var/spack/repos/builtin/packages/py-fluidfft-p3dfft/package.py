# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFluidfftP3dfft(PythonPackage):
    """Fluidfft MPI plugin using p3dfft."""

    pypi = "fluidfft-p3dfft/fluidfft_p3dfft-0.0.1.tar.gz"

    maintainers("paugier")
    license("CECILL-B", checked_by="paugier")

    version("0.0.1", sha256="1c291236a43045b9f8b9725e568277c5f405d2e2d9f811ba1bc9c5e1d9f2f827")

    with default_args(type=("build", "run")):
        depends_on("python@3.9:")
        depends_on("py-mpi4py")

    with default_args(type="link"):
        depends_on("p3dfft3")
        depends_on("fftw")

    with default_args(type="build"):
        depends_on("py-meson-python")
        depends_on("py-transonic@0.6.4:")
        depends_on("py-fluidfft-builder")
        depends_on("py-cython@3.0:")

    depends_on("py-fluidfft", type="run")
