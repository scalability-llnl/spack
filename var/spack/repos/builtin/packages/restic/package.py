# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Restic(GoPackage):
    """Fast, secure, efficient backup program."""

    homepage = "https://restic.net"
    url = "https://github.com/restic/restic/releases/download/v0.12.1/restic-0.12.1.tar.gz"

    maintainers("alecbcs")

    license("BSD-2-Clause")

    version("0.17.1", sha256="cba3a5759690d11dae4b5620c44f56be17a5688e32c9856776db8a9a93d6d59a")
    version("0.16.4", sha256="d736a57972bb7ee3398cf6b45f30e5455d51266f5305987534b45a4ef505f965")
    version("0.16.3", sha256="a94d6c1feb0034fcff3e8b4f2d65c0678f906fc21a1cf2d435341f69e7e7af52")
    version("0.16.2", sha256="88165b5b89b6064df37a9964d660f40ac62db51d6536e459db9aaea6f2b2fc11")
    version("0.16.0", sha256="b91f5ef6203a5c50a72943c21aaef336e1344f19a3afd35406c00f065db8a8b9")
    version("0.15.2", sha256="52aca841486eaf4fe6422b059aa05bbf20db94b957de1d3fca019ed2af8192b7")
    version("0.15.1", sha256="fce382fdcdac0158a35daa640766d5e8a6e7b342ae2b0b84f2aacdff13990c52")
    version("0.15.0", sha256="85a6408cfb0798dab52335bcb00ac32066376c32daaa75461d43081499bc7de8")
    version("0.14.0", sha256="78cdd8994908ebe7923188395734bb3cdc9101477e4163c67e7cc3b8fd3b4bd6")
    version("0.12.1", sha256="a9c88d5288ce04a6cc78afcda7590d3124966dab3daa9908de9b3e492e2925fb")

    depends_on("go@1.15:", type="build", when="@0.14.0:")
    depends_on("go@1.18:", type="build", when="@0.15.0:")
    depends_on("go@1.19:", type="build", when="@1.16.1:")

    build_directory = "cmd/restic"

    @run_after("install")
    def install_completions(self):
        restic = Executable(self.prefix.bin.restic)

        mkdirp(bash_completion_path(self.prefix))
        mkdirp(fish_completion_path(self.prefix))
        mkdirp(zsh_completion_path(self.prefix))

        restic("generate", "--bash-completion", "restic.bash")
        restic("generate", "--fish-completion", "restic.fish")
        restic("generate", "--zsh-completion", "_restic")

        install("restic.bash", bash_completion_path(self.prefix))
        install("restic.fish", fish_completion_path(self.prefix))
        install("_restic", zsh_completion_path(self.prefix))
