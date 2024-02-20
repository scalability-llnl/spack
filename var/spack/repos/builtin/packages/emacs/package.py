# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class Emacs(AutotoolsPackage, GNUMirrorPackage):
    """The Emacs programmable text editor."""

    homepage = "https://www.gnu.org/software/emacs"
    git = "git://git.savannah.gnu.org/emacs.git"
    gnu_mirror_path = "emacs/emacs-24.5.tar.gz"

    maintainers("alecbcs")

    license("GPL-3.0-or-later")

    version("master", branch="master")
    version("29.3", sha256="2de8df5cab8ac697c69a1c46690772b0cf58fe7529f1d1999582c67d927d22e4")
    version("29.2", sha256="ac8773eb17d8b3c0c4a3bccbb478f7c359266b458563f9a5e2c23c53c05e4e59")
    version("29.1", sha256="5b80e0475b0e619d2ad395ef5bc481b7cb9f13894ed23c301210572040e4b5b1")
    version("28.2", sha256="a6912b14ef4abb1edab7f88191bfd61c3edd7085e084de960a4f86485cb7cad8")
    version("28.1", sha256="1439bf7f24e5769f35601dbf332e74dfc07634da6b1e9500af67188a92340a28")
    version("27.2", sha256="80ff6118fb730a6d8c704dccd6915a6c0e0a166ab1daeef9fe68afa9073ddb73")
    version("27.1", sha256="ffbfa61dc951b92cf31ebe3efc86c5a9d4411a1222b8a4ae6716cfd0e2a584db")
    version("26.3", sha256="09c747e048137c99ed35747b012910b704e0974dde4db6696fde7054ce387591")
    version("26.2", sha256="4f99e52a38a737556932cc57479e85c305a37a8038aaceb5156625caf102b4eb")
    version("26.1", sha256="760382d5e8cdc5d0d079e8f754bce1136fbe1473be24bb885669b0e38fc56aa3")
    version("25.3", sha256="f72c6a1b48b6fbaca2b991eed801964a208a2f8686c70940013db26cd37983c9")
    version("25.2", sha256="505bbd6ea6c197947001d0f80bfccb6b30e1add584d6376f54d4fd6e4de72d2d")
    version("25.1", sha256="763344b90db4d40e9fe90c5d14748a9dbd201ce544e2cf0835ab48a0aa4a1c67")
    version("24.5", sha256="2737a6622fb2d9982e9c47fb6f2fb297bda42674e09db40fc9bcc0db4297c3b6")

    variant("X", default=False, description="Enable an X toolkit")
    variant(
        "toolkit",
        default="gtk",
        values=("gtk", "athena"),
        description="Select an X toolkit (gtk, athena)",
    )
    variant("tls", default=True, description="Build Emacs with gnutls")
    variant("native", default=False, when="@28:", description="enable native compilation of elisp")
    variant("treesitter", default=False, when="@29:", description="Build with tree-sitter support")
    variant("json", default=False, when="@27:", description="Build with json support")

    depends_on("pkgconfig", type="build")
    depends_on("gzip", type="build")

    depends_on("ncurses")
    depends_on("pcre")
    depends_on("zlib-api")
    depends_on("libxml2")
    depends_on("libtiff", when="+X")
    depends_on("libpng", when="+X")
    depends_on("libxpm", when="+X")
    depends_on("giflib", when="+X")
    depends_on("libx11", when="+X")
    depends_on("libxaw", when="+X toolkit=athena")
    depends_on("gtkplus", when="+X toolkit=gtk")
    depends_on("gnutls", when="+tls")
    depends_on("jpeg")
    depends_on("tree-sitter", when="+treesitter")
    depends_on("m4", type="build", when="@master:")
    depends_on("autoconf", type="build", when="@master:")
    depends_on("automake", type="build", when="@master:")
    depends_on("libtool", type="build", when="@master:")
    depends_on("texinfo", type="build")
    depends_on("gcc@11: +strip languages=jit", when="+native")
    depends_on("jansson@2.7:", when="+json")

    conflicts("@:26.3", when="platform=darwin os=catalina")

    @when("platform=darwin")
    def setup_build_environment(self, env):
        # on macOS, emacs' config does search hard enough for ncurses'
        # termlib `-ltinfo` lib, which results in linker errors
        if "+termlib" in self.spec["ncurses"]:
            env.append_flags("LDFLAGS", "-ltinfo")

    def configure_args(self):
        spec = self.spec

        toolkit = spec.variants["toolkit"].value
        if "+X" in spec:
            args = ["--with-x", "--with-x-toolkit={0}".format(toolkit)]
        else:
            args = ["--without-x"]

        # On OS X/macOS, do not build "nextstep/Emacs.app", because
        # doing so throws an error at build-time
        if sys.platform == "darwin":
            args.append("--without-ns")

        args += self.with_or_without("native-compilation", variant="native")
        args += self.with_or_without("gnutls", variant="tls")
        args += self.with_or_without("tree-sitter", variant="treesitter")
        args += self.with_or_without("json")

        return args

    def run_version_check(self, bin):
        """Runs and checks output of the installed binary."""
        exe_path = join_path(self.prefix.bin, bin)
        if not os.path.exists(exe_path):
            raise SkipTest(f"{exe_path} is not installed")

        exe = which(exe_path)
        out = exe("--version", output=str.split, error=str.split)
        assert str(self.spec.version) in out

    def test_ctags(self):
        """check ctags version"""
        self.run_version_check("ctags")

    def test_ebrowse(self):
        """check ebrowse version"""
        self.run_version_check("ebrowse")

    def test_emacs(self):
        """check emacs version"""
        self.run_version_check("emacs")

    def test_emacsclient(self):
        """check emacsclient version"""
        self.run_version_check("emacsclient")

    def test_etags(self):
        """check etags version"""
        self.run_version_check("etags")
