# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFluidfftFftw(PythonPackage):
    """Fluidfft plugin using fftw."""

    pypi = "fluidfft_fftw/fluidfft_fftw-0.0.1.tar.gz"

    maintainers("paugier")
    license("CECILL-B", checked_by="paugier")

    version("0.0.1", sha256="59967846e1d976508db30ff65987e9c1e6c024ec9c095849608ee8913b96d3ff")

    with default_args(type=("build", "run")):
        depends_on("python@3.9:")

    with default_args(type="link"):
        depends_on("fftw")

    with default_args(type="build"):
        depends_on("py-meson-python")
        depends_on("py-transonic@0.6.4:")
        depends_on("py-fluidfft-builder")
        depends_on("py-cython@3.0:")

    depends_on("py-fluidfft", type="run")
