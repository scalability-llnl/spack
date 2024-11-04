# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Glab(GoPackage):
    """GitLab's official command line tool."""

    homepage = "https://gitlab.com/gitlab-org/cli"
    url = "https://gitlab.com/gitlab-org/cli/-/archive/v1.22.0/cli-v1.22.0.tar.gz"

    maintainers("alecbcs")

    license("MIT")

    version("1.46.1", sha256="935f732ddacc6e54fc83d06351fc25454ac8a58c465c3efa43e066ea226257c2")
    version("1.36.0", sha256="8d6c759ebfe9c6942fcdb7055a4a5c7209a3b22beb25947f906c9aef3bc067e8")
    version("1.35.0", sha256="7ed31c7a9b425fc15922f83c5dd8634a2758262a4f25f92583378655fcad6303")
    version("1.33.0", sha256="447a9b76acb5377642a4975908f610a3082026c176329c7c8cfed1461d2e1570")
    version("1.31.0", sha256="5648e88e7d6cc993227f5a4e80238af189bed09c7aed1eb12be7408e9a042747")
    version("1.30.0", sha256="d3c1a9ba723d94a0be10fc343717cf7b61732644f5c42922f1c8d81047164b99")
    version("1.29.4", sha256="f6c628d376ea2db9872b1df20abc886281ba58b7bdf29f19dc179c541958640b")
    version("1.28.1", sha256="243a0f15e4400aab7b4d27ec71c6ae650bf782473c47520ffccd57af8d939c90")
    version("1.28.0", sha256="9a0b433c02033cf3d257405d845592e2b7c2e38741027769bb97a8fd763aeeac")
    version("1.27.0", sha256="26bf5fe24eeaeb0f861c89b31129498f029441ae11cc9958e14ad96ec1356d51")
    version("1.26.0", sha256="af1820a7872d53c7119a23317d6c80497374ac9529fc2ab1ea8b1ca033a9b4da")
    version("1.22.0", sha256="4d9bceb6818c8bf9f681119dae3a65f1c895fa21e9da6b38e8f88d245f524e10")
    version("1.21.1", sha256="8bb35c5cf6b011ff14d1eaa9ab70ec052d296978792984250e9063b006ee4d50")
    version("1.20.0", sha256="6beb0186fa50d0dea3b05fcfe6e4bc1f9be0c07aa5fa15b37ca2047b16980412")

    depends_on("go@1.13:", type="build")
    depends_on("go@1.17:", type="build", when="@1.22:")
    depends_on("go@1.18:", type="build", when="@1.23:")
    depends_on("go@1.19:", type="build", when="@1.35:")
    depends_on("go@1.21:", type="build", when="@1.37:")
    depends_on("go@1.22.3:", type="build", when="@1.41:")
    depends_on("go@1.22.4:", type="build", when="@1.42:")
    depends_on("go@1.22.5:", type="build", when="@1.44:")
    depends_on("go@1.23:", type="build", when="@1.46:")

    build_directory = "cmd/glab"

    @run_after("install")
    def install_completions(self):
        glab = Executable(self.prefix.bin.glab)

        mkdirp(bash_completion_path(self.prefix))
        with open(bash_completion_path(self.prefix) / "glab", "w") as file:
            glab("completion", "-s", "bash", output=file)

        mkdirp(fish_completion_path(self.prefix))
        with open(fish_completion_path(self.prefix) / "glab.fish", "w") as file:
            glab("completion", "-s", "fish", output=file)

        mkdirp(zsh_completion_path(self.prefix))
        with open(zsh_completion_path(self.prefix) / "_glab", "w") as file:
            glab("completion", "-s", "zsh", output=file)
