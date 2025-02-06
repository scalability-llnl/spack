# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFuture(RPackage):
    """Unified Parallel and Distributed Processing in R for Everyone.

    The purpose of this package is to provide a lightweight and unified Future
    API for sequential and parallel processing of R expression via futures. The
    simplest way to evaluate an expression in parallel is to use 'x %<-% {
    expression }' with 'plan(multiprocess)'. This package implements
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

    cran = "future"

    license("LGPL-2.1-or-later")

    version("1.34.0", sha256="5839d4fd1f8beb1b18b27a7c50c1eb2bb5d80acd926b1bce9323637c8b2dfa5d")
    version("1.32.0", sha256="d5bb74512d069745184dd580a36449dc0b50d95b1cbbbc1605db82de596f2f76")
    version("1.29.0", sha256="856d1fd51d2f998c6572490c49fdcc27e5f3e0c1ade75eecdbf64a2cd0954373")
    version("1.28.0", sha256="6fdda66acd9a255e5baa70ff5dacd3c57ab2ecc2d87fd6abeebdfb939c051bf6")
    version("1.26.1", sha256="a35c0bdae86265ebe86119231802b6fbf7b1d533b57cb423d8483fbe779390d5")
    version("1.24.0", sha256="7b8b212ba0e9d6303bfc15c512e6cf9b5db3a7aa0b2462d2e15cdd84dd09b276")
    version("1.23.0", sha256="d869c80e837c0937a414b8050deff081aefeac586b796f3d634d64f0f4fdb8f8")
    version("1.22.1", sha256="87b24a85caf08e1d809eab28f9258444105cd7788eee2e3e2f21727ba3bbedcd")
    version("1.21.0", sha256="909e6602068eba543a6d2e464b911123cc29efdb600a7000eff0e5624ff0d12d")
    version("1.14.0", sha256="0a535010d97a01b21aaf9d863603e44359335e273019c1e1980bbb5b2917dbcb")

    depends_on("r-digest", type=("build", "run"))
    depends_on("r-globals@0.12.4:", type=("build", "run"))
    depends_on("r-globals@0.13.1:", type=("build", "run"), when="@1.21.0:")
    depends_on("r-globals@0.14.0:", type=("build", "run"), when="@1.22.0:")
    depends_on("r-globals@0.15.0:", type=("build", "run"), when="@1.26.1:")
    depends_on("r-globals@0.16.0:", type=("build", "run"), when="@1.28.0:")
    depends_on("r-globals@0.16.1:", type=("build", "run"), when="@1.29.0:")
    depends_on("r-listenv@0.7.0:", type=("build", "run"))
    depends_on("r-listenv@0.8.0:", type=("build", "run"), when="@1.21.0:")
    depends_on("r-parallelly@1.21.0:", type=("build", "run"), when="@1.21.0:")
    depends_on("r-parallelly@1.26.1:", type=("build", "run"), when="@1.22.0:")
    depends_on("r-parallelly@1.30.0:", type=("build", "run"), when="@1.24.0:")
    depends_on("r-parallelly@1.32.1:", type=("build", "run"), when="@1.28.0:")
    depends_on("r-parallelly@1.34.0:", type=("build", "run"), when="@1.32.0:")
    depends_on("r-parallelly@1.38.0:", type=("build", "run"), when="@1.34.0:")
