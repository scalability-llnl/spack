# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hunspell(AutotoolsPackage):
    """The most popular spellchecking library (sez the author...)."""

    homepage = "https://hunspell.github.io/"
    url = "https://github.com/hunspell/hunspell/archive/v1.6.0.tar.gz"

    license("GPL-2.0-or-later OR LGPL-2.1-or-later OR MPL-1.1")

    version("1.7.2", sha256="69fa312d3586c988789266eaf7ffc9861d9f6396c31fc930a014d551b59bbd6e")
    version("1.7.0", sha256="bb27b86eb910a8285407cf3ca33b62643a02798cf2eef468c0a74f6c3ee6bc8a")
    version("1.6.0", sha256="512e7d2ee69dad0b35ca011076405e56e0f10963a02d4859dbcc4faf53ca68e2")

    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("gettext")

    # TODO: If https://github.com/spack/spack/pull/12344 is merged, this
    # method is unnecessary.
    def autoreconf(self, spec, prefix):
        autoreconf = which("autoreconf")
        autoreconf("-fiv")
