# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gpgme(AutotoolsPackage):
    """GPGME is the standard library to access GnuPG
    functions from programming languages."""

    homepage = "https://www.gnupg.org/software/gpgme/index.html"
    url = "https://www.gnupg.org/ftp/gcrypt/gpgme/gpgme-1.16.0.tar.bz2"

    executables = ["^gpgme-config$"]

    version("1.20.0", sha256="25a5785a5da356689001440926b94e967d02e13c49eb7743e35ef0cf22e42750")
    version("1.19.0", sha256="cb58494dc415fba9eeb12b826550ad3190dc92e265c5bb2ae1a21c92841cfd38")
    version("1.18.0", sha256="361d4eae47ce925dba0ea569af40e7b52c645c4ae2e65e5621bf1b6cdd8b0e9e")
    version("1.16.0", sha256="6c8cc4aedb10d5d4c905894ba1d850544619ee765606ac43df7405865de29ed0")
    version("1.12.0", sha256="b4dc951c3743a60e2e120a77892e9e864fb936b2e58e7c77e8581f4d050e8cd8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # https://dev.gnupg.org/T5509 - New test t-edit-sign test crashes with GCC 11.1.0
    patch(
        "https://git.gnupg.org/cgi-bin/gitweb.cgi?p=gpgme.git;a=commitdiff_plain;h=81a33ea5e1b86d586b956e893a5b25c4cd41c969;hp=e8e055e682f8994d62012574e1c8d862ca72a35d",
        sha256="b934e3cb0b3408ad27990d97b594c89801a4748294e2eb5804a455a312821411",
        when="@1.16.0",
    )

    depends_on("gnupg", type="build")
    depends_on("libgpg-error", type="build")
    depends_on("libassuan@2.4.2:2", type=("build", "link"))

    @classmethod
    def determine_version(cls, exe):
        return Executable(exe)("--version", output=str, error=str).rstrip()

    def configure_args(self):
        """Fix the build when incompatible Qt libraries are installed on the host"""
        return ["--enable-languages=cpp"]

    def setup_build_environment(self, env):
        """Build tests create a public keyring in ~/.gnupg if $HOME is not redirected"""
        if self.run_tests:
            env.set("HOME", self.build_directory)
            env.prepend_path("LD_LIBRARY_PATH", self.spec["libgpg-error"].prefix.lib)

    @property
    def make_tests(self):
        """Use the Makefile's tests variable to control if the build tests shall run"""
        return "tests=tests" if self.run_tests else "tests="

    def build(self, spec, prefix):
        make(self.make_tests)

    def install(self, spec, prefix):
        make(self.make_tests, "install")
