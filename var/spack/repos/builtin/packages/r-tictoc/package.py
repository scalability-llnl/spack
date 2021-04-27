# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTictoc(RPackage):
    """tictoc: Functions for timing R scripts, as well as implementations of
    Stack and List structures

    This package provides the timing functions 'tic' and 'toc'
    that can be nested. One can record all timings while a
    complex script is running, and examine the values later. It
    is also possible to instrument the timing calls with custom
    callbacks. In addition, this package provides class
    'Stack', implemented as a vector, and class 'List',
    implemented as a list, both of which support operations
    'push', 'pop', 'first', 'last' and 'clear'."""

    homepage = "https://collectivemedia.github.io/tictoc/"
    url      = "https://cloud.r-project.org/src/contrib/tictoc_1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tictoc"

    version('1.0', sha256='47da097c1822caa2d8e262381987cfa556ad901131eb96109752742526b2e2fe')

    depends_on('r@3.0.3:', type=('build', 'run'))
