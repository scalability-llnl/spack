# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFuture(RPackage):
    """The purpose of this package is to provide a lightweight and unified
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

    version('1.14.0', sha256='0a535010d97a01b21aaf9d863603e44359335e273019c1e1980bbb5b2917dbcb')

    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-globals@0.12.4:', type=('build', 'run'))
    depends_on('r-listenv@0.7.0:', type=('build', 'run'))
