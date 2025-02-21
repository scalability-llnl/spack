# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCubature(RPackage):
    """Adaptive multivariate integration over hypercubes.

    R wrappers around the cubature C library of Steven G. Johnson for adaptive
    multivariate integration over hypercubes and the Cuba C library of Thomas
    Hahn for deterministic and Monte Carlo integration. Scalar and vector
    interfaces for  cubature and Cuba routines are provided; the vector
    interfaces are highly recommended as demonstrated in the package
    vignette."""

    cran = "cubature"

    license("GPL-3.0-only")

    version("2.1.1", sha256="b37220e733f4e610e089e69896f66dc5bc461478a040321c19600ec5d07ea684")
    version("2.0.4.6", sha256="330c9dc2be9bf6815473fd40efa8c2de47c1ed286cb097d0ff846b56c9e9f95a")
    version("2.0.4.5", sha256="a81f118e5b7950a4a29e5509f8a40d7b87544fb25783917242000561379c9023")
    version("2.0.4.4", sha256="087b3b2c4f25d873fa95e9d38766a17a7201d03a6f4960f1e080a8db8b67d569")
    version("2.0.4.2", sha256="605bdd9d90fb6645359cccd1b289c5afae235b46360ef5bdd2001aa307a7694e")
    version("2.0.4.1", sha256="383fbdf49d1cdf760ad5d88d353e69118c7c663cde126c5bdd33b6fecc50d400")
    version("2.0.3", sha256="79bf03ebdb64b0de1ef19d24051b9d922df9310254bee459bb47764522407a73")
    version("2.0.2", sha256="641165c665ff490c523bccc05c42bb6851e42676b6b366b55fc442a51a8fbe8c")
    version("1.1-2", sha256="0a05469bdc85d6bd8165a42a3fc5c35a06700d279e4e8b3cf4669df19edffeed")

    depends_on("r-rcpp", type=("build", "run"), when="@2.0.3:")
    depends_on("gmake", type="build")

    parallel = False
