# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mcpp(AutotoolsPackage, SourceforgePackage):
    """MCPP is an alternative C/C++ preprocessor with the highest
    conformance."""

    homepage = "https://sourceforge.net/projects/mcpp/"
    sourceforge_mirror_path = "mcpp/mcpp/V.2.7.2/mcpp-2.7.2.tar.gz"
    git = "https://github.com/jbrandwood/mcpp.git"

    # Versions from `git describe --tags`
    version("2.7.2-25-g619046f", commit="619046fa0debac3f86ff173098aeb59b8f051d19")
    version("2.7.2", sha256="3b9b4421888519876c4fc68ade324a3bbd81ceeb7092ecdbbc2055099fcb8864")

    depends_on("c", type="build")

    def configure_args(self):
        config_args = ["--enable-mcpplib", "--disable-static"]
        return config_args
