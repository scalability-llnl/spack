# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mcl(AutotoolsPackage):
    """The MCL algorithm is short for the Markov Cluster Algorithm, a fast
    and scalable unsupervised cluster algorithm for graphs (also known
    as networks) based on simulation of (stochastic) flow in graphs."""

    homepage = "https://www.micans.org/mcl/index.html"
    url = "https://www.micans.org/mcl/src/mcl-14-137.tar.gz"

    license("GPL-3.0-or-later")

    version("14-137", sha256="b5786897a8a8ca119eb355a5630806a4da72ea84243dba85b19a86f14757b497")

    depends_on("c", type="build")  # generated

    @when("%gcc@10:")
    def patch(self):
        filter_file("^dim", "extern dim", "src/impala/iface.h")
        filter_file("^double", "extern double", "src/impala/iface.h")

    depends_on("perl", type="run")

    variant("blast", default=False, description="Build bio-informatics tools.")

    def configure_args(self):
        args = []

        if "+blast" in self.spec:
            args.append("--enable-blast")

        return args
