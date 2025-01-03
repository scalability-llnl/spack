# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import shlex

from spack.package import *
from spack.util.environment import filter_system_paths


class Nim(Package):
    """Nim is a statically typed compiled systems programming language.
    It combines successful concepts from mature languages like Python,
    Ada and Modula.
    """

    homepage = "https://nim-lang.org/"
    url = "https://nim-lang.org/download/nim-2.2.0.tar.xz"
    git = "https://github.com/nim-lang/Nim.git"

    license("MIT", checked_by="Buldram")

    maintainers("Buldram")

    version("devel", branch="devel")
    version("2.2.0", sha256="ce9842849c9760e487ecdd1cdadf7c0f2844cafae605401c7c72ae257644893c")
    version("2.0.12", sha256="c4887949c5eb8d7f9a9f56f0aeb2bf2140fabf0aee0f0580a319e2a09815733a")
    version("2.0.4", sha256="71526bd07439dc8e378fa1a6eb407eda1298f1f3d4df4476dca0e3ca3cbe3f09")
    version("1.6.20", sha256="ffed047504d1fcaf610f0dd7cf3e027be91a292b0c9c51161504c2f3b984ffb9")
    version("1.4.8", sha256="b798c577411d7d95b8631261dbb3676e9d1afd9e36740d044966a0555b41441a")
    version("1.4.4", sha256="6d73729def143f72fc2491ca937a9cab86d2a8243bd845a5d1403169ad20660e")
    version("1.4.2", sha256="03a47583777dd81380a3407aa6a788c9aa8a67df4821025770c9ac4186291161")
    version("1.2.18", sha256="a1739185508876f6e21a13f590a20e219ce3eec1b0583ea745e9058c37ad833e")
    with default_args(deprecated=True):
        # Past development (odd-numbered) versions
        version("1.9.3", sha256="d8de7515db767f853d9b44730f88ee113bfe9c38dcccd5afabc773e2e13bf87c")

        # CVE-2021-46872, CVE-2021-29495, CVE-2021-21374, CVE-2021-21373, CVE-2021-21372
        version(
            "1.0.10", sha256="28045fb6dcd86bd79748ead7874482d665ca25edca68f63d6cebc925b1428da5"
        )

        # CVE-2020-15694, CVE-2020-15693, CVE-2020-15692, CVE-2020-15690
        version(
            "0.20.0", sha256="51f479b831e87b9539f7264082bb6a64641802b54d2691b3c6e68ac7e2699a90"
        )
        version(
            "0.19.9",
            sha256="154c440cb8f27da20b3d6b1a8cc03f63305073fb995bbf26ec9bc6ad891ce276",
            url="https://github.com/nim-lang/nightlies/releases/download/2019-06-02-devel-1255b3c/nim-0.19.9-linux_x64.tar.xz",
        )
        version(
            "0.19.6", sha256="a09f0c58d29392434d4fd6d15d4059cf7e013ae948413cb9233b8233d67e3a29"
        )

    variant(
        "sqlite", default=False, when="@0:1.7.3", description="Install SQLite for std/db_sqlite"
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("gmake", type="build", when="@devel,0.20:")
    depends_on("pcre", type="link")
    depends_on("openssl", type="link")
    depends_on("openssl@1", type="link", when="@0:1.6.9")
    depends_on("sqlite@3:", type="link", when="+sqlite")

    # CVE-2021-46872
    patch(
        "https://github.com/nim-lang/Nim/commit/17522d6ae1444614be78b1002005513105f2893f.patch?full_index=1",
        sha256="fee426d5f027a8676d94309932812c5d70e1bc089f4d030326a413cacba78330",
        when="@1.4.0:1.4.9",
    )
    # CVE-2021-21374, CVE-2021-29495
    patch(
        "https://github.com/nim-lang/Nim/commit/c7d090c418f7847bdfa1fd3bfed831470665c3e9.patch?full_index=1",
        sha256="88fd2a137a2170a4df41b9f5419a47aff78b0dbf421405e22a6d6a066e3e0431",
        when="@1.4.0:1.4.3",
    )
    # CVE-2021-21373
    patch(
        "https://github.com/nim-lang/nimble/commit/aec0ae5c23d2e2a2ec28e97dcb9dd6cb1e68b134.patch?full_index=1",
        sha256="4fe4f8b760e7a516fcd51d6ce02562432f1d34623751f52556d4e6c1823e705a",
        when="@1:1.2.9,1.4.0:1.4.3",
        working_dir="dist/nimble",
    )
    # CVE-2021-21372
    patch(
        "https://github.com/nim-lang/nimble/commit/89954f8b03b05970aea78c8fe1241138f5bbeae8.patch?full_index=1",
        sha256="5e6f7e2d2dac5d2ed70b5047418d9b43e156de35737f9fad0052ae30dd539b03",
        when="@0:1.2.9,1.4.0:1.4.3",
        working_dir="dist/nimble",
    )

    resource(
        name="csources_v2",
        git="https://github.com/nim-lang/csources_v2.git",
        commit="86742fb02c6606ab01a532a0085784effb2e753e",
        when="@devel",
    )

    phases = ["build", "install"]

    def patch(self):
        """Hardcode dependency dynamic library paths into
        wrapper modules using rpath."""

        def append_rpath(path, libdirs):
            """Add a pragma at the end of the file which passes
            rpath with libdirs to the linker when the module is used."""

            with open(path, "a") as f:
                scope = False
                for path in filter_system_paths(libdirs):
                    quoted_path = shlex.quote(path)
                    if '"""' in quoted_path:
                        raise InstallError(
                            "Quoted dependency path " + quoted_path + ' contains """'
                        )

                    if not scope:
                        f.write("\nwhen not defined(vcc):\n")  # TODO: Implement for msvc
                        scope = True

                    f.write('  {.passl: """-Xlinker -rpath -Xlinker ' + quoted_path + '""".}\n')

        spec = self.spec
        append_rpath("lib/wrappers/pcre.nim", spec["pcre"].libs.directories)
        append_rpath("lib/wrappers/openssl.nim", spec["openssl"].libs.directories)
        if spec.satisfies("+sqlite"):
            append_rpath("lib/wrappers/sqlite3.nim", spec["sqlite"].libs.directories)

    def build(self, spec, prefix):
        if spec.satisfies("@devel"):
            with working_dir("csources_v2"):
                make()

        elif spec.satisfies("@0.20:"):
            make()

        else:
            Executable("./build.sh")()

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

        Executable("./install.sh")(prefix)

        install_tree("bin", prefix.bin)
