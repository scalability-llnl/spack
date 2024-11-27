# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

from spack.package import *


class Oras(Package):
    """ORAS means OCI Registry As Storage"""

    homepage = "https://oras.land"
    git = "https://github.com/oras-project/oras"
    url = "https://github.com/oras-project/oras/archive/refs/tags/v0.12.0.tar.gz"

    maintainers("vsoch")

    license("MIT")

    version("main", branch="main")
    version("0.12.0", sha256="5e19d61683a57b414efd75bd1b0290c941b8faace5fcc9d488f5e4aa674bf03e")

    depends_on("go", type="build")

    def setup_build_environment(self, env):
        # Point GOPATH at the top of the staging dir for the build step.
        env.prepend_path("GOPATH", self.stage.path)

    def install(self, spec, prefix):
        if self.spec.satisfies("platform=linux target=aarch64:"):
            make("build-linux-arm64")
        elif self.spec.satisfies("platform=linux"):
            make("build-linux")
        elif self.spec.satisfies("platform=darwin target=aarch64:"):
            make("build-mac-arm64")
        elif self.spec.satisfies("platform=darwin"):
            make("build-mac")
        elif self.spec.satisfies("platform=windows"):
            make("build-windows")
        mkdirp(prefix.bin)

        oras = find("bin", "oras")
        if not oras:
            tty.die("Oras executable missing in bin.")
        tty.debug("Found oras executable %s to move into install bin" % oras[0])
        install(oras[0], prefix.bin)
