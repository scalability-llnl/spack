# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RFuture(RPackage):
    """Unified Parallel and Distributed Processing in R for Everyone

    The purpose of this package is to provide a lightweight and unified
    Future API for sequential and parallel processing of R expression via
    futures. The simplest way to evaluate an expression in parallel is to use
    'x %<-% { expression }' with 'plan(multiprocess)'. This package implements
    sequential, multicore, multisession, and cluster futures. With these, R
    expressions can be evaluated on the local machine, in parallel a set of
    local machines, or distributed on a mix of local and remote machines.
    Extensions to this package implement additional backends for processing
    futures via compute cluster schedulers etc. Because of its unified API,
    there is no need to modify any code in order switch from sequential on the
    local machine to, say, distributed processing on a remote compute cluster.
    Another strength of this package is that global variables and functions are
    automatically identified and exported as needed, making it straightforward
    to tweak existing code to make use of futures."""

    homepage = "https://github.com/HenrikBengtsson/future"
    url      = "https://cloud.r-project.org/src/contrib/future_1.14.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/future"

    version('1.21.0', sha256='909e6602068eba543a6d2e464b911123cc29efdb600a7000eff0e5624ff0d12d')
    version('1.14.0', sha256='0a535010d97a01b21aaf9d863603e44359335e273019c1e1980bbb5b2917dbcb')

    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-globals@0.12.4:', type=('build', 'run'))
    depends_on('r-globals@0.13.1:', when='@1.21.0:', type=('build', 'run'))
    depends_on('r-listenv@0.7.0:', type=('build', 'run'))
    depends_on('r-listenv@0.8.0:', when='@1.21.0:', type=('build', 'run'))
    depends_on('r-parallelly@1.21.0:', when='@1.21.0:', type=('build', 'run'))
