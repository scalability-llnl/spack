# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRcppparallel(RPackage):
    """Parallel Programming Tools for 'Rcpp'

    High level functions for parallel programming with 'Rcpp'. For example,
    the 'parallelFor()' function can be used to convert the work of a standard
    serial "for" loop into a parallel one and the 'parallelReduce()' function
    can be used for accumulating aggregate or other values."""

    homepage = "http://rcppcore.github.io/RcppParallel"
    url      = "https://cloud.r-project.org/src/contrib/RcppParallel_4.4.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RcppParallel"

    version('5.0.2', sha256='8ca200908c6365aafb2063be1789f0894969adc03c0f523c6cc45434b8236f81')
    version('4.4.3', sha256='7a04929ecab97e46c0b09fe5cdbac9d7bfa17ad7d111f1a9787a9997f45fa0fa')

    depends_on('r@3.0.2:', type=('build', 'run'))
    depends_on('gmake', type='build')

    patch('asclang.patch', when='%fj')
