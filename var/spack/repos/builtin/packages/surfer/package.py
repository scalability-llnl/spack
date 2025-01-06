# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Surfer(CargoPackage):
    """A waveform viewer with a focus on a snappy usable interface, and extensibility."""

    homepage = "https://surfer-project.org"
    url = "https://gitlab.com/surfer-project/surfer/-/archive/v0.3.0/surfer-v0.3.0.tar.gz"
    git = "https://gitlab.com/surfer-project/surfer.git"

    maintainers("davekeeshan")

    license("EUPL-1.2")

    version("main", branch="main", submodules=True)

    version(
        "0.3.0", tag="v0.3.0", commit="1a6b34c44ea0e5089bd55d0bce1297aa1a02e6ef", submodules=True
    )

    depends_on("rust@1.82:")
    depends_on("c", type="build")
    depends_on("openssl")

    def build(self, spec, prefix):
        cargo("build", "--release")

    def install(self, spec, prefix):
        cargo("install", "--path", "surfer", "--root", prefix)
