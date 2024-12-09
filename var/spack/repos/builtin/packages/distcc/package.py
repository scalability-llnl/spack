# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Distcc(AutotoolsPackage):
    """distcc is a program to distribute compilation of C or C++
    code across several machines on a network."""

    homepage = "https://github.com/distcc/distcc"
    url = "https://github.com/distcc/distcc/archive/v3.3.3.tar.gz"

    license("GPL-2.0-or-later")

    version("3.4", sha256="37a34c9555498a1168fea026b292ab07e7bb394715d87d8403e0c33b16d2d008")
    version("3.3.5", sha256="13a4b3ce49dfc853a3de550f6ccac583413946b3a2fa778ddf503a9edc8059b0")
    version("3.3.3", sha256="b7f37d314704fbaf006d747514ff6e4d0d722102ef7d2aea132f97cf170f5169")

    depends_on("c", type="build")  # generated

    depends_on("popt")
    depends_on("libiberty")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
