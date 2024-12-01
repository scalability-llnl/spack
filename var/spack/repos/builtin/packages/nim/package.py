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
    url = "https://nim-lang.org/download/nim-2.2.0.tar.xz"
    git = "https://github.com/nim-lang/Nim.git"

    license("MIT")

    version("devel", branch="devel")
    version("2.2.0", sha256="ce9842849c9760e487ecdd1cdadf7c0f2844cafae605401c7c72ae257644893c")
    version("2.0.12", sha256="c4887949c5eb8d7f9a9f56f0aeb2bf2140fabf0aee0f0580a319e2a09815733a")
    version("2.0.4", sha256="71526bd07439dc8e378fa1a6eb407eda1298f1f3d4df4476dca0e3ca3cbe3f09")
    version("1.9.3", sha256="d8de7515db767f853d9b44730f88ee113bfe9c38dcccd5afabc773e2e13bf87c")
    version("1.6.20", sha256="ffed047504d1fcaf610f0dd7cf3e027be91a292b0c9c51161504c2f3b984ffb9")
    version("1.4.8", sha256="b798c577411d7d95b8631261dbb3676e9d1afd9e36740d044966a0555b41441a")
    version("1.4.4", sha256="6d73729def143f72fc2491ca937a9cab86d2a8243bd845a5d1403169ad20660e")
    version("1.4.2", sha256="03a47583777dd81380a3407aa6a788c9aa8a67df4821025770c9ac4186291161")
    version("1.2.18", sha256="a1739185508876f6e21a13f590a20e219ce3eec1b0583ea745e9058c37ad833e")
    version("1.0.10", sha256="28045fb6dcd86bd79748ead7874482d665ca25edca68f63d6cebc925b1428da5")
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

    resource(
        name="csources_v2",
        git="https://github.com/nim-lang/csources_v2.git",
        commit="86742fb02c6606ab01a532a0085784effb2e753e",
        when="@devel",
    )

    phases = ["build", "install"]

    def build(self, spec, prefix):
        bash = which("bash")
        if spec.satisfies("@devel"):
            with working_dir("csources_v2"):
                bash("./build.sh")
        else:
            bash("./build.sh")

        nim = Executable(join_path("bin", "nim"))
        # Separate nimcache allows parallel compilation of different versions of the Nim compiler
        nim_flags = ["--skipUserCfg", "--skipParentCfg", "--nimcache:nimcache"]
        nim("c", *nim_flags, "koch")

        koch = Executable("./koch")
        koch("boot", "-d:release", *nim_flags)
        koch("tools", *nim_flags)

        if spec.satisfies("@devel"):
            koch("geninstall")

    def install(self, spec, prefix):
        filter_file("1/nim", "1", "install.sh")

        bash = which("bash")
        bash("./install.sh", prefix)

        install_tree("bin", prefix.bin)
