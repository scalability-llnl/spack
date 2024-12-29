# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fd(CargoPackage):
    """A simple, fast and user-friendly alternative to 'find'"""

    homepage = "https://github.com/sharkdp/fd"
    url = "https://github.com/sharkdp/fd/archive/refs/tags/v8.4.0.tar.gz"

    maintainers("alecbcs", "ashermancinelli")

    license("Apache-2.0 OR MIT")

    version("10.2.0", sha256="73329fe24c53f0ca47cd0939256ca5c4644742cb7c14cf4114c8c9871336d342")
    version("10.1.0", sha256="ee4b2403388344ff60125c79ff25b7895a170e7960f243ba2b5d51d2c3712d97")
    version("9.0.0", sha256="306d7662994e06e23d25587246fa3fb1f528579e42a84f5128e75feec635a370")
    version("8.7.0", sha256="13da15f3197d58a54768aaad0099c80ad2e9756dd1b0c7df68c413ad2d5238c9")
    version("8.4.0", sha256="d0c2fc7ddbe74e3fd88bf5bb02e0f69078ee6d2aeea3d8df42f508543c9db05d")
    version("7.4.0", sha256="33570ba65e7f8b438746cb92bb9bc4a6030b482a0d50db37c830c4e315877537")

    depends_on("rust@1.64:", type="build", when="@8.7:")
    depends_on("rust@1.70:", type="build", when="@8.7.1:")
    depends_on("rust@1.77.2:", type="build", when="@10:")

    @run_after("install")
    def install_completions(self):
        fd = Executable(self.prefix.bin.fd)

        mkdirp(bash_completion_path(self.prefix))
        with open(bash_completion_path(self.prefix) / "fd", "w") as file:
            fd("--gen-completions", "bash", output=file)

        mkdirp(fish_completion_path(self.prefix))
        with open(fish_completion_path(self.prefix) / "fd.fish", "w") as file:
            fd("--gen-completions", "fish", output=file)

        mkdirp(zsh_completion_path(self.prefix))
        with open(zsh_completion_path(self.prefix) / "_fd", "w") as file:
            fd("--gen-completions", "zsh", output=file)
