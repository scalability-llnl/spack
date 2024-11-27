# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import stat
import tempfile

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Nix(AutotoolsPackage):
    """Nix, the purely functional package manager"""

    homepage = "https://nixos.org/nix"
    url = "https://github.com/NixOS/nix/archive/2.3.15.zip"
    maintainers("charmoniumq")

    license("LGPL-2.1-or-later")

    version("2.3.15", sha256="7bf04e47960e7895655ad40461f2cf8038b97e98165672db7a7ac1990fc77a22")
    version("2.2.1", sha256="b591664dd1b04a8f197407d445799ece41140a3117bcbdf8e3c5e94cd3f59854")
    version("2.1.3", sha256="80d0834f3e34b3e91bd20969733d8010b3e253517ea64bf12258c5f450f86425")
    version("2.0.4", sha256="49c78122b20e3ad894f546dd2a2f01c32ec528de790314820b1f1335276e3c22")

    patch("fix-doc-build.patch")

    variant(
        "storedir",
        values=str,
        default="none",
        description="path of the Nix store (defaults to /nix)",
    )
    variant(
        "statedir",
        values=str,
        default="none",
        description="path to the locale state (defaults to /nix/var)",
    )
    variant(
        "doc",
        default=False,
        description="Build documentation, tries to fetch docbook.xsl from sf.net",
    )
    variant("sandboxing", default=True, description="Enable build isolation")

    depends_on("autoconf-archive", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("bison@2.6.0:", type="build")
    depends_on("flex@2.5.35:", type="build")
    depends_on("libtool", type="build")
    depends_on("libxml2", when="+doc", type="build")
    depends_on("libxslt", when="+doc", type="build")

    depends_on("boost@1.66.0:+coroutine+context cxxstd=14", when="@2.2.0:")
    depends_on("boost@1.61.0:+coroutine+context cxxstd=14", when="@2.0.0:")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="@2.0.0:")
    depends_on("brotli")
    depends_on("editline")

    depends_on("bzip2")
    depends_on("curl")
    depends_on("libseccomp", when="+sandboxing")
    depends_on("libsodium")
    depends_on("openssl")
    depends_on("sqlite@3.6.19:")
    depends_on("xz")

    # gcc 4.9+ and higher supported with c++14
    conflicts("%gcc@:4.8")

    def configure_args(self):
        args = []
        if "+sandboxing" not in self.spec:
            args.append("--disable-seccomp-sandboxing")
        if "+doc" not in self.spec:
            args.append("--disable-doc-gen")
        storedir = self.spec.variants["storedir"].value
        if storedir != "none":
            args.append("--with-store-dir=" + storedir)
        statedir = self.spec.variants["statedir"].value
        if statedir != "none":
            args.append("--localstatedir=" + statedir)
        return args

    def patch(self):
        """A few files of the testsuite need to be patched for all tests to pass"""
        filter_file("wc", "/usr/bin/wc", "tests/gc-auto.sh")
        # For nix shebang with full path to work, spack's self.prefix has to shorten:
        filter_file("@ENV_PROG@", "/usr/bin/env", "tests/shell.shebang.sh")
        filter_file("@SHELL_PROG@", "/usr/bin/env nix-shell", "tests/shell.shebang.rb")

    def installcheck(self):
        # We have to clean this tmpdir ourself later as it contains readonly directories
        self.test_path = tempfile.mkdtemp(
            prefix="tmp-spack-check-nix-{0}-".format(self.spec.version)
        )
        mkdir(self.test_path + "/nix-test")
        mkdir(self.test_path + "/tests")
        os.environ["TMPDIR"] = self.test_path
        os.environ["TEST_ROOT"] = self.test_path + "/tests"
        with working_dir(self.build_directory):
            make("installcheck")

    @run_after("install")
    def installcheck_clean(self):
        if hasattr(self, "test_path") and self.test_path:
            for root, dirs, files in os.walk(self.test_path, topdown=True):
                os.chmod(root, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
            remove_linked_tree(self.test_path)
