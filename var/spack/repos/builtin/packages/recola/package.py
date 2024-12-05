# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Recola(CMakePackage):
    """REcursive Computation of One-Loop Amplitudes:
    a fortran library for the perturbative computation of
    next-to-leading-order transition amplitudes in the
    Standard Model of particle physics."""

    tags = ["hep"]

    homepage = "https://recola.gitlab.io/recola2/"
    url = "https://gitlab.com/recola/recola2/-/archive/2.2.4/recola2-2.2.4.tar.gz"

    maintainers("vvolkl")

    variant("python", default=True, description="Build py-recola python bindings.")

    license("GPL-3.0-or-later")

    version("2.2.4", sha256="212ae6141bc5de38c50be3e0c6947a3b0752aeb463cf850c22cfed5e61b1a64b")
    version("2.2.3", sha256="8dc25798960c272434fcde93817ed92aad82b2a7cf07438bb4deb5688d301086")
    version("2.2.2", sha256="a64cf2b4aa213289dfab6e2255a77264f281cd0ac85f5e9770c82b815272c5c9")
    version("2.2.0", sha256="a64cf2b4aa213289dfab6e2255a77264f281cd0ac85f5e9770c82b815272c5c9")
    version(
        "1.4.3",
        url="https://recola.hepforge.org/downloads/?f=recola-1.4.3.tar.gz",
        sha256="f6a7dce6e1f09821ba919524f786557984f216c001ab63e7793e8aa9a8560ceb",
    )
    version(
        "1.4.0",
        url="https://recola.hepforge.org/downloads/?f=recola-1.4.0.tar.gz",
        sha256="dc7db5ac9456dda2e6c03a63ad642066b0b5e4ceb8cae1f2a13ab33b35caaba8",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("collier")
    depends_on("recola-sm")
    depends_on("python@3:", when="+python")

    def cmake_args(self):
        args = [
            self.define("static", True),
            self.define("collier_path", self.spec["collier"].prefix.lib.cmake),
            self.define("modelfile_path", self.spec["recola-sm"].prefix.lib.cmake),
            self.define_from_variant("with_python3", "python"),
        ]
        return args
