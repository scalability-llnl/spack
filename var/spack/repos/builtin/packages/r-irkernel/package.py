# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RIrkernel(RPackage):
    """Native R Kernel for the 'Jupyter Notebook'.

    The R kernel for the 'Jupyter' environment executes R code which the
    front-end ('Jupyter Notebook' or other front-ends) submits to the kernel
    via the network."""

    cran = "IRkernel"

    version("1.3.2", sha256="e1c6d8bddc23e5039dd9c537feb371f937d60028fb753b90345698c58ae424a6")
    version("1.3.1", sha256="3186e3a177c7246d45218af55f8b10836540e68a2d106858a0385f7d741b640c")
    version("1.3", sha256="5a7fcbfd978dfb3cca6702a68a21c147551995fc400084ae8382ffcbbdae1903")
    version("1.2", sha256="5fb4dbdb741d05043120a8be0eb73f054b607d9854f314bd79cfec08d219ff91")
    version(
        "0.7",
        git="https://github.com/IRkernel/IRkernel.git",
        commit="9cdd284e03eb42d03fab18544b81f486852d5fe0",
        deprecated=True,
    )

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r-repr@0.4.99:", type=("build", "run"))
    depends_on("r-evaluate@0.10:", type=("build", "run"))
    depends_on("r-irdisplay@0.3.0.9999:", type=("build", "run"))
    depends_on("r-pbdzmq@0.2-1:", type=("build", "run"))
    depends_on("r-crayon", type=("build", "run"))
    depends_on("r-jsonlite@0.9.6:", type=("build", "run"))
    depends_on("r-uuid", type=("build", "run"))
    depends_on("r-digest", type=("build", "run"))
    depends_on("py-jupyter-client", type="run")

    depends_on("r-evaluate@0.5.4:", type=("build", "run"), when="@0.7")
    depends_on("r-devtools", type=("build", "run"), when="@0.7")
