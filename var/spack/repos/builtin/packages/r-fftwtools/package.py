# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFftwtools(RPackage):
    """Wrapper for 'FFTW3' Includes: One-Dimensional Univariate,
    One-Dimensional Multivariate, and Two-Dimensional Transform.

    Provides a wrapper for several 'FFTW' functions. This package provides
    access to the two-dimensional 'FFT', the multivariate 'FFT', and the
    one-dimensional real to complex 'FFT' using the 'FFTW3' library. The
    package includes the functions fftw() and mvfftw() which are designed to
    mimic the functionality of the R functions fft() and mvfft().  The 'FFT'
    functions have a parameter that allows them to not return the redundant
    complex conjugate when the input is real data."""

    cran = "fftwtools"

    license("GPL-2.0-or-later")

    version("0.9-11", sha256="f1f0c9a9086c7b2f72c5fb0334717cc917213a004eaef8448eab4940c9852c7f")
    version("0.9-9", sha256="a9273b7e495d228d740ab4525467e4bbefe8614bd2d97e7234017f1305f51441")
    version("0.9-8", sha256="4641c8cd70938c2a8bde0b6da6cf7f83e96175ef52f1ca42ec3920a1dabf1bdb")

    depends_on("c", type="build")  # generated

    depends_on("r@2.15.2:", type=("build", "run"))
    depends_on("r@3.0:", type=("build", "run"), when="@0.9-11:")
    depends_on("fftw@3.1.2:")
