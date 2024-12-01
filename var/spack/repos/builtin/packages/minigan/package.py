# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Minigan(Package):
    """miniGAN is a generative adversarial network code developed as part of the
    Exascale Computing Project's (ECP) ExaLearn project at
    Sandia National Laboratories."""

    homepage = "https://github.com/SandiaMLMiniApps/miniGAN"
    url = "https://github.com/SandiaMLMiniApps/miniGAN/archive/1.0.0.tar.gz"

    license("BSD-3-Clause")

    version("1.0.0", sha256="ef6d5def9c7040af520acc64b7a8b6c8ec4b7901721b11b0cb25a583ea0c8ae3")

    depends_on("python", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-torch", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-horovod@master", type=("build", "run"))
    depends_on("py-torchvision", type=("build", "run"))
    depends_on("py-matplotlib@3.0.0", type=("build", "run"))

    def install(self, spec, prefix):
        install_tree(".", prefix)
