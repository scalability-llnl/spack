# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mokutil(AutotoolsPackage):
    """The utility to manipulate machines owner keys which managed in shim."""

    homepage = "https://github.com/lcp/mokutil"
    url = "https://github.com/lcp/mokutil/archive/0.4.0.tar.gz"

    license("GPL-3.0-or-later")

    version("0.4.0", sha256="2e9c574e4a4fa63b2f23116cdcb389f448a28945548e232076f77947e35b7361")
    version("0.3.0", sha256="70ccbffbbba0427dfd6b57902d667bf73d6223296c897ce3441fc2221352a773")
    version("0.2.0", sha256="a51ef146b8f2169c4e4a0d2f86cae5f4d66cc520989fc2f70a7a620f9587a20b")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("efivar")

    def setup_build_environment(self, env):
        env.prepend_path("C_INCLUDE_PATH", self.spec["efivar"].prefix.include.efivar)

    def install(self, spec, prefix):
        bash_completion_dir = "BASH_COMPLETION_DIR="
        bash_completion_dir += "{0}/usr/share/bash-completion/completions"
        make("install", bash_completion_dir.format(prefix))
