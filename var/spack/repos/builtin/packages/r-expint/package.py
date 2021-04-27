# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RExpint(RPackage):
    """Exponential Integral and Incomplete Gamma Function

    The exponential integrals E_1(x), E_2(x), E_n(x) and Ei(x), and the
    incomplete gamma function G(a, x) defined for negative values of its first
    argument. The package also gives easy access to the underlying C routines
    through an API; see the package vignette for details. A test package
    included in sub-directory example_API provides an implementation. C
    routines derived from the GNU Scientific Library
    <https://www.gnu.org/software/gsl/>."""

    homepage = "https://cloud.r-project.org/package=expint"
    url      = "https://cloud.r-project.org/src/contrib/expint_0.1-5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/expint"

    version('0.1-6', sha256='c7d13a8e299a91e94622047fe22b0006137e7bf82e34d10871b631fa58115145')
    version('0.1-5', sha256='b03d60938cd6cf615aa3a02b1bf73436785eca89eaff56059ee0807b8244718a')

    depends_on('r@3.3.0:', type=('build', 'run'))
