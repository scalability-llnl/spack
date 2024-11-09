# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Neovim(CMakePackage):
    """Neovim: Vim-fork focused on extensibility and usability"""

    homepage = "https://neovim.io"
    git = "https://github.com/neovim/neovim.git"
    url = "https://github.com/neovim/neovim/archive/v0.4.3.tar.gz"

    maintainers("albestro", "trws")

    license("Apache-2.0 AND Vim")

    version("master", branch="master")
    version("stable", tag="stable", commit="d772f697a281ce9c58bf933997b87c7f27428a60")
    version("0.10.0", sha256="372ea2584b0ea2a5a765844d95206bda9e4a57eaa1a2412a9a0726bab750f828")
    version("0.9.5", sha256="fe74369fc30a32ec7a086b1013acd0eacd674e7570eb1acc520a66180c9e9719")
    version("0.9.4", sha256="148356027ee8d586adebb6513a94d76accc79da9597109ace5c445b09d383093")
    version("0.9.2", sha256="06b8518bad4237a28a67a4fbc16ec32581f35f216b27f4c98347acee7f5fb369")
    version("0.9.1", sha256="8db17c2a1f4776dcda00e59489ea0d98ba82f7d1a8ea03281d640e58d8a3a00e")
    version("0.9.0", sha256="39d79107c54d2f3babcad2cd157c399241c04f6e75e98c18e8afaf2bb5e82937")
    version("0.8.3", sha256="adf45ff160e1d89f519b6114732eba03485ae469beb27919b0f7a4f6b44233c1")
    version("0.8.2", sha256="c516c8db73e1b12917a6b2e991b344d0914c057cef8266bce61a2100a28ffcc9")
    version("0.8.0", sha256="505e3dfb71e2f73495c737c034a416911c260c0ba9fd2092c6be296655be4d18")
    version("0.7.2", sha256="ccab8ca02a0c292de9ea14b39f84f90b635a69282de38a6b4ccc8565bc65d096")
    version("0.7.0", sha256="792a9c55d5d5f4a5148d475847267df309d65fb20f05523f21c1319ea8a6c7df")
    version("0.6.1", sha256="dd882c21a52e5999f656cae3f336b5fc702d52addd4d9b5cd3dc39cfff35e864")
    version("0.6.0", sha256="2cfd600cfa5bb57564cc22ffbbbcb2c91531053fc3de992df33656614384fa4c")
    version("0.5.1", sha256="aa449795e5cc69bdd2eeed7095f20b9c086c6ecfcde0ab62ab97a9d04243ec84")
    version(
        "0.5.0",
        sha256="6bcfa5192c9460c946e853dbd1a0baf659df5de184436144147711d1bceedeee",
        deprecated=True,
    )
    version(
        "0.4.4",
        sha256="2f76aac59363677f37592e853ab2c06151cca8830d4b3fe4675b4a52d41fc42c",
        deprecated=True,
    )
    version(
        "0.4.3",
        sha256="91a0b5d32204a821bf414690e6b48cf69224d1961d37158c2b383f6a6cf854d2",
        deprecated=True,
    )
    version(
        "0.3.4",
        sha256="a641108bdebfaf319844ed46b1bf35d6f7c30ef5aeadeb29ba06e19c3274bc0e",
        deprecated=True,
    )
    version(
        "0.3.1",
        sha256="bc5e392d4c076407906ccecbc283e1a44b7832c2f486cad81aa04cc29973ad22",
        deprecated=True,
    )
    version(
        "0.3.0",
        sha256="f7acb61b16d3f521907d99c486b7a9f1e505e8b2a18c9ef69a6d7f18f29f74b8",
        deprecated=True,
    )
    version(
        "0.2.2",
        sha256="a838ee07cc9a2ef8ade1b31a2a4f2d5e9339e244ade68e64556c1f4b40ccc5ed",
        deprecated=True,
    )
    version(
        "0.2.1",
        sha256="9e2c068a8994c9023a5f84cde9eb7188d3c85996a7e42e611e3cd0996e345dd3",
        deprecated=True,
    )
    version(
        "0.2.0",
        sha256="72e263f9d23fe60403d53a52d4c95026b0be428c1b9c02b80ab55166ea3f62b5",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    variant(
        "no_luajit",
        default=False,
        description="use lua rather than luajit as lua language provider",
    )

    # depend on virtual, lua-luajit-openresty preferred
    depends_on("luajit", when="~no_luajit")
    depends_on("lua-lang@5.1", when="+no_luajit")

    # dependencies to allow regular lua to work
    depends_on("lua-ffi", when="^[virtuals=lua-lang] lua", type=("link", "run"))
    depends_on("lua-bitlib", when="^[virtuals=lua-lang] lua", type=("link", "run"))

    # base dependencies
    depends_on("cmake@3.0:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("gettext")
    depends_on("gperf", type="link")
    depends_on("jemalloc", type="link", when="platform=linux")
    depends_on("lua-lpeg")
    depends_on("lua-mpack")
    depends_on("iconv", type="link")
    depends_on("libtermkey", type="link")
    depends_on("libuv", type="link")
    depends_on("libluv", type="link")
    depends_on("libvterm", type="link")
    depends_on("msgpack-c", type="link")
    depends_on("unibilium", type="link")
    depends_on("unibilium@:1.2.0", type="link", when="@0.2.0")

    # versions
    with when("@0.4:"):
        depends_on("libuv@1.28:", type="link")
        depends_on("libluv@1.30.0:", type="link")
        depends_on("libtermkey@0.18:", type="link")
        depends_on("libvterm@0.1:", type="link")
        depends_on("unibilium@2.0:", type="link")
        depends_on("msgpack-c@1.0.0:", type="link")
    with when("@0.5:"):
        depends_on("libuv@1.42:", type="link")
        depends_on("tree-sitter")
    with when("@0.6:"):
        depends_on("cmake@3.10:", type="build")
        depends_on("gperf@3.1:", type="link")
        conflicts("^libiconv@:1.14")
        depends_on("libtermkey@0.22:", type="link")
        depends_on("libvterm@0.1.4:", type="link")
        depends_on("msgpack-c@3.0.0:", type="link")
    with when("@0.7:"):
        depends_on("gettext@0.20.1:")
        depends_on("libluv@1.43.0:", type="link")
        depends_on("libuv@1.44.1:", type="link")
        depends_on("tree-sitter@0.20.6:")
    with when("@0.8:"):
        depends_on("libvterm@0.3:", type="link")
    with when("@0.9:"):
        depends_on("tree-sitter@0.20.8:")
    with when("@0.10:"):
        depends_on("cmake@3.13:", type="build")
        depends_on("libvterm@0.3.3:")
        depends_on("tree-sitter@0.20.9:")
    with when("@master"):
        depends_on("utf8proc", type="link")

    # Support for `libvterm@0.2:` has been added in neovim@0.8.0
    # term: Add support for libvterm >= 0.2 (https://github.com/neovim/neovim/releases/tag/v0.8.0)
    # https://github.com/neovim/neovim/issues/16217#issuecomment-958590493
    conflicts("libvterm@0.2:", when="@:0.7")

    @when("^lua")
    def cmake_args(self):
        return [self.define("PREFER_LUA", True)]
