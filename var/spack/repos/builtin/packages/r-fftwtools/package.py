# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFftwtools(RPackage):
    """Provides a wrapper for several 'FFTW' functions. This package provides
       access to the two-dimensional 'FFT', the multivariate 'FFT', and the
       one-dimensional real to complex 'FFT' using the 'FFTW3' library. The
       package includes the functions fftw() and mvfftw() which are designed
       to mimic the functionality of the R functions fft() and mvfft().
       The 'FFT' functions have a parameter that allows them to not return
       the redundant complex conjugate when the input is real data."""

    homepage = "https://github.com/krahim/fftwtools"
    url      = "https://cloud.r-project.org/src/contrib/fftwtools_0.9-8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/fftwtools"

    version('0.9-8', sha256='4641c8cd70938c2a8bde0b6da6cf7f83e96175ef52f1ca42ec3920a1dabf1bdb')

    depends_on('r@2.15.2:', type=('build', 'run'))
    depends_on('fftw@3.1.2:')
