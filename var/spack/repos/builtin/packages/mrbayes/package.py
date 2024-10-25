# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mrbayes(AutotoolsPackage):
    """MrBayes is a program for Bayesian inference and model choice across a
    wide range of phylogenetic and evolutionary models. MrBayes uses Markov
    chain Monte Carlo (MCMC) methods to estimate the posterior distribution
    of model parameters."""

    homepage = "https://mrbayes.sourceforge.net"
    url = "https://github.com/NBISweden/MrBayes/releases/download/v3.2.7a/mrbayes-3.2.7a.tar.gz"

    license("GPL-3.0-or-later")

    version("3.2.7a", sha256="1a4670be84e6b968d59382328294db4c8ceb73e0c19c702265deec6f2177815c")
    version("3.2.7", sha256="39d9eb269969b501268d5c27f77687c6eaa2c71ccf15c724e6f330fc405f24b9")

    depends_on("c", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI parallel support")
    variant("beagle", default=True, description="Enable BEAGLE library for speed benefits")
    variant(
        "readline", default=False, description="Enable readline library, not recommended with MPI"
    )

    conflicts("+readline", when="+mpi", msg="MPI and readline support are exclusive")

    depends_on("libbeagle", when="+beagle")
    depends_on("mpi", when="+mpi")
    depends_on("readline", when="+readline")

    def configure_args(self):
        args = []
        if "~beagle" in self.spec:
            args.append("--with-beagle=no")
        else:
            args.append("--with-beagle=%s" % self.spec["libbeagle"].prefix)
        if "+readline" in self.spec:
            args.append("--with-readline=yes")
        else:
            args.append("--with-readline=no")
        if "~mpi" in self.spec:
            args.append("--with-mpi=no")
        else:
            args.append("--with-mpi=yes")
        return args

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir("src"):
            install("mb", prefix.bin)
