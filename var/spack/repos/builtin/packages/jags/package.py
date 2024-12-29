# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jags(AutotoolsPackage):
    """JAGS is Just Another Gibbs Sampler.  It is a program for analysis of
    Bayesian hierarchical models using Markov Chain Monte Carlo (MCMC)
    simulation not wholly unlike BUGS"""

    tags = ["mcmc", "Gibbs-sampler"]

    homepage = "https://mcmc-jags.sourceforge.net/"
    url = "https://downloads.sourceforge.net/project/mcmc-jags/JAGS/4.x/Source/JAGS-4.2.0.tar.gz"

    license("GPL-2.0-or-later")

    version("4.3.2", sha256="871f556af403a7c2ce6a0f02f15cf85a572763e093d26658ebac55c4ab472fc8")
    version("4.3.0", sha256="8ac5dd57982bfd7d5f0ee384499d62f3e0bb35b5f1660feb368545f1186371fc")
    version("4.2.0", sha256="af3e9d2896d3e712f99e2a0c81091c6b08f096650af6aa9d0c631c0790409cf7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("blas")
    depends_on("lapack")

    def configure_args(self):
        args = [
            "--with-blas=%s" % self.spec["blas"].libs.ld_flags,
            "--with-lapack=%s" % self.spec["lapack"].libs.ld_flags,
        ]
        return args
