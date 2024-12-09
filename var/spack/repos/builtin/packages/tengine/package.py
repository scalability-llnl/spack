# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tengine(AutotoolsPackage):
    """A distribution of Nginx with some advanced features."""

    homepage = "https://tengine.taobao.org/"
    url = "https://github.com/alibaba/tengine/archive/2.3.2.tar.gz"

    version("3.1.0", sha256="64ed7155c0c904ce0fe7199c21b8eb6c2abfc267278fa8af832c0cb781e864dc")
    version("2.3.2", sha256="a65998a35739a59f8a16ec4c6090a59e569ba5a1a3f68fecad952057c1a18fea")
    version("2.3.1", sha256="3dd93f813b80ed7581a81079a2037df6e4777b7e760fd6635b4009d344a5ab1c")
    version("2.3.0", sha256="17cf1380d4faefb70707970437b3f8b66f6ff4530b5e6e61970b35f59b2e2624")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("pcre")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
