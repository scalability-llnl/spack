# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Glow(GoPackage):
    """
    Glow is a terminal based markdown reader designed
    from the ground up to bring out the beauty—and power—of the CLI.
    Use it to discover markdown files,
    read documentation directly on the command line and stash markdown files
    to your own private collection, so you can read them anywhere.
    Glow will find local markdown files in subdirectories or a local Git repository.
    """

    homepage = "https://github.com/charmbracelet/glow"

    url = "https://github.com/charmbracelet/glow/archive/refs/tags/v1.5.1.tar.gz"

    license("MIT")

    version("1.5.1", sha256="b4ecf269b7c6447e19591b1d23f398ef2b38a6a75be68458390b42d3efc44b92")
    version("1.5.0", sha256="66f2a876eba15d71cfd08b56667fb07e1d49d383aa17d31696a39e794e23ba92")
    version("1.4.1", sha256="ff6dfd7568f0bac5144ffa3a429ed956dcbdb531487ef6e38ac61365322c9601")
    version("1.4.0", sha256="97d373e002332e54e2fb808ea38f098ca49e2b88038c115bd6d33d0b3b921495")
    version("1.3.0", sha256="828d8453f026a24cd7a6dcf8d97213fe713cadcfab7ca969d5f4c8338d88bb86")
    version("1.2.1", sha256="ceb9369e2f93412abf914fd4cdc2e1a7e70cf48e2b2607c1e10847223c4a1b68")
    version("1.2.0", sha256="75d80dcd3258569e187d189f96f79de544332b72d635cc20b5111453d03c3a2d")
    version("1.1.0", sha256="c9a72e2267b95e39033e845961ad45675c9f0d86080b138c6a2fbf2a5d3428d1")
    version("1.0.2", sha256="2d98c1e780d750b83d8da094de4c2a999c324021906e6d813b7c75d0320243c8")
    version("1.0.1", sha256="78d163bea8e6c13fb343f1e3586e93e0392e5052c408a248cc2f0fcc7aa38618")

    @run_after("install")
    def install_completions(self):
        glow = Executable(self.prefix.bin.glow)

        mkdirp(bash_completion_path(self.prefix))
        with open(bash_completion_path(self.prefix) / "glow", "w") as file:
            glow("completion", "bash", output=file)

        mkdirp(fish_completion_path(self.prefix))
        with open(fish_completion_path(self.prefix) / "glow.fish", "w") as file:
            glow("completion", "fish", output=file)

        mkdirp(zsh_completion_path(self.prefix))
        with open(zsh_completion_path(self.prefix) / "_glow", "w") as file:
            glow("completion", "zsh", output=file)
