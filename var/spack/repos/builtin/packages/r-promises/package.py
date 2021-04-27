# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RPromises(RPackage):
    """Abstractions for Promise-Based Asynchronous Programming

    Provides fundamental abstractions for doing asynchronous programming in
    R using promises. Asynchronous programming is useful for allowing a single
    R process to orchestrate multiple tasks in the background while also
    attending to something else. Semantics are similar to 'JavaScript'
    promises, but with a syntax that is idiomatic R."""

    homepage = "https://rstudio.github.io/promises"
    url      = "https://cloud.r-project.org/src/contrib/promises_1.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/promises"

    version('1.1.1', sha256='3718c6eb2c3362cbe89389e613118f783f9977dbf24757f85026e661199c5800')
    version('1.0.1', sha256='c2dbc7734adf009377a41e570dfe0d82afb91335c9d0ca1ef464b9bdcca65558')

    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-later', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
