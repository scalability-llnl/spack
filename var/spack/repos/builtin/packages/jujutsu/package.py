# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import spack.build_systems.cargo
from spack.package import *


class Jujutsu(CargoPackage):
    """A Git-compatible VCS that is both simple and powerful"""

    homepage = "https://jj-vcs.github.io/jj/latest/"
    url = "https://github.com/jj-vcs/jj/archive/refs/tags/v0.25.0.tar.gz"

    maintainers("pranav-sivaraman")

    license("Apache-2.0", checked_by="pranav-sivaraman")

    version("0.25.0", sha256="3a99528539e414a3373f24eb46a0f153d4e52f7035bb06df47bd317a19912ea3")

    depends_on("rust@1.76:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("openssl")


class CargoBuilder(spack.build_systems.cargo.CargoBuilder):
    @property
    def build_directory(self):
        """Return the directory containing the main Cargo.toml."""
        return f"{self.pkg.stage.source_path}/cli"

    @property
    def build_args(self):
        return ["--bin", "jj", "jj-cli"]
