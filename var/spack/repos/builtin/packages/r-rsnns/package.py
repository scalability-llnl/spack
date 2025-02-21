# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RRsnns(RPackage):
    """Neural Networks using the Stuttgart Neural Network Simulator (SNNS).

    The Stuttgart Neural Network Simulator (SNNS) is a library containing many
    standard implementations of neural networks. This package wraps the SNNS
    functionality to make it available from within R. Using the RSNNS low-level
    interface, all of the algorithmic functionality and flexibility of SNNS can
    be accessed. Furthermore, the package contains a convenient high-level
    interface, so that the most common neural network topologies and learning
    algorithms integrate seamlessly into R."""

    cran = "RSNNS"

    version("0.4-17", sha256="424557d7326889e09e31e04d2a9b7224bed0bb4aa6f9e5433d7ce4fe04a35afc")
    version("0.4-15", sha256="4a4286444f50b28fb6294b8b49250fa6c43c8fddf2ee0550a3ae59a4212ec1b3")
    version("0.4-14", sha256="7f6262cb2b49b5d5979ccce9ded9cbb2c0b348fd7c9eabc1ea1d31c51a102c20")
    version("0.4-12", sha256="b18dfeda71573bc92c6888af72da407651bff7571967965fd3008f0d331743b9")
    version("0.4-11", sha256="87943126e98ae47f366e3025d0f3dc2f5eb0aa2924508fd9ee9a0685d7cb477c")
    version("0.4-10.1", sha256="38bb3d172390bd01219332ec834744274b87b01f94d23b29a9d818c2bca04071")
    version("0.4-7", sha256="ec941dddda55e4e29ed281bd8768a93d65e0d86d56ecab0f2013c64c8d1a4994")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r-rcpp@0.8.5:", type=("build", "run"))
