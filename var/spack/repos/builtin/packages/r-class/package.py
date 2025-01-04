# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RClass(RPackage):
    """Functions for Classification.

    Various functions for classification, including k-nearest neighbour,
    Learning Vector Quantization and Self-Organizing Maps."""

    cran = "class"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("7.3-22", sha256="b6994164e93843fcc7e08dfdc8c8b4af6a5a10ef7153d2e72a6855342508d15c")
    version("7.3-21", sha256="0c19404aa4d2da61a62495e788b07c8e429c4c5ee64486ea5e6dd347bcaecddf")
    version("7.3-20", sha256="e65b046bc72b312ff0c5dc7feba4fa3e9bc63387274d44911493782b85f65483")
    version("7.3-19", sha256="7820ae94b22009561a69ed1f8b2ca2a3814be6a656e9884738206997caecbe37")
    version("7.3-17", sha256="be1f85b6df7556db93f50cb08106aac6620d4b5bb3fee846422863a022461313")
    version("7.3-15", sha256="f6bf33d610c726d58622b6cea78a808c7d6a317d02409d27c17741dfd1c730f4")
    version("7.3-14", sha256="18b876dbc18bebe6a00890eab7d04ef72b903ba0049d5ce50731406a82426b9c")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
