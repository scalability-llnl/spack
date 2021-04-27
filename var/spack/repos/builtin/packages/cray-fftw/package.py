# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class CrayFftw(Package):
    """FFTW is a C subroutine library for computing the discrete Fourier
       transform (DFT) in one or more dimensions, of arbitrary input
       size, and of both real and complex data (as well as of even/odd
       data, i.e. the discrete cosine/sine transforms or DCT/DST).
       This package is a wrapper for Cray's version of FFTW.

       To install this package, list it as an external package in packages.yaml,
       and make sure to load the correct cray-fftw module. In some cases you
       need to load cray-mpich before cray-fftw.
       """

    homepage = "https://docs.nersc.gov/development/libraries/fftw/"
    has_code = False    # Skip attempts to fetch source that is not available

    maintainers = ['haampie']

    version('3.3.8.8')
    version('3.3.8.7')

    provides('fftw-api@3')

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format('{name} is not installable, you need to specify '
                             'it as an external package in packages.yaml'))
