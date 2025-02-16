# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RRjags(RPackage):
    """Bayesian Graphical Models using MCMC.

    Interface to the JAGS MCMC library."""

    cran = "rjags"

    license("GPL-2.0-only")

    version("4-16", sha256="369d393e519ae26219ff44e6a8f07d9310a9bb06fa0ec9dcce33ce7c4bc7e7e7")
    version("4-14", sha256="313b5df702598ce3bbc5f8b027b654c8489420ca5a4e0a794954ea9f4837e2cb")
    version("4-13", sha256="f85cc34c5127b828d8a3fa3613ef29f147c868bdaf55eb0f7406c10abbf92b32")
    version("4-12", sha256="b91f34c3f9ebf78fa44bd661346fbb6f28a01693a7203ac133c98392dd273e10")
    version("4-10", sha256="bd3e0bdf50b23b63061a0caa2428be585ccbf0b3f5d28eaa690e714e508d0ada")
    version("4-8", sha256="1529827ab11493fb5f05552e239d700ae2f818995d86d3c9e4c92523f594b59f")
    version("4-6", sha256="cf24bb1e7c8445bafb49097089ad33e5bd5d8efbccf16fc7e32ad230f05f89ad")

    depends_on("r@2.14.0:", type=("build", "run"))
    depends_on("r-coda@0.13:", type=("build", "run"))
    depends_on("jags@4.0.0:4.999.999", type=("link"))

    def configure_args(self):
        args = [
            "--with-jags-lib=%s" % self.spec["jags"].prefix.lib,
            "--with-jags-include=%s" % self.spec["jags"].prefix.include,
            "--with-jags-modules=%s/JAGS/modules-4" % self.spec["jags"].prefix.lib,
        ]
        return args
