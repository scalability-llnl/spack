# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RReshape2(RPackage):
    """Flexibly Reshape Data: A Reboot of the Reshape Package.

    Flexibly restructure and aggregate data using just two functions: melt and
    dcast (or acast)."""

    cran = "reshape2"

    license("MIT")

    version("1.4.4", sha256="d88dcf9e2530fa9695fc57d0c78adfc5e361305fe8919fe09410b17da5ca12d8")
    version("1.4.3", sha256="8aff94c935e75032344b52407593392ddd4e16a88bb206984340c816d42c710e")
    version("1.4.2", sha256="6d3783610379be4c5676d9236cf66276a166b5b96c18f2759e9b219758959b6b")
    version("1.4.1", sha256="fbd49f75a5b0b7266378515af98db310cf6c772bf6e68bed01f38ee99b408042")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.1:", type=("build", "run"), when="@1.4.3:")
    depends_on("r-plyr@1.8.1:", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-stringr", type=("build", "run"))
