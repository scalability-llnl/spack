# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cronie(AutotoolsPackage):
    """Cronie contains the standard UNIX daemon crond that runs specified
    programs at scheduled times and related tools."""

    homepage = "https://github.com/cronie-crond/cronie"
    url = "https://github.com/cronie-crond/cronie/archive/cronie-1.5.5.tar.gz"

    license("ISC")

    version("1.7.1", sha256="535b96894c52e679085e1d8b36794308c162b1e8dac29031c02f678effc523e1")
    version("1.6.1", sha256="1ddbc8f8d07dfe1d45998b0a0cbd9a216cd4d7bc64d1626b2bc8b3a69e4641d1")
    version("1.5.5", sha256="22c2a2b22577c0f776c1268d0e0f305c5c041e10155022a345b43b665da0ffe9")

    depends_on("c", type="build")  # generated

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
