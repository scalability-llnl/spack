# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Abduco(MakefilePackage):
    """abduco provides session management i.e. it allows programs to be
    run independently from its controlling terminal. That is programs
    can be detached - run in the background - and then later reattached.
    Together with dvtm it provides a simpler and cleaner alternative to
    tmux or screen."""

    homepage = "https://github.com/martanne/abduco"
    url = "https://github.com/martanne/abduco/archive/v0.6.tar.gz"

    license("ISC")

    version("0.6", sha256="647d0381418f43a38f861d151b0efb2e3458ec651914e7d477956768b0af9bb7")
    version("0.5", sha256="bf22226a4488355a7001a5dabbd1e8e3b7e7645efd1519274b956fcb8bcff086")
    version("0.4", sha256="bda3729df116ce41f9a087188d71d934da2693ffb1ebcf33b803055eb478bcbb")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        make(f"PREFIX={prefix}", "install")
