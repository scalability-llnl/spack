# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Hugo(GoPackage):
    """The world's fastest framework for building websites."""

    homepage = "https://gohugo.io"
    url = "https://github.com/gohugoio/hugo/archive/v0.53.tar.gz"

    executables = ["^hugo$"]

    maintainers("alecbcs")

    license("Apache-2.0")

    version("0.135.0", sha256="a75c4c684d2125255f214d11b9834a5ec6eb64353f4de2c06952d2b3b7430f0e")
    version("0.127.0", sha256="549c7ebdf2ee6b3107ea10a9fbd9932a91bb3f30f7e8839245f6d8e318aca88c")
    version("0.126.3", sha256="2a1d65b09884e3c57a8705db99487404856c947dd847cf7bb845e0e1825b33ec")
    version("0.118.2", sha256="915d7dcb44fba949c80858f9c2a55a11256162ba28a9067752f808cfe8faedaa")
    version("0.112.7", sha256="d706e52c74f0fb00000caf4e95b98e9d62c3536a134d5e26b433b1fa1e2a74aa")
    version("0.111.3", sha256="b6eeb13d9ed2e5d5c6895bae56480bf0fec24a564ad9d17c90ede14a7b240999")
    version("0.111.2", sha256="66500ae3a03cbf51a6ccf7404d01f42fdc454aa1eaea599c934860bbf0aa2fc5")
    version("0.111.1", sha256="a71d4e1f49ca7156d3811c0b10957816b75ff2e01b35ef326e7af94dfa554ec0")
    version("0.110.0", sha256="eeb137cefcea1a47ca27dc5f6573df29a8fe0b7f1ed0362faf7f73899e313770")
    version("0.109.0", sha256="35a5ba92057fe2c20b2218c374e762887021e978511d19bbe81ce4d9c21f0c78")
    version("0.108.0", sha256="dc90e9de22ce87c22063ce9c309cefacba89269a21eb369ed556b90b22b190c5")
    version("0.107.0", sha256="31d959a3c1633087d338147782d03bdef65323b67ff3efcec7b40241413e270a")
    version("0.106.0", sha256="9219434beb51466487b9f8518edcbc671027c1998e5a5820d76d517e1dfbd96a")

    depends_on("go@1.11:", type="build", when="@0.48:")
    depends_on("go@1.18:", type="build", when="@0.106:")
    depends_on("go@1.20:", type="build", when="@0.123:")
    depends_on("go@1.21.8:", type="build", when="@0.131:")
    depends_on("go@1.22.6:", type="build", when="@0.133:")

    variant("extended", default=False, description="Enable extended features")

    phases = ["build", "install"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("version", output=str, error=str)
        match = re.search(r"Hugo Static Site Generator v(\S+)", output)
        return match.group(1) if match else None

    @property
    def build_args(self):
        args = super().build_args
        if self.spec.satisfies("+extended"):
            args.extend(["--tags", "extended"])

        return args

    @run_after("install")
    def install_completions(self):
        hugo = Executable(self.prefix.bin.hugo)

        mkdirp(bash_completion_path(self.prefix))
        with open(bash_completion_path(self.prefix) / "hugo", "w") as file:
            hugo("completion", "bash", output=file)

        mkdirp(fish_completion_path(self.prefix))
        with open(fish_completion_path(self.prefix) / "hugo.fish", "w") as file:
            hugo("completion", "fish", output=file)

        mkdirp(zsh_completion_path(self.prefix))
        with open(zsh_completion_path(self.prefix) / "_hugo", "w") as file:
            hugo("completion", "zsh", output=file)
