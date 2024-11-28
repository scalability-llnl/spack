# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nim(Package):
    """Nim is a statically typed compiled systems programming language.
    It combines successful concepts from mature languages like Python,
    Ada and Modula.
    """

    homepage = "https://nim-lang.org/"
    url = "https://nim-lang.org/download/nim-1.4.4.tar.xz"

    license("MIT")

    version("2.0.4", sha256="71526bd07439dc8e378fa1a6eb407eda1298f1f3d4df4476dca0e3ca3cbe3f09")
    version("1.9.3", sha256="d8de7515db767f853d9b44730f88ee113bfe9c38dcccd5afabc773e2e13bf87c")
    version("1.4.4", sha256="6d73729def143f72fc2491ca937a9cab86d2a8243bd845a5d1403169ad20660e")
    version("1.4.2", sha256="03a47583777dd81380a3407aa6a788c9aa8a67df4821025770c9ac4186291161")
    version(
        "0.20.0",
        sha256="51f479b831e87b9539f7264082bb6a64641802b54d2691b3c6e68ac7e2699a90",
        deprecated=True,
    )
    version(
        "0.19.6",
        sha256="a09f0c58d29392434d4fd6d15d4059cf7e013ae948413cb9233b8233d67e3a29",
        deprecated=True,
    )
    version(
        "0.19.9",
        sha256="154c440cb8f27da20b3d6b1a8cc03f63305073fb995bbf26ec9bc6ad891ce276",
        url="https://github.com/nim-lang/nightlies/releases/download/2019-06-02-devel-1255b3c/nim-0.19.9-linux_x64.tar.xz",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("pcre")
    depends_on("openssl")

    def patch(self):
        install_sh_path = join_path(self.stage.source_path, "install.sh")
        filter_file("1/nim", "1", install_sh_path)

    def install(self, spec, prefix):
        bash = which("bash")
        bash("./build.sh")

        nim = Executable(join_path("bin", "nim"))
        nim("c", "koch")

        koch = Executable("./koch")
        koch("boot", "-d:release")
        koch("tools")
        koch("nimble")

        bash("./install.sh", prefix)
        install(join_path("bin", "nimble"), join_path(prefix, "bin"))
