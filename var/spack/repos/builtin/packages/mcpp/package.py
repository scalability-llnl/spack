# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mcpp(AutotoolsPackage, SourceforgePackage):
    """MCPP is an alternative C/C++ preprocessor with the highest
    conformance."""

    homepage = "https://sourceforge.net/projects/mcpp/"
    sourceforge_mirror_path = "mcpp/mcpp/V.2.7.2/mcpp-2.7.2.tar.gz"

    version("2.7.2", sha256="3b9b4421888519876c4fc68ade324a3bbd81ceeb7092ecdbbc2055099fcb8864")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def configure_args(self):
        config_args = ["--enable-mcpplib", "--disable-static"]
        return config_args
